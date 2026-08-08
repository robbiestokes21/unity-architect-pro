#if UNITY_EDITOR
using System;
using System.IO;
using UnityEditor;
using UnityEngine;

namespace UnityArchitectPro.Runtime.Editor
{
    public sealed class RuntimeDebuggerWindow : EditorWindow
    {
        private Vector2 _scroll;
        private string _json = "Enter Play Mode and select an object.";

        [MenuItem("Tools/Unity Architect Pro/Runtime Debugger")]
        public static void Open() { GetWindow<RuntimeDebuggerWindow>("UAP Runtime Debugger"); }

        private void OnGUI()
        {
            EditorGUILayout.HelpBox("Read-only capture. Add RuntimeStateProbe to a runtime object; adapters can implement the Phase 6 diagnostic interfaces.", MessageType.Info);
            using (new EditorGUI.DisabledScope(!EditorApplication.isPlaying || Selection.activeGameObject == null))
            {
                if (GUILayout.Button("Capture Selected Runtime Object")) CaptureSelection();
            }
            if (GUILayout.Button("Export Current Capture")) Export();
            _scroll = EditorGUILayout.BeginScrollView(_scroll);
            EditorGUILayout.TextArea(_json, GUILayout.ExpandHeight(true));
            EditorGUILayout.EndScrollView();
        }

        private void CaptureSelection()
        {
            var selected = Selection.activeGameObject;
            var probe = selected ? selected.GetComponent<RuntimeStateProbe>() : null;
            if (!probe) { _json = "Selected runtime object has no RuntimeStateProbe."; return; }
            try { _json = JsonUtility.ToJson(probe.Capture(), true); }
            catch (Exception ex) { _json = "Capture failed: " + ex; }
            Repaint();
        }

        private void Export()
        {
            var directory = Path.Combine("Temp", "UnityArchitectPro");
            Directory.CreateDirectory(directory);
            var path = Path.Combine(directory, "runtime-debugger-selection.json");
            File.WriteAllText(path, _json ?? string.Empty);
            Debug.Log("[UnityArchitectPro] Runtime debugger capture: " + Path.GetFullPath(path));
        }
    }
}
#endif
