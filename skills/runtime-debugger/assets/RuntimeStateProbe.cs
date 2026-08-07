using System;
using UnityEngine;

namespace UnityArchitectPro.Runtime
{
    public sealed class RuntimeStateProbe : MonoBehaviour
    {
        [SerializeField] private float intervalSeconds = 1f;
        private float _next;
        private void Update()
        {
            if (Time.unscaledTime < _next) return;
            _next = Time.unscaledTime + Mathf.Max(0.1f, intervalSeconds);
            Debug.Log($"[UAP-RUNTIME] frame={Time.frameCount} scene={gameObject.scene.name} object={name} active={isActiveAndEnabled} pos={transform.position}");
        }
    }
}
