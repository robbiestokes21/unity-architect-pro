using System;
using System.Collections;
using System.Globalization;
using UnityEngine;

namespace UnityArchitectPro.GameplayTesting
{
    public sealed class TransformGameplayTestAdapter : MonoBehaviour, IGameplayTestAdapter
    {
        [SerializeField] private string targetId = "player";

        public string AdapterId => "transform";
        public bool SupportsAction(string kind) => kind == "teleport" || kind == "translate" || kind == "set_active";
        public bool SupportsAssertion(string kind) => kind == "active" || kind == "position" || kind == "distance_to";

        public IEnumerator Execute(GameplayAction action, GameplayTestContext context)
        {
            if (action.kind == "set_active") gameObject.SetActive(Bool(action.parameters, "value"));
            else
            {
                Vector3 value = Vector(action.parameters);
                if (action.kind == "teleport") transform.position = value;
                else transform.position += value;
            }
            yield return null;
        }

        public GameplayAssertionResult Evaluate(GameplayAssertion assertion, GameplayTestContext context)
        {
            if (assertion.kind == "active") return Result(gameObject.activeSelf == Bool(assertion.parameters, "value"), "active", gameObject.activeSelf.ToString());
            Vector3 expected = Vector(assertion.parameters);
            float tolerance = Float(assertion.parameters, "tolerance", 0.01f);
            float distance = Vector3.Distance(transform.position, expected);
            return Result(distance <= tolerance, assertion.kind, distance.ToString("G9", CultureInfo.InvariantCulture));
        }

        public void CaptureState(System.Collections.Generic.ICollection<GameplayStateValue> values, GameplayTestContext context)
        {
            values.Add(new GameplayStateValue { adapter = AdapterId, key = targetId + ".active", value = gameObject.activeSelf.ToString() });
            values.Add(new GameplayStateValue { adapter = AdapterId, key = targetId + ".position", value = transform.position.ToString("F4") });
        }

        public void ResetAdapter(GameplayTestContext context) { }

        private static GameplayAssertionResult Result(bool passed, string expected, string actual) => new GameplayAssertionResult { passed = passed, expected = expected, actual = actual };
        private static float Float(GameplayParameter[] parameters, string key, float fallback = 0f)
        {
            string value = Find(parameters, key);
            return string.IsNullOrEmpty(value) ? fallback : float.Parse(value, CultureInfo.InvariantCulture);
        }
        private static bool Bool(GameplayParameter[] parameters, string key)
        {
            string value = Find(parameters, key);
            if (string.IsNullOrEmpty(value)) throw new ArgumentException("Missing gameplay parameter: " + key);
            return bool.Parse(value);
        }
        private static Vector3 Vector(GameplayParameter[] parameters) => new Vector3(Float(parameters, "x"), Float(parameters, "y"), Float(parameters, "z"));
        private static string Find(GameplayParameter[] parameters, string key)
        {
            foreach (GameplayParameter parameter in parameters ?? Array.Empty<GameplayParameter>()) if (parameter.key == key) return parameter.value;
            return null;
        }
    }
}
