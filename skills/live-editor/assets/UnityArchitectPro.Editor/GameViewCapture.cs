#if UNITY_EDITOR
using System.IO;
using UnityEditor;
using UnityEngine;

namespace UnityArchitectPro.EditorTools
{
    public static class GameViewCapture
    {
        [MenuItem("Tools/Unity Architect Pro/Capture Game View")]
        public static void Capture()
        {
            if (!EditorApplication.isPlaying)
            {
                Debug.LogError("[UnityArchitectPro] Game View capture requires Play Mode.");
                return;
            }
            var relative = Path.Combine("Temp", "UnityArchitectPro", "gameview.png");
            Directory.CreateDirectory(Path.GetDirectoryName(relative)!);
            ScreenCapture.CaptureScreenshot(relative);
            Debug.Log($"[UnityArchitectPro] Requested Game View capture: {Path.GetFullPath(relative)}");
        }
    }
}
#endif
