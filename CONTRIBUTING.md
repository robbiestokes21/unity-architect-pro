# Contributing

Keep skills small, composable, evidence-driven and version-aware. New provider-specific behavior belongs in a resource or specialist skill rather than bloating the master router. Every change should include validation instructions and must not commit secrets, machine-specific paths, generated caches, Unity `Library/`, or proprietary project assets.

Run `python scripts/validate_plugin.py` before opening a PR. Prefer official Unity/provider documentation for version-sensitive behavior.
