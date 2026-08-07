#if UNITY_EDITOR
using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace UnityArchitectPro.EditorTools
{
    public static class HierarchySnapshot
    {
        [Serializable] private sealed class Snapshot { public string unityVersion; public string utc; public List<SceneInfo> scenes = new(); }
        [Serializable] private sealed class SceneInfo { public string name; public string path; public bool loaded; public List<Node> roots = new(); }
        [Serializable] private sealed class Node { public string name; public string hierarchyPath; public bool activeSelf; public bool activeInHierarchy; public string tag; public int layer; public List<string> components = new(); public List<Node> children = new(); }

        [MenuItem("Tools/Unity Architect Pro/Capture Hierarchy Snapshot")]
        public static void Capture()
        {
            var snapshot = new Snapshot { unityVersion = Application.unityVersion, utc = DateTime.UtcNow.ToString("O") };
            for (var i = 0; i < SceneManager.sceneCount; i++)
            {
                var scene = SceneManager.GetSceneAt(i);
                var info = new SceneInfo { name = scene.name, path = scene.path, loaded = scene.isLoaded };
                if (scene.isLoaded)
                    foreach (var root in scene.GetRootGameObjects()) info.roots.Add(ReadNode(root, root.name));
                snapshot.scenes.Add(info);
            }
            var output = Path.Combine("Temp", "UnityArchitectPro", "hierarchy.json");
            Directory.CreateDirectory(Path.GetDirectoryName(output)!);
            File.WriteAllText(output, JsonUtility.ToJson(snapshot, true));
            Debug.Log($"[UnityArchitectPro] Hierarchy snapshot: {Path.GetFullPath(output)}");
        }

        private static Node ReadNode(GameObject go, string path)
        {
            var node = new Node { name = go.name, hierarchyPath = path, activeSelf = go.activeSelf, activeInHierarchy = go.activeInHierarchy, tag = go.tag, layer = go.layer };
            foreach (var c in go.GetComponents<Component>()) node.components.Add(c ? c.GetType().FullName : "<MissingScript>");
            for (var i = 0; i < go.transform.childCount; i++)
            {
                var child = go.transform.GetChild(i).gameObject;
                node.children.Add(ReadNode(child, path + "/" + child.name));
            }
            return node;
        }
    }
}
#endif
