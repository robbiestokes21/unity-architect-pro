using System;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace UnityArchitectPro.Runtime
{
    /// <summary>Development-only, bounded runtime snapshot probe. Remove before shipping unless intentionally adopted.</summary>
    [DisallowMultipleComponent]
    public sealed class RuntimeStateProbe : MonoBehaviour
    {
        [Serializable] public sealed class Snapshot
        {
            public int schemaVersion = 1;
            public string utc;
            public int frame;
            public string scene;
            public string hierarchyPath;
            public string objectName;
            public int instanceId;
            public bool active;
            public string position;
            public string rotation;
            public string scale;
            public string physics;
            public string animator;
            public string[] stateDiagnostics;
            public string[] networkDiagnostics;
            public RuntimeOperationSnapshot[] operations;
            public MetricSnapshot metrics;
        }

        [Serializable] public sealed class MetricSnapshot
        {
            public float unscaledTime;
            public float deltaTimeMs;
            public float smoothDeltaTimeMs;
            public float approximateFps;
            public long monoUsedBytes;
            public int loadedScenes;
            public int objectCount;
        }

        [SerializeField, Min(0.1f)] private float intervalSeconds = 1f;
        [SerializeField] private bool logToConsole = true;
        [SerializeField] private bool writeJsonLines;
        [SerializeField, Range(1, 1000)] private int maximumOperations = 100;
        private float _nextCapture;
        public Snapshot Latest { get; private set; }

        private void Update()
        {
            if (Time.unscaledTime < _nextCapture) return;
            _nextCapture = Time.unscaledTime + Mathf.Max(0.1f, intervalSeconds);
            Latest = Capture();
            var json = JsonUtility.ToJson(Latest);
            if (logToConsole) Debug.Log("[UAP-RUNTIME] " + json, this);
            if (writeJsonLines) AppendJsonLine(json);
        }

        public Snapshot Capture()
        {
            return new Snapshot
            {
                utc = DateTime.UtcNow.ToString("O"), frame = Time.frameCount, scene = gameObject.scene.name,
                hierarchyPath = HierarchyPath(transform), objectName = name, instanceId = GetInstanceID(),
                active = isActiveAndEnabled, position = transform.position.ToString("R"), rotation = transform.rotation.eulerAngles.ToString("R"), scale = transform.lossyScale.ToString("R"),
                physics = CapturePhysics(), animator = CaptureAnimator(), stateDiagnostics = CaptureStates(), networkDiagnostics = CaptureNetwork(),
                operations = RuntimeOperationRegistry.Snapshot(maximumOperations), metrics = CaptureMetrics()
            };
        }

        private string CapturePhysics()
        {
            var body = GetComponent<Rigidbody>();
            if (body) return "3D velocity=" + body.velocity.ToString("R") + ";angular=" + body.angularVelocity.ToString("R") + ";sleeping=" + body.IsSleeping();
            var body2D = GetComponent<Rigidbody2D>();
            if (body2D) return "2D velocity=" + body2D.velocity.ToString("R") + ";angular=" + body2D.angularVelocity + ";sleeping=" + body2D.IsSleeping();
            return "none";
        }

        private string CaptureAnimator()
        {
            var animator = GetComponent<Animator>();
            if (!animator) return "none";
            var parts = new List<string>();
            for (var layer = 0; layer < animator.layerCount; layer++)
            {
                var state = animator.GetCurrentAnimatorStateInfo(layer);
                parts.Add("layer=" + layer + ";stateHash=" + state.fullPathHash + ";normalized=" + state.normalizedTime.ToString("R") + ";transition=" + animator.IsInTransition(layer));
            }
            foreach (var parameter in animator.parameters)
            {
                switch (parameter.type)
                {
                    case AnimatorControllerParameterType.Bool: parts.Add(parameter.name + "=" + animator.GetBool(parameter.name)); break;
                    case AnimatorControllerParameterType.Float: parts.Add(parameter.name + "=" + animator.GetFloat(parameter.name).ToString("R")); break;
                    case AnimatorControllerParameterType.Int: parts.Add(parameter.name + "=" + animator.GetInteger(parameter.name)); break;
                    case AnimatorControllerParameterType.Trigger: parts.Add(parameter.name + "=<trigger>"); break;
                }
            }
            return string.Join("|", parts);
        }

        private string[] CaptureStates()
        {
            var result = new List<string>();
            foreach (var behaviour in GetComponents<MonoBehaviour>())
            {
                var source = behaviour as IRuntimeStateDiagnostics;
                if (source == null) continue;
                var values = new Dictionary<string, string>();
                try { source.AppendDiagnosticValues(values); result.Add(source.DiagnosticSystem + ":" + source.DiagnosticState + FormatValues(values)); }
                catch (Exception ex) { result.Add(behaviour.GetType().FullName + ":error=" + ex.GetType().Name); }
            }
            return result.ToArray();
        }

        private string[] CaptureNetwork()
        {
            var result = new List<string>();
            foreach (var behaviour in GetComponents<MonoBehaviour>())
            {
                var source = behaviour as IRuntimeNetworkDiagnostics;
                if (source == null) continue;
                var values = new Dictionary<string, string>();
                try
                {
                    source.AppendNetworkValues(values);
                    result.Add(source.NetworkProvider + ":object=" + source.NetworkObjectId + ";owner=" + source.NetworkOwnerId + ";spawned=" + source.IsSpawned + ";authority=" + source.HasLocalAuthority + FormatValues(values));
                }
                catch (Exception ex) { result.Add(behaviour.GetType().FullName + ":error=" + ex.GetType().Name); }
            }
            return result.ToArray();
        }

        private MetricSnapshot CaptureMetrics()
        {
            return new MetricSnapshot
            {
                unscaledTime = Time.unscaledTime, deltaTimeMs = Time.unscaledDeltaTime * 1000f, smoothDeltaTimeMs = Time.smoothDeltaTime * 1000f,
                approximateFps = Time.unscaledDeltaTime > 0f ? 1f / Time.unscaledDeltaTime : 0f,
                monoUsedBytes = UnityEngine.Profiling.Profiler.GetMonoUsedSizeLong(), loadedScenes = SceneManager.sceneCount,
                objectCount = FindObjectsOfType<GameObject>().Length
            };
        }

        private void AppendJsonLine(string json)
        {
            var directory = Path.Combine(Application.persistentDataPath, "UnityArchitectPro");
            Directory.CreateDirectory(directory);
            File.AppendAllText(Path.Combine(directory, "runtime-diagnostics.jsonl"), json + Environment.NewLine);
        }

        private static string HierarchyPath(Transform current)
        {
            var path = current.name;
            while (current.parent) { current = current.parent; path = current.name + "/" + path; }
            return path;
        }

        private static string FormatValues(Dictionary<string, string> values)
        {
            var keys = new List<string>(values.Keys); keys.Sort(StringComparer.Ordinal);
            var result = string.Empty;
            foreach (var key in keys) result += ";" + key + "=" + values[key];
            return result;
        }
    }
}
