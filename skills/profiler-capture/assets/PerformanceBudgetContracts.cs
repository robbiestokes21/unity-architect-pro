using System;
using System.Collections.Generic;

namespace UnityArchitectPro.Performance
{
    [Serializable] public sealed class PerformanceBudget
    {
        public float frameP50Ms;
        public float frameP95Ms;
        public float frameP99Ms;
        public float cpuP95Ms;
        public float gpuP95Ms;
        public long gcBytesPerFrameP95;
        public long totalAllocatedMemoryBytes;
        public float maximumRegressionPercent = 10f;
    }
    [Serializable] public sealed class PerformanceMetric { public string name; public string unit; public bool available; public double p50; public double p95; public double p99; public double maximum; public double budget; public bool passed; }
    [Serializable] public sealed class PerformanceBudgetResult
    {
        public int schemaVersion = 1;
        public string scenarioId;
        public string verdict;
        public string startedUtc;
        public string finishedUtc;
        public string platform;
        public string unityVersion;
        public string qualityLevel;
        public int warmupFrames;
        public int measuredFrames;
        public PerformanceMetric[] metrics;
        public string failure;
    }
    public interface IPerformanceMetricSource
    {
        string SourceId { get; }
        void Sample(IDictionary<string, double> values);
    }
}
