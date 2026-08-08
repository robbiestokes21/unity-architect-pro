# Provider adapter contract

Phase 7 adapters translate a project's verified provider/bootstrap contract into the provider-neutral laboratory scenario format. The adapter engine does not invent NGO, NfE, Mirror, FishNet, Fusion, Steam, EOS or PlayFab command-line flags.

An adapter declares package/provider detection evidence, required project bootstrap behavior, variables, and a scenario template containing real executable argv arrays. Project bootstrap code must emit stable readiness/completion/failure markers and accept explicit role, endpoint/session, test identity, scenario and seed inputs.

Use `scripts/provider_adapter.py ADAPTER --var KEY=VALUE --out scenario.json`. Validate the installed package/version before selecting an adapter. Secrets and production credentials must never be embedded in descriptors; supply short-lived test credentials through a secret-aware environment outside committed files.

Fault shaping is explicit: `fault_on` runs a reviewed argv-array controller and records a matching teardown command. OS shaping tools may require elevation and vary by platform; absence is reported as unverified rather than silently simulated.
