using System;
using System.Collections.Generic;
using Unity.Profiling;
using UnityEngine;

namespace UnityArchitectPro.RuntimeDiagnostics
{
    /// <summary>Development-only example. Verify counter availability against the project's Unity version before installation.</summary>
    public sealed class RuntimePerformanceProbe : MonoBehaviour
    {
        private readonly List<ProfilerRecorder> _recorders = new();
        [SerializeField] private float reportEverySeconds = 5f;
        private float _nextReport;

        private void OnEnable()
        {
            TryAdd(ProfilerCategory.Memory, "GC Reserved Memory");
            TryAdd(ProfilerCategory.Memory, "System Used Memory");
            TryAdd(ProfilerCategory.Scripts, "GC Allocated In Frame");
            _nextReport = Time.unscaledTime + reportEverySeconds;
        }

        private void Update()
        {
            if (Time.unscaledTime < _nextReport) return;
            _nextReport = Time.unscaledTime + reportEverySeconds;
            foreach (var recorder in _recorders)
                if (recorder.Valid) Debug.Log($"[UAP-METRIC] {recorder.CurrentValue}");
        }

        private void TryAdd(ProfilerCategory category, string stat)
        {
            try { var r = ProfilerRecorder.StartNew(category, stat, 128); if (r.Valid) _recorders.Add(r); else r.Dispose(); }
            catch (Exception e) { Debug.LogWarning($"[UnityArchitectPro] Profiler counter unavailable: {stat}: {e.Message}"); }
        }

        private void OnDisable()
        {
            foreach (var recorder in _recorders) recorder.Dispose();
            _recorders.Clear();
        }
    }
}
