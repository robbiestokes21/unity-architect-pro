using System;
using System.Collections;
using System.IO;
using UnityEngine;
using UnityArchitectPro.GameplayTesting;

namespace UnityArchitectPro.VisualQa
{
    [DisallowMultipleComponent]
    public sealed class VisualQaRunner : MonoBehaviour
    {
        [SerializeField] private VisualCaptureCase[] cases;
        [SerializeField] private bool captureOnGameplayCheckpoints = true;

        private void OnEnable() { if (captureOnGameplayCheckpoints) GameplayScenarioRunner.StepCompleted += OnCheckpoint; }
        private void OnDisable() { GameplayScenarioRunner.StepCompleted -= OnCheckpoint; }
        private void OnCheckpoint(string checkpointId)
        {
            foreach (var item in cases ?? Array.Empty<VisualCaptureCase>()) if (item != null && item.checkpointId == checkpointId) StartCoroutine(Capture(item));
        }

        public void CaptureCase(string caseId)
        {
            foreach (var item in cases ?? Array.Empty<VisualCaptureCase>()) if (item != null && item.id == caseId) { StartCoroutine(Capture(item)); return; }
            Debug.LogError("[UAP-VISUAL] Unknown capture case: " + caseId, this);
        }

        private IEnumerator Capture(VisualCaptureCase item)
        {
            yield return new WaitForEndOfFrame();
            var result = NewResult(item); Texture2D current = null; Texture2D heatmap = null; RenderTexture target = null;
            try
            {
                if (!item.camera) throw new InvalidOperationException("Capture camera is missing.");
                if (!item.baseline) throw new InvalidOperationException("Approved baseline is missing.");
                if (item.width <= 0 || item.height <= 0) throw new InvalidOperationException("Capture dimensions must be positive.");
                if (item.baseline.width != item.width || item.baseline.height != item.height) throw new InvalidOperationException("Baseline dimensions do not match the capture case.");
                target = RenderTexture.GetTemporary(item.width, item.height, 24, RenderTextureFormat.ARGB32);
                var previousTarget = item.camera.targetTexture; var previousActive = RenderTexture.active;
                try
                {
                    item.camera.targetTexture = target; item.camera.Render(); RenderTexture.active = target;
                    current = new Texture2D(item.width, item.height, TextureFormat.RGBA32, false, false);
                    current.ReadPixels(new Rect(0, 0, item.width, item.height), 0, 0); current.Apply(false, false);
                }
                finally { item.camera.targetTexture = previousTarget; RenderTexture.active = previousActive; }
                heatmap = Compare(item, current, result);
                string directory = DirectoryPath();
                result.capturePath = WritePng(directory, Safe(item.id) + "-current.png", current);
                result.heatmapPath = WritePng(directory, Safe(item.id) + "-heatmap.png", heatmap);
                result.verdict = result.mismatchRatio <= item.allowedMismatchRatio ? "passed" : "failed";
            }
            catch (Exception error) { result.verdict = "failed"; result.failure = error.GetType().Name + ": " + error.Message; }
            finally
            {
                if (target) RenderTexture.ReleaseTemporary(target); if (current) Destroy(current); if (heatmap) Destroy(heatmap);
                string report = Path.Combine(DirectoryPath(), Safe(item.id) + "-visual-result.json"); File.WriteAllText(report, JsonUtility.ToJson(result, true));
                Debug.Log((result.verdict == "passed" ? "UAP_VISUAL_PASS " : "UAP_VISUAL_FAIL ") + report, this);
            }
        }

        private static Texture2D Compare(VisualCaptureCase item, Texture2D current, VisualQaResult result)
        {
            Color32[] actual = current.GetPixels32(); Color32[] expected = item.baseline.GetPixels32(); Color32[] mask = item.ignoreMask ? item.ignoreMask.GetPixels32() : null;
            if (mask != null && mask.Length != actual.Length) throw new InvalidOperationException("Ignore-mask dimensions do not match.");
            var pixels = new Color32[actual.Length]; int mismatches = 0, compared = 0, maximum = 0; int tolerance = Mathf.RoundToInt(item.channelTolerance * 255f);
            for (int i = 0; i < actual.Length; i++)
            {
                if (mask != null && mask[i].a > 0) { pixels[i] = new Color32(0, 0, 0, 0); continue; }
                int delta = Mathf.Max(Mathf.Abs(actual[i].r - expected[i].r), Mathf.Abs(actual[i].g - expected[i].g), Mathf.Abs(actual[i].b - expected[i].b));
                compared++; maximum = Mathf.Max(maximum, delta); bool failed = delta > tolerance; if (failed) mismatches++;
                pixels[i] = failed ? new Color32(255, (byte)(255 - delta), 0, 255) : new Color32(0, 0, 0, 0);
            }
            result.comparedPixels = compared; result.mismatchedPixels = mismatches; result.mismatchRatio = compared == 0 ? 0f : (float)mismatches / compared; result.maximumChannelDelta = maximum / 255f;
            var heatmap = new Texture2D(item.width, item.height, TextureFormat.RGBA32, false, false); heatmap.SetPixels32(pixels); heatmap.Apply(false, false); return heatmap;
        }

        private static VisualQaResult NewResult(VisualCaptureCase item) => new VisualQaResult { caseId = item.id, checkpointId = item.checkpointId, width = item.width, height = item.height, verdict = "failed", capturedUtc = DateTime.UtcNow.ToString("O"), platform = Application.platform.ToString(), unityVersion = Application.unityVersion, qualityLevel = QualitySettings.names[QualitySettings.GetQualityLevel()] };
        private static string DirectoryPath() { string path = Path.Combine(Application.persistentDataPath, "UnityArchitectPro", "VisualQa"); Directory.CreateDirectory(path); return path; }
        private static string WritePng(string directory, string name, Texture2D texture) { string path = Path.Combine(directory, name); File.WriteAllBytes(path, texture.EncodeToPNG()); return path; }
        private static string Safe(string value) { if (string.IsNullOrEmpty(value)) return "capture"; foreach (char invalid in Path.GetInvalidFileNameChars()) value = value.Replace(invalid, '_'); return value; }
    }
}
