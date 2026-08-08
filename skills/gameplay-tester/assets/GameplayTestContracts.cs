using System;
using System.Collections;
using System.Collections.Generic;

namespace UnityArchitectPro.GameplayTesting
{
    [Serializable] public sealed class GameplayParameter { public string key; public string value; }
    [Serializable] public sealed class GameplayAssertion { public string adapter; public string kind; public string target; public string comparison; public string expected; public float tolerance; public float timeoutSeconds = 2f; public GameplayParameter[] parameters; }
    [Serializable] public sealed class GameplayAction { public string adapter; public string kind; public string target; public float timeoutSeconds = 5f; public GameplayParameter[] parameters; }
    [Serializable] public sealed class GameplayStep { public string id; public GameplayAction action; public float settleSeconds; public GameplayAssertion[] assertions; public bool captureState = true; }
    [Serializable] public sealed class GameplayScenario { public int schemaVersion = 1; public string id; public string name; public int seed; public float timeoutSeconds = 120f; public bool captureStateAfterEachStep; public GameplayStep[] steps; }
    [Serializable] public sealed class GameplayStateValue { public string adapter; public string key; public string value; }
    [Serializable] public sealed class GameplayAssertionResult { public bool passed; public string actual; public string message; }

    public sealed class GameplayTestContext
    {
        public GameplayScenario Scenario { get; internal set; }
        public GameplayStep Step { get; internal set; }
        public int StepIndex { get; internal set; }
        public IDictionary<string, object> Shared { get; } = new Dictionary<string, object>();
    }

    /// <summary>Project-owned bridge from semantic test steps to real gameplay systems.</summary>
    public interface IGameplayTestAdapter
    {
        string AdapterId { get; }
        bool SupportsAction(string kind);
        bool SupportsAssertion(string kind);
        IEnumerator Execute(GameplayAction action, GameplayTestContext context);
        GameplayAssertionResult Evaluate(GameplayAssertion assertion, GameplayTestContext context);
        void CaptureState(ICollection<GameplayStateValue> values, GameplayTestContext context);
        void ResetAdapter(GameplayTestContext context);
    }
}
