#if UNITY_EDITOR
using System;
using UnityEditor;
using UnityEngine;

namespace UnityArchitectPro.GameplayTesting.Editor
{
    public static class GameplayScenarioValidator
    {
        [MenuItem("Tools/Unity Architect Pro/Validate Gameplay Scenario")]
        public static void ValidateSelection()
        {
            var text = Selection.activeObject as TextAsset;
            if (!text) throw new InvalidOperationException("Select a gameplay scenario JSON TextAsset.");
            var scenario = JsonUtility.FromJson<GameplayScenario>(text.text);
            if (scenario == null || scenario.schemaVersion != 1 || scenario.steps == null || scenario.steps.Length == 0) throw new InvalidOperationException("Invalid or empty gameplay scenario.");
            var ids = new System.Collections.Generic.HashSet<string>();
            foreach (var step in scenario.steps)
            {
                if (step == null || string.IsNullOrEmpty(step.id) || !ids.Add(step.id)) throw new InvalidOperationException("Step IDs must be non-empty and unique.");
                if (step.action == null || string.IsNullOrEmpty(step.action.kind)) throw new InvalidOperationException("Step " + step.id + " has no action kind.");
            }
            Debug.Log("[UnityArchitectPro] Gameplay scenario valid: " + scenario.name + " (" + scenario.steps.Length + " steps)", text);
        }
    }
}
#endif
