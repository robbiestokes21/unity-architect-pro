#if UNITY_EDITOR
using System;
using System.Collections.Generic;
using System.IO;
using UnityEditor;
using UnityEditor.Animations;
using UnityEditor.PackageManager;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.SceneManagement;

namespace UnityArchitectPro.EditorTools
{
    /// <summary>Package-optional, read-only project/scene inspector. Writes evidence under Temp/UnityArchitectPro.</summary>
    public static class LiveUnityInspector
    {
        [Serializable] private sealed class Report
        {
            public int schemaVersion = 1;
            public string unityVersion;
            public string utc;
            public string activeScene;
            public List<Entry> hierarchy = new();
            public List<Entry> cameras = new();
            public List<Entry> animators = new();
            public List<Entry> lighting = new();
            public List<Entry> packages = new();
            public List<Entry> settings = new();
            public List<Entry> assets = new();
        }

        [Serializable] private sealed class Entry
        {
            public string category;
            public string path;
            public string type;
            public string value;
            public List<Property> properties = new();
        }

        [Serializable] private sealed class Property
        {
            public string path;
            public string displayName;
            public string propertyType;
            public string value;
            public bool editable;
        }

        [MenuItem("Tools/Unity Architect Pro/Live Inspector/Capture Full Report")]
        public static void CaptureFullReport()
        {
            var report = new Report
            {
                unityVersion = Application.unityVersion,
                utc = DateTime.UtcNow.ToString("O"),
                activeScene = SceneManager.GetActiveScene().path
            };

            CaptureHierarchy(report);
            CapturePackages(report);
            CaptureGlobalSettings(report);
            CaptureAssets(report);
            WriteReport("live-inspector.json", report);
        }

        [MenuItem("Tools/Unity Architect Pro/Live Inspector/Inspect Selection")]
        public static void InspectSelection()
        {
            if (!Selection.activeObject)
            {
                Debug.LogError("[UnityArchitectPro] Select a scene object, component, or asset first.");
                return;
            }

            var report = new Report { unityVersion = Application.unityVersion, utc = DateTime.UtcNow.ToString("O") };
            report.assets.Add(InspectObject("selection", AssetDatabase.GetAssetPath(Selection.activeObject), Selection.activeObject));
            WriteReport("selection-inspector.json", report);
        }

        private static void CaptureHierarchy(Report report)
        {
            for (var sceneIndex = 0; sceneIndex < SceneManager.sceneCount; sceneIndex++)
            {
                var scene = SceneManager.GetSceneAt(sceneIndex);
                if (!scene.isLoaded) continue;
                foreach (var root in scene.GetRootGameObjects()) Visit(root, scene.path, root.name, report);
            }
        }

        private static void Visit(GameObject go, string scenePath, string hierarchyPath, Report report)
        {
            var node = InspectObject("hierarchy", scenePath + "::" + hierarchyPath, go);
            node.value = $"activeSelf={go.activeSelf};activeInHierarchy={go.activeInHierarchy};tag={go.tag};layer={LayerMask.LayerToName(go.layer)}({go.layer});sibling={go.transform.GetSiblingIndex()};prefab={PrefabUtility.GetPrefabInstanceStatus(go)}";
            report.hierarchy.Add(node);

            foreach (var component in go.GetComponents<Component>())
            {
                if (!component)
                {
                    report.hierarchy.Add(new Entry { category = "missing-script", path = node.path, type = "<MissingScript>", value = "null component slot" });
                    continue;
                }
                var entry = InspectObject("component", node.path, component);
                entry.value = PrefabOverrideSummary(component);
                AppendPrefabOverrides(component, entry);
                report.hierarchy.Add(entry);
                if (component is Camera) report.cameras.Add(entry);
                if (component is Animator animator) CaptureAnimator(animator, node.path, report);
                if (component is Light || component.GetType().Name.Contains("Volume")) report.lighting.Add(entry);
            }

            for (var i = 0; i < go.transform.childCount; i++)
            {
                var child = go.transform.GetChild(i).gameObject;
                Visit(child, scenePath, hierarchyPath + "/" + child.name, report);
            }
        }

        private static string PrefabOverrideSummary(Component component)
        {
            if (!PrefabUtility.IsPartOfPrefabInstance(component)) return "not-prefab-instance";
            var source = PrefabUtility.GetCorrespondingObjectFromSource(component);
            var overrides = PrefabUtility.GetPropertyModifications(component);
            return $"source={AssetDatabase.GetAssetPath(source)};overrides={(overrides == null ? 0 : overrides.Length)}";
        }

        private static void AppendPrefabOverrides(Component component, Entry entry)
        {
            var overrides = PrefabUtility.GetPropertyModifications(component);
            if (overrides == null) return;
            foreach (var modification in overrides)
            {
                entry.properties.Add(new Property
                {
                    path = modification.propertyPath,
                    displayName = "prefab override",
                    propertyType = modification.objectReference ? "ObjectReference" : "String",
                    value = modification.objectReference ? AssetDatabase.GetAssetPath(modification.objectReference) : modification.value,
                    editable = false
                });
            }
        }

