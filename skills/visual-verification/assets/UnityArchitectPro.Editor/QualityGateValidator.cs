#if UNITY_EDITOR
using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityArchitectPro.Performance;

namespace UnityArchitectPro.VisualQa.Editor
{
    public static class QualityGateValidator
    {
        [MenuItem("Tools/Unity Architect Pro/Validate Visual and Performance Gates")]
        public static void ValidateScene()
        {
            var errors = new List<string>();
            foreach (var runner in UnityEngine.Object.FindObjectsOfType<VisualQaRunner>(true)) ValidateVisual(runner, errors);
            foreach (var probe in UnityEngine.Object.FindObjectsOfType<PerformanceBudgetProbe>(true)) ValidatePerformance(probe, errors);
            if (errors.Count > 0) throw new InvalidOperationException(string.Join("\n", errors));
            Debug.Log("[UnityArchitectPro] Visual and performance gate configuration is valid.");
        }

        private static void ValidateVisual(VisualQaRunner runner, ICollection<string> errors)
        {
            var serialized = new SerializedObject(runner); var cases = serialized.FindProperty("cases"); var ids = new HashSet<string>();
            if (cases == null || cases.arraySize == 0) { errors.Add(runner.name + ": no visual capture cases."); return; }
            for (int i = 0; i < cases.arraySize; i++)
            {
                var item = cases.GetArrayElementAtIndex(i); string prefix = runner.name + ".cases[" + i + "]"; string id = item.FindPropertyRelative("id").stringValue;
                if (string.IsNullOrEmpty(id) || !ids.Add(id)) errors.Add(prefix + ": ID must be non-empty and unique.");
                if (!item.FindPropertyRelative("camera").objectReferenceValue) errors.Add(prefix + ": camera is required.");
                var baseline = item.FindPropertyRelative("baseline").objectReferenceValue as Texture2D;
                if (!baseline) errors.Add(prefix + ": approved baseline is required."); else ValidateReadable(baseline, prefix + ".baseline", errors);
                var mask = item.FindPropertyRelative("ignoreMask").objectReferenceValue as Texture2D; if (mask) ValidateReadable(mask, prefix + ".ignoreMask", errors);
                if (item.FindPropertyRelative("width").intValue <= 0 || item.FindPropertyRelative("height").intValue <= 0) errors.Add(prefix + ": dimensions must be positive.");
            }
        }

        private static void ValidatePerformance(PerformanceBudgetProbe probe, ICollection<string> errors)
        {
            var serialized = new SerializedObject(probe);
            if (serialized.FindProperty("warmupFrames").intValue < 0) errors.Add(probe.name + ": warmup frames cannot be negative.");
            if (serialized.FindProperty("measurementFrames").intValue <= 0) errors.Add(probe.name + ": measurement frames must be positive.");
        }

        private static void ValidateReadable(Texture2D texture, string label, ICollection<string> errors)
        {
            string path = AssetDatabase.GetAssetPath(texture); var importer = AssetImporter.GetAtPath(path) as TextureImporter;
            if (importer != null && !importer.isReadable) errors.Add(label + ": texture Read/Write must be enabled for comparison.");
        }
    }
}
#endif
