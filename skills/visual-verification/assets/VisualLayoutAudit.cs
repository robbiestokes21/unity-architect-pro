using System;
using System.Collections.Generic;
using UnityEngine;

namespace UnityArchitectPro.VisualQa
{
    public sealed class VisualLayoutAudit : MonoBehaviour
    {
        [SerializeField] private RectTransform[] mustRemainOnScreen;
        [SerializeField] private RectTransform[] mustNotOverlap;
        [SerializeField] private Renderer[] requireMaterials;

        public string[] Audit()
        {
            var issues = new List<string>();
            foreach (var rect in mustRemainOnScreen ?? Array.Empty<RectTransform>())
            {
                if (!rect) { issues.Add("Missing required RectTransform reference."); continue; }
                var corners = new Vector3[4]; rect.GetWorldCorners(corners);
                foreach (var corner in corners) if (corner.x < 0 || corner.y < 0 || corner.x > Screen.width || corner.y > Screen.height) { issues.Add(rect.name + " is clipped outside the screen."); break; }
            }
            var overlap = mustNotOverlap ?? Array.Empty<RectTransform>();
            for (int i = 0; i < overlap.Length; i++) for (int j = i + 1; j < overlap.Length; j++) if (overlap[i] && overlap[j] && WorldRect(overlap[i]).Overlaps(WorldRect(overlap[j]))) issues.Add(overlap[i].name + " overlaps " + overlap[j].name + ".");
            foreach (var renderer in requireMaterials ?? Array.Empty<Renderer>()) if (!renderer || !renderer.sharedMaterial || !renderer.sharedMaterial.shader) issues.Add((renderer ? renderer.name : "<missing renderer>") + " has a missing material or shader.");
            return issues.ToArray();
        }

        private static Rect WorldRect(RectTransform value) { var corners = new Vector3[4]; value.GetWorldCorners(corners); return Rect.MinMaxRect(corners[0].x, corners[0].y, corners[2].x, corners[2].y); }
    }
}
