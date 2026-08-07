#if UNITY_EDITOR
using System;
using System.Globalization;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

namespace UnityArchitectPro.EditorTools
{
    public static class SerializedPropertyValue
    {
        public static string Format(SerializedProperty property)
        {
            switch (property.propertyType)
            {
                case SerializedPropertyType.Integer: return property.longValue.ToString(CultureInfo.InvariantCulture);
                case SerializedPropertyType.Boolean: return property.boolValue.ToString();
                case SerializedPropertyType.Float: return property.doubleValue.ToString("R", CultureInfo.InvariantCulture);
                case SerializedPropertyType.String: return property.stringValue;
                case SerializedPropertyType.Enum: return property.enumValueIndex + ":" + property.enumDisplayNames[property.enumValueIndex];
                case SerializedPropertyType.ObjectReference: return property.objectReferenceValue ? GlobalObjectId.GetGlobalObjectIdSlow(property.objectReferenceValue).ToString() : "null";
                case SerializedPropertyType.Color: return property.colorValue.ToString();
                case SerializedPropertyType.Vector2: return property.vector2Value.ToString();
                case SerializedPropertyType.Vector3: return property.vector3Value.ToString();
                case SerializedPropertyType.Vector4: return property.vector4Value.ToString();
                default: return property.propertyType.ToString();
            }
        }
    }

    /// <summary>Optimistic, Undo-backed mutation of a single safe SerializedProperty from a Temp JSON request.</summary>
    public static class SerializedPropertyMutation
    {
        [Serializable] private sealed class Request
        {
            public int schemaVersion = 1;
            public string targetGlobalObjectId;
            public string propertyPath;
            public string expectedValue;
            public string value;
            public string objectReferenceAssetPath;
            public bool allowProjectSettings;
        }

        [MenuItem("Tools/Unity Architect Pro/Live Inspector/Apply Serialized Property Request")]
        public static void ApplyRequest()
        {
            var requestPath = Path.Combine("Temp", "UnityArchitectPro", "property-mutation-request.json");
            if (!File.Exists(requestPath)) throw new FileNotFoundException("Create a mutation request first.", requestPath);
            var request = JsonUtility.FromJson<Request>(File.ReadAllText(requestPath));
            if (request == null || request.schemaVersion != 1) throw new InvalidOperationException("Unsupported mutation request schema.");
            if (!GlobalObjectId.TryParse(request.targetGlobalObjectId, out var id)) throw new InvalidOperationException("Invalid targetGlobalObjectId.");
            var target = GlobalObjectId.GlobalObjectIdentifierToObjectSlow(id);
            if (!target) throw new InvalidOperationException("Target no longer resolves; recapture before retrying.");

            var assetPath = AssetDatabase.GetAssetPath(target);
            if (assetPath.StartsWith("ProjectSettings/", StringComparison.OrdinalIgnoreCase) && !request.allowProjectSettings)
                throw new InvalidOperationException("ProjectSettings mutation requires allowProjectSettings=true and explicit review.");

            var serialized = new SerializedObject(target);
            serialized.UpdateIfRequiredOrScript();
            var property = serialized.FindProperty(request.propertyPath);
            if (property == null) throw new InvalidOperationException("Property path was not found.");
            if (!IsSafeProperty(property)) throw new InvalidOperationException("Property type/path is blocked from automated mutation.");
            var before = SerializedPropertyValue.Format(property);
            if (!string.Equals(before, request.expectedValue, StringComparison.Ordinal))
                throw new InvalidOperationException("Stale request: expected '" + request.expectedValue + "' but found '" + before + "'.");

            Undo.RecordObject(target, "Unity Architect Pro serialized property change");
            SetValue(property, request);
            if (!serialized.ApplyModifiedProperties()) throw new InvalidOperationException("Unity reported no serialized change.");
            EditorUtility.SetDirty(target);
            if (target is Component component && component.gameObject.scene.IsValid()) EditorSceneManager.MarkSceneDirty(component.gameObject.scene);
            AssetDatabase.SaveAssets();

            serialized.UpdateIfRequiredOrScript();
            var after = SerializedPropertyValue.Format(serialized.FindProperty(request.propertyPath));
            Debug.Log("[UnityArchitectPro] Serialized property changed: " + target.name + "." + request.propertyPath + " '" + before + "' -> '" + after + "'. Undo is available.");
        }

        public static bool IsSafeProperty(SerializedProperty property)
        {
            if (property == null || property.propertyPath == "m_Script" || property.propertyPath.Contains("managedReferences") || property.isArray) return false;
            switch (property.propertyType)
            {
                case SerializedPropertyType.Integer:
                case SerializedPropertyType.Boolean:
                case SerializedPropertyType.Float:
                case SerializedPropertyType.String:
                case SerializedPropertyType.Enum:
                case SerializedPropertyType.Color:
                case SerializedPropertyType.Vector2:
                case SerializedPropertyType.Vector3:
                case SerializedPropertyType.Vector4:
                case SerializedPropertyType.ObjectReference:
                    return true;
                default: return false;
            }
        }

        private static void SetValue(SerializedProperty property, Request request)
        {
            switch (property.propertyType)
            {
                case SerializedPropertyType.Integer: property.longValue = long.Parse(request.value, CultureInfo.InvariantCulture); break;
                case SerializedPropertyType.Boolean: property.boolValue = bool.Parse(request.value); break;
                case SerializedPropertyType.Float: property.doubleValue = double.Parse(request.value, CultureInfo.InvariantCulture); break;
                case SerializedPropertyType.String: property.stringValue = request.value ?? string.Empty; break;
                case SerializedPropertyType.Enum:
                    var enumIndex = int.Parse(request.value, CultureInfo.InvariantCulture);
                    if (enumIndex < 0 || enumIndex >= property.enumDisplayNames.Length) throw new ArgumentOutOfRangeException(nameof(request.value));
                    property.enumValueIndex = enumIndex; break;
                case SerializedPropertyType.Color: property.colorValue = ParseColor(request.value); break;
                case SerializedPropertyType.Vector2: property.vector2Value = ParseVector4(request.value); break;
                case SerializedPropertyType.Vector3: property.vector3Value = ParseVector4(request.value); break;
                case SerializedPropertyType.Vector4: property.vector4Value = ParseVector4(request.value); break;
                case SerializedPropertyType.ObjectReference:
                    property.objectReferenceValue = string.IsNullOrEmpty(request.objectReferenceAssetPath) ? null : AssetDatabase.LoadMainAssetAtPath(request.objectReferenceAssetPath);
                    if (!string.IsNullOrEmpty(request.objectReferenceAssetPath) && !property.objectReferenceValue) throw new InvalidOperationException("Object reference asset was not found.");
                    break;
                default: throw new NotSupportedException(property.propertyType.ToString());
            }
        }

        private static Vector4 ParseVector4(string text)
        {
            var values = text.Split(',');
            if (values.Length < 2 || values.Length > 4) throw new FormatException("Vector values use comma-separated invariant numbers.");
            var result = Vector4.zero;
            for (var i = 0; i < values.Length; i++) result[i] = float.Parse(values[i], CultureInfo.InvariantCulture);
            return result;
        }

        private static Color ParseColor(string text)
        {
            var v = ParseVector4(text);
            return new Color(v.x, v.y, v.z, v.w);
        }
    }
}
#endif
