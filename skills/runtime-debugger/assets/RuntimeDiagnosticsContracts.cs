using System;
using System.Collections.Generic;

namespace UnityArchitectPro.Runtime
{
    /// <summary>Implement on an FSM, behavior tree, planner, or other stateful system to expose safe diagnostics.</summary>
    public interface IRuntimeStateDiagnostics
    {
        string DiagnosticSystem { get; }
        string DiagnosticState { get; }
        void AppendDiagnosticValues(IDictionary<string, string> values);
    }

    /// <summary>Package-neutral adapter for NGO, Netcode for Entities, Mirror, FishNet, Fusion, or custom networking.</summary>
    public interface IRuntimeNetworkDiagnostics
    {
        string NetworkProvider { get; }
        string NetworkObjectId { get; }
        string NetworkOwnerId { get; }
        bool IsSpawned { get; }
        bool HasLocalAuthority { get; }
        void AppendNetworkValues(IDictionary<string, string> values);
    }

    [Serializable]
    public sealed class RuntimeOperationSnapshot
    {
        public string id;
        public string kind;
        public string owner;
        public string state;
        public string startedUtc;
        public string updatedUtc;
        public string detail;
    }

    /// <summary>
    /// Explicit registry for tasks, coroutines, jobs, requests, and other asynchronous operations.
    /// Unity does not expose a safe general coroutine enumerator, so systems opt in at lifecycle boundaries.
    /// </summary>
    public static class RuntimeOperationRegistry
    {
        private static readonly object Gate = new object();
        private static readonly Dictionary<string, RuntimeOperationSnapshot> Operations = new Dictionary<string, RuntimeOperationSnapshot>();

        public static string Begin(string kind, string owner, string detail = null, string id = null)
        {
            id = string.IsNullOrEmpty(id) ? Guid.NewGuid().ToString("N") : id;
            var now = DateTime.UtcNow.ToString("O");
            lock (Gate)
            {
                Operations[id] = new RuntimeOperationSnapshot { id = id, kind = kind ?? "operation", owner = owner ?? string.Empty, state = "running", detail = detail ?? string.Empty, startedUtc = now, updatedUtc = now };
            }
            return id;
        }

        public static void Update(string id, string state, string detail = null)
        {
            if (string.IsNullOrEmpty(id)) return;
            lock (Gate)
            {
                RuntimeOperationSnapshot operation;
                if (!Operations.TryGetValue(id, out operation)) return;
                operation.state = state ?? operation.state;
                operation.detail = detail ?? operation.detail;
                operation.updatedUtc = DateTime.UtcNow.ToString("O");
            }
        }

        public static void Complete(string id, string detail = null) { Update(id, "completed", detail); }
        public static void Fail(string id, Exception error) { Update(id, "failed", error == null ? string.Empty : error.GetType().Name + ": " + error.Message); }
        public static void Cancel(string id, string detail = null) { Update(id, "cancelled", detail); }

        public static RuntimeOperationSnapshot[] Snapshot(int maximum = 100)
        {
            maximum = Math.Max(1, Math.Min(maximum, 1000));
            lock (Gate)
            {
                var result = new List<RuntimeOperationSnapshot>(Operations.Values);
                result.Sort((a, b) => string.CompareOrdinal(b.updatedUtc, a.updatedUtc));
                if (result.Count > maximum) result.RemoveRange(maximum, result.Count - maximum);
                return result.ToArray();
            }
        }

        public static void PruneTerminal()
        {
            lock (Gate)
            {
                var remove = new List<string>();
                foreach (var pair in Operations)
                    if (pair.Value.state != "running") remove.Add(pair.Key);
                foreach (var id in remove) Operations.Remove(id);
            }
        }

        public static void Clear() { lock (Gate) Operations.Clear(); }
    }
}
