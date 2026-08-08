using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;

namespace UnityArchitectPro.GameplayTesting
{
    /// <summary>Development-only deterministic gameplay journey runner.</summary>
    [DisallowMultipleComponent]
    public sealed class GameplayScenarioRunner : MonoBehaviour
    {
        [Serializable] public sealed class AssertionEvidence { public string kind; public string target; public string expected; public string actual; public bool passed; public string message; public float elapsedSeconds; }
        [Serializable] public sealed class StepEvidence { public string id; public string action; public string target; public string result; public float durationSeconds; public AssertionEvidence[] assertions; public GameplayStateValue[] state; public string screenshot; public string failure; }
        [Serializable] public sealed class ScenarioResult { public int schemaVersion = 1; public string scenarioId; public string scenarioName; public int seed; public string startedUtc; public string finishedUtc; public string result; public float durationSeconds; public StepEvidence[] steps; public string failure; }

        [SerializeField] private TextAsset scenarioJson;
        [SerializeField] private MonoBehaviour[] adapterBehaviours;
        [SerializeField] private bool runOnStart = true;
        [SerializeField] private bool captureScreenshotOnFailure = true;
        [SerializeField] private bool useUnscaledTime = true;
        private readonly List<IGameplayTestAdapter> _adapters = new List<IGameplayTestAdapter>();
        private Coroutine _running;

        private void Awake()
        {
            _adapters.Clear();
            foreach (var behaviour in adapterBehaviours)
            {
                var adapter = behaviour as IGameplayTestAdapter;
                if (adapter != null) _adapters.Add(adapter);
            }
        }

        private void Start()
        {
            Debug.Log("UAP_GAMEPLAY_READY", this);
            if (runOnStart) Run();
        }

        [ContextMenu("Run Gameplay Scenario")]
        public void Run()
        {
            if (_running != null) { Debug.LogError("[UAP-GAMEPLAY] A scenario is already running.", this); return; }
            _running = StartCoroutine(RunScenario());
        }

        private IEnumerator RunScenario()
        {
            var started = Now();
            var result = new ScenarioResult { startedUtc = DateTime.UtcNow.ToString("O"), result = "failed" };
            var evidence = new List<StepEvidence>();
            GameplayScenario scenario = null;
            try
            {
                if (!scenarioJson) throw new InvalidOperationException("No gameplay scenario JSON is assigned.");
                scenario = JsonUtility.FromJson<GameplayScenario>(scenarioJson.text);
                Validate(scenario);
                result.scenarioId = scenario.id; result.scenarioName = scenario.name; result.seed = scenario.seed;
                UnityEngine.Random.InitState(scenario.seed);
                var context = new GameplayTestContext { Scenario = scenario };
                for (var index = 0; index < scenario.steps.Length; index++)
                {
                    if (Now() - started > scenario.timeoutSeconds) throw new TimeoutException("Scenario timeout exceeded.");
                    context.StepIndex = index; context.Step = scenario.steps[index];
                    var stepEvidence = new StepEvidence { id = context.Step.id, action = context.Step.action.kind, target = context.Step.action.target, result = "failed" };
                    evidence.Add(stepEvidence);
                    var stepStarted = Now();
                    yield return RunAction(context.Step.action, context, stepEvidence);
                    if (!string.IsNullOrEmpty(stepEvidence.failure)) throw new InvalidOperationException(stepEvidence.failure);
                    if (context.Step.settleSeconds > 0f) yield return Wait(context.Step.settleSeconds);
                    yield return RunAssertions(context.Step.assertions, context, stepEvidence);
                    if (!string.IsNullOrEmpty(stepEvidence.failure)) throw new InvalidOperationException(stepEvidence.failure);
                    if (scenario.captureStateAfterEachStep || context.Step.captureState) stepEvidence.state = CaptureState(context);
                    stepEvidence.durationSeconds = Now() - stepStarted; stepEvidence.result = "passed";
                }
                result.result = "passed";
            }
            catch (Exception error)
            {
                result.failure = error.GetType().Name + ": " + error.Message;
                if (evidence.Count > 0 && string.IsNullOrEmpty(evidence[evidence.Count - 1].failure)) evidence[evidence.Count - 1].failure = result.failure;
                if (captureScreenshotOnFailure && evidence.Count > 0) evidence[evidence.Count - 1].screenshot = CaptureFailureScreenshot(scenario == null ? "unknown" : scenario.id);
            }
            finally
            {
                if (scenario != null)
                {
                    var context = new GameplayTestContext { Scenario = scenario };
                    foreach (var adapter in _adapters)
                    {
                        try { adapter.ResetAdapter(context); }
                        catch (Exception error) { Debug.LogWarning("[UAP-GAMEPLAY] Adapter reset failed: " + error.Message, this); }
                    }
                }
                result.steps = evidence.ToArray(); result.durationSeconds = Now() - started; result.finishedUtc = DateTime.UtcNow.ToString("O");
                WriteResult(result);
                Debug.Log(result.result == "passed" ? "UAP_TEST_COMPLETE" : "UAP_TEST_FAILED " + result.failure, this);
                _running = null;
            }
        }

