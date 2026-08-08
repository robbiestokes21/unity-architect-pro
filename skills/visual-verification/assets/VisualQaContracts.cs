using System;
using UnityEngine;

namespace UnityArchitectPro.VisualQa
{
    [Serializable] public sealed class VisualCaptureCase
    {
        public string id;
        public string checkpointId;
        public Camera camera;
        public Texture2D baseline;
        public Texture2D ignoreMask;
        public int width = 1920;
        public int height = 1080;
        [Range(0f, 1f)] public float channelTolerance = 0.02f;
        [Range(0f, 1f)] public float allowedMismatchRatio = 0.001f;
    }

    [Serializable] public sealed class VisualQaResult
    {
        public int schemaVersion = 1;
        public string caseId;
        public string checkpointId;
        public string verdict;
        public int width;
        public int height;
        public int comparedPixels;
        public int mismatchedPixels;
        public float mismatchRatio;
        public float maximumChannelDelta;
        public string capturePath;
        public string heatmapPath;
        public string failure;
        public string capturedUtc;
        public string platform;
        public string unityVersion;
        public string qualityLevel;
    }
}