        private static void CaptureAnimator(Animator animator, string path, Report report)
        {
            var controller = animator.runtimeAnimatorController as AnimatorController;
            var entry = new Entry { category = "animator-state-machine", path = path, type = animator.runtimeAnimatorController ? animator.runtimeAnimatorController.GetType().FullName : "null" };
            if (controller != null)
            {
                foreach (var layer in controller.layers)
                    entry.properties.Add(new Property { path = layer.name, displayName = "layer", propertyType = "AnimatorLayer", value = StateMachineSummary(layer.stateMachine), editable = false });
            }
            report.animators.Add(entry);
        }

        private static string StateMachineSummary(AnimatorStateMachine machine)
        {
            var states = new List<string>();
            foreach (var state in machine.states) states.Add(state.state.name);
            foreach (var child in machine.stateMachines) states.Add(child.stateMachine.name + "/...");
            return string.Join(",", states);
        }

        private static void CaptureGlobalSettings(Report report)
        {
            report.settings.Add(new Entry { category = "layers-tags-sorting", type = "TagManager", value = TagAndLayerSummary() });
            report.settings.Add(InspectObject("render-pipeline", "GraphicsSettings.currentRenderPipeline", GraphicsSettings.currentRenderPipeline));
            report.lighting.Add(new Entry { category = "lighting", type = "RenderSettings", value = $"ambientMode={RenderSettings.ambientMode};fog={RenderSettings.fog};skybox={AssetDatabase.GetAssetPath(RenderSettings.skybox)};lightmaps={LightmapSettings.lightmaps.Length}" });

            foreach (var path in new[] { "ProjectSettings/PhysicsManager.asset", "ProjectSettings/Physics2DSettings.asset", "ProjectSettings/GraphicsSettings.asset", "ProjectSettings/QualitySettings.asset", "ProjectSettings/ProjectSettings.asset", "ProjectSettings/TagManager.asset", "ProjectSettings/NavMeshAreas.asset", "ProjectSettings/TimeManager.asset", "ProjectSettings/AudioManager.asset" })
            {
                var objects = AssetDatabase.LoadAllAssetsAtPath(path);
                if (objects.Length > 0) report.settings.Add(InspectObject("project-settings", path, objects[0]));
            }
        }

        private static void CapturePackages(Report report)
        {
            foreach (var package in PackageInfo.GetAllRegisteredPackages())
                report.packages.Add(new Entry { category = "package", path = package.assetPath, type = package.name, value = package.version });
        }

        private static string TagAndLayerSummary()
        {
            var layers = new List<string>();
            for (var i = 0; i < 32; i++) if (!string.IsNullOrEmpty(LayerMask.LayerToName(i))) layers.Add(i + ":" + LayerMask.LayerToName(i));
            return "tags=" + string.Join(",", UnityEditorInternal.InternalEditorUtility.tags) + ";layers=" + string.Join(",", layers) + ";sortingLayers=" + string.Join(",", Array.ConvertAll(SortingLayer.layers, x => x.name));
        }

        private static void CaptureAssets(Report report)
        {
            CaptureAssetsByFilter(report, "input-system", "t:InputActionAsset");
            CaptureAssetsByFilter(report, "animator-controller", "t:AnimatorController");
            CaptureAssetsByFilter(report, "lighting-settings", "t:LightingSettings");
            CaptureAssetsByFilter(report, "render-pipeline", "t:RenderPipelineAsset");
            CaptureAssetsByFilter(report, "volume-profile", "t:VolumeProfile");
            CaptureAssetsByFilter(report, "navigation", "t:NavMeshData");
        }

        private static void CaptureAssetsByFilter(Report report, string category, string filter)
        {
            foreach (var guid in AssetDatabase.FindAssets(filter))
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                report.assets.Add(InspectObject(category, path, AssetDatabase.LoadMainAssetAtPath(path)));
            }
        }

        private static Entry InspectObject(string category, string path, UnityEngine.Object target)
        {
            var entry = new Entry { category = category, path = path ?? string.Empty, type = target ? target.GetType().FullName : "null" };
            if (!target) return entry;
            try
            {
                var serialized = new SerializedObject(target);
                var iterator = serialized.GetIterator();
                var enterChildren = true;
                while (iterator.NextVisible(enterChildren))
                {
                    enterChildren = false;
                    entry.properties.Add(new Property { path = iterator.propertyPath, displayName = iterator.displayName, propertyType = iterator.propertyType.ToString(), value = SerializedPropertyValue.Format(iterator), editable = SerializedPropertyMutation.IsSafeProperty(iterator) });
                    if (entry.properties.Count >= 500)
                    {
                        entry.value = "property output truncated at 500";
                        break;
                    }
                }
            }
            catch (Exception ex) { entry.value = "inspection-error=" + ex.GetType().Name + ":" + ex.Message; }
            return entry;
        }

        private static void WriteReport(string fileName, Report report)
        {
            var directory = Path.Combine("Temp", "UnityArchitectPro");
            Directory.CreateDirectory(directory);
            var path = Path.Combine(directory, fileName);
            File.WriteAllText(path, JsonUtility.ToJson(report, true));
            Debug.Log("[UnityArchitectPro] Live Inspector report: " + Path.GetFullPath(path));
        }
    }
}
#endif