        private IEnumerator RunAction(GameplayAction action, GameplayTestContext context, StepEvidence evidence)
        {
            var adapter = FindAdapter(action.adapter, action.kind, true);
            if (adapter == null) { evidence.failure = "No adapter supports action " + action.kind; yield break; }
            IEnumerator operation;
            try { operation = adapter.Execute(action, context); }
            catch (Exception error) { evidence.failure = "Action start failed: " + error.Message; yield break; }
            if (operation == null) yield break;
            var started = Now();
            while (true)
            {
                bool next;
                object current = null;
                try { next = operation.MoveNext(); if (next) current = operation.Current; }
                catch (Exception error) { evidence.failure = "Action failed: " + error.Message; yield break; }
                if (!next) yield break;
                if (Now() - started > Mathf.Max(.01f, action.timeoutSeconds)) { evidence.failure = "Action timeout: " + action.kind; yield break; }
                yield return current;
            }
        }

        private IEnumerator RunAssertions(GameplayAssertion[] assertions, GameplayTestContext context, StepEvidence evidence)
        {
            if (assertions == null) { evidence.assertions = Array.Empty<AssertionEvidence>(); yield break; }
            var results = new List<AssertionEvidence>();
            foreach (var assertion in assertions)
            {
                var adapter = FindAdapter(assertion.adapter, assertion.kind, false);
                if (adapter == null) { evidence.failure = "No adapter supports assertion " + assertion.kind; yield break; }
                var started = Now(); GameplayAssertionResult value = null;
                while (Now() - started <= Mathf.Max(.01f, assertion.timeoutSeconds))
                {
                    try { value = adapter.Evaluate(assertion, context); }
                    catch (Exception error) { value = new GameplayAssertionResult { passed = false, message = error.GetType().Name + ": " + error.Message }; }
                    if (value != null && value.passed) break;
                    yield return null;
                }
                var item = new AssertionEvidence { kind = assertion.kind, target = assertion.target, expected = assertion.expected, actual = value == null ? "<null>" : value.actual, passed = value != null && value.passed, message = value == null ? "Adapter returned null." : value.message, elapsedSeconds = Now() - started };
                results.Add(item);
                if (!item.passed) { evidence.assertions = results.ToArray(); evidence.failure = "Assertion failed: " + assertion.kind + " " + item.message; yield break; }
            }
            evidence.assertions = results.ToArray();
        }

        private GameplayStateValue[] CaptureState(GameplayTestContext context)
        {
            var values = new List<GameplayStateValue>();
            foreach (var adapter in _adapters)
                try { adapter.CaptureState(values, context); }
                catch (Exception error) { values.Add(new GameplayStateValue { adapter = adapter.AdapterId, key = "captureError", value = error.Message }); }
            return values.ToArray();
        }

        private IGameplayTestAdapter FindAdapter(string requested, string kind, bool action)
        {
            foreach (var adapter in _adapters)
            {
                if (!string.IsNullOrEmpty(requested) && adapter.AdapterId != requested) continue;
                if (action ? adapter.SupportsAction(kind) : adapter.SupportsAssertion(kind)) return adapter;
            }
            return null;
        }

        private string CaptureFailureScreenshot(string scenarioId)
        {
            var directory = Path.Combine(Application.persistentDataPath, "UnityArchitectPro", "GameplayTests"); Directory.CreateDirectory(directory);
            var path = Path.Combine(directory, SafeName(scenarioId) + "-failure.png"); ScreenCapture.CaptureScreenshot(path); return path;
        }

        private void WriteResult(ScenarioResult result)
        {
            var directory = Path.Combine(Application.persistentDataPath, "UnityArchitectPro", "GameplayTests"); Directory.CreateDirectory(directory);
            var path = Path.Combine(directory, SafeName(result.scenarioId) + "-result.json"); File.WriteAllText(path, JsonUtility.ToJson(result, true));
            Debug.Log("[UAP-GAMEPLAY] Result: " + path, this);
        }

        private float Now() { return useUnscaledTime ? Time.unscaledTime : Time.time; }
        private IEnumerator Wait(float seconds) { var until = Now() + seconds; while (Now() < until) yield return null; }
        private static string SafeName(string value) { if (string.IsNullOrEmpty(value)) return "scenario"; foreach (var invalid in Path.GetInvalidFileNameChars()) value = value.Replace(invalid, '_'); return value; }
        private static void Validate(GameplayScenario scenario)
        {
            if (scenario == null || scenario.schemaVersion != 1) throw new InvalidOperationException("Unsupported gameplay scenario schema.");
            if (scenario.steps == null || scenario.steps.Length == 0) throw new InvalidOperationException("Scenario has no steps.");
            foreach (var step in scenario.steps) if (step == null || string.IsNullOrEmpty(step.id) || step.action == null || string.IsNullOrEmpty(step.action.kind)) throw new InvalidOperationException("Every step needs an id and action kind.");
        }
    }
}
