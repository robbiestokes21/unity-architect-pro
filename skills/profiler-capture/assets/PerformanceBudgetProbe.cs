using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Unity.Profiling;
using UnityEngine;
using UnityEngine.Profiling;
using UnityArchitectPro.GameplayTesting;

namespace UnityArchitectPro.Performance
{
    [DisallowMultipleComponent]
    public sealed class PerformanceBudgetProbe : MonoBehaviour
    {
        [SerializeField] private PerformanceBudget budget = new PerformanceBudget();
        [SerializeField] private int warmupFrames = 120;
        [SerializeField] private int measurementFrames = 600;
        [SerializeField] private bool runWithGameplayScenario = true;
        [SerializeField] private MonoBehaviour[] customMetricSources;
        private readonly List<double> _frame = new List<double>(), _cpu = new List<double>(), _gpu = new List<double>(), _gc = new List<double>(), _memory = new List<double>();
        private readonly Dictionary<string, List<double>> _custom = new Dictionary<string, List<double>>();
        private ProfilerRecorder _mainThread; private ProfilerRecorder _gcAllocated; private bool _running;

        private void OnEnable() { if (runWithGameplayScenario) GameplayScenarioRunner.ScenarioStarted += Begin; }
        private void OnDisable() { GameplayScenarioRunner.ScenarioStarted -= Begin; DisposeRecorders(); }
        public void Begin(string scenarioId) { if (!_running) StartCoroutine(Measure(scenarioId)); }

        private IEnumerator Measure(string scenarioId)
        {
            _running = true; Clear(); string started = DateTime.UtcNow.ToString("O");
            TryRecorder(ref _mainThread, ProfilerCategory.Internal, "Main Thread", 128);
            TryRecorder(ref _gcAllocated, ProfilerCategory.Memory, "GC Allocated In Frame", 128);
            for (int i = 0; i < Mathf.Max(0, warmupFrames); i++) yield return null;
            for (int i = 0; i < Mathf.Max(1, measurementFrames); i++)
            {
                FrameTimingManager.CaptureFrameTimings(); yield return null;
                _frame.Add(Time.unscaledDeltaTime * 1000.0);
                if (_mainThread.Valid) _cpu.Add(_mainThread.LastValue / 1000000.0);
                if (_gcAllocated.Valid) _gc.Add(_gcAllocated.LastValue);
                _memory.Add(Profiler.GetTotalAllocatedMemoryLong());
                var timings = new FrameTiming[1]; uint count = FrameTimingManager.GetLatestTimings(1, timings);
                if (count > 0 && timings[0].gpuFrameTime > 0) _gpu.Add(timings[0].gpuFrameTime);
                SampleCustom();
            }
            var result = Build(scenarioId, started); string path = Write(result);
            Debug.Log((result.verdict == "passed" ? "UAP_PERFORMANCE_PASS " : "UAP_PERFORMANCE_FAIL ") + path, this);
            DisposeRecorders(); _running = false;
        }

        private PerformanceBudgetResult Build(string scenarioId, string started)
        {
            var metrics = new List<PerformanceMetric>
            {
                Metric("frameTime", "ms", _frame, budget.frameP95Ms, budget.frameP50Ms, budget.frameP99Ms),
                Metric("cpuMainThread", "ms", _cpu, budget.cpuP95Ms),
                Metric("gpuFrame", "ms", _gpu, budget.gpuP95Ms),
                Metric("gcAllocatedPerFrame", "bytes", _gc, budget.gcBytesPerFrameP95),
                Metric("totalAllocatedMemory", "bytes", _memory, budget.totalAllocatedMemoryBytes)
            };
            foreach (var pair in _custom) metrics.Add(Metric(pair.Key, "custom", pair.Value, 0));
            return new PerformanceBudgetResult { scenarioId = scenarioId, verdict = metrics.All(value => value.passed) ? "passed" : "failed", startedUtc = started, finishedUtc = DateTime.UtcNow.ToString("O"), platform = Application.platform.ToString(), unityVersion = Application.unityVersion, qualityLevel = QualitySettings.names[QualitySettings.GetQualityLevel()], warmupFrames = warmupFrames, measuredFrames = _frame.Count, metrics = metrics.ToArray() };
        }

        private static PerformanceMetric Metric(string name, string unit, List<double> values, double p95Budget, double p50Budget = 0, double p99Budget = 0)
        {
            var sorted = values.Where(value => value >= 0).OrderBy(value => value).ToArray();
            double p50 = Percentile(sorted, .50), p95 = Percentile(sorted, .95), p99 = Percentile(sorted, .99), maximum = sorted.Length == 0 ? 0 : sorted[sorted.Length - 1];
            bool available = sorted.Length > 0;
            bool passed = (!available && p95Budget <= 0 && p50Budget <= 0 && p99Budget <= 0) || (available && (p95Budget <= 0 || p95 <= p95Budget) && (p50Budget <= 0 || p50 <= p50Budget) && (p99Budget <= 0 || p99 <= p99Budget));
            return new PerformanceMetric { name = name, unit = unit, available = available, p50 = p50, p95 = p95, p99 = p99, maximum = maximum, budget = p95Budget, passed = passed };
        }
        private static double Percentile(double[] values, double fraction) { if (values.Length == 0) return 0; int index = Mathf.Clamp(Mathf.CeilToInt((float)(values.Length * fraction)) - 1, 0, values.Length - 1); return values[index]; }
        private void SampleCustom()
        {
            foreach (var behaviour in customMetricSources ?? Array.Empty<MonoBehaviour>())
            {
                var source = behaviour as IPerformanceMetricSource; if (source == null) continue; var values = new Dictionary<string, double>(); source.Sample(values);
                foreach (var pair in values) { string key = source.SourceId + "." + pair.Key; if (!_custom.TryGetValue(key, out var list)) _custom[key] = list = new List<double>(); list.Add(pair.Value); }
            }
        }
        private static void TryRecorder(ref ProfilerRecorder recorder, ProfilerCategory category, string name, int capacity) { try { recorder = ProfilerRecorder.StartNew(category, name, capacity); } catch (Exception) { recorder = default; } }
        private void DisposeRecorders() { if (_mainThread.Valid) _mainThread.Dispose(); if (_gcAllocated.Valid) _gcAllocated.Dispose(); }
        private void Clear() { _frame.Clear(); _cpu.Clear(); _gpu.Clear(); _gc.Clear(); _memory.Clear(); _custom.Clear(); }
        private static string Write(PerformanceBudgetResult result) { string directory = Path.Combine(Application.persistentDataPath, "UnityArchitectPro", "Performance"); Directory.CreateDirectory(directory); string path = Path.Combine(directory, Safe(result.scenarioId) + "-performance-result.json"); File.WriteAllText(path, JsonUtility.ToJson(result, true)); return path; }
        private static string Safe(string value) { if (string.IsNullOrEmpty(value)) return "capture"; foreach (char invalid in Path.GetInvalidFileNameChars()) value = value.Replace(invalid, '_'); return value; }
    }
}
