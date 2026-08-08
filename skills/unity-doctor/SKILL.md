---
name: "unity-doctor"
description: "Perform a whole-project Unity health audit and produce a prioritized engineering report covering architecture, correctness, serialization, lifecycle, performance, testing, multiplayer/security, assets, build health and dependencies. Use for /unity-doctor style audits, inherited projects, pre-release reviews, or when deciding what technical debt to fix first."
---

# Unity Doctor

Audit; do not shotgun-refactor. Findings require evidence from code/config/logs.

## Workflow
1. Load `project-intelligence` and establish project truth.
2. Sample architecture broadly, then drill into risky areas.
3. Run static diagnostics/tests/build checks when available and appropriate.
4. If multiplayer exists, load `multiplayer` and the network security reviewer.
5. If Addressables/DOTS/custom shaders exist, load the matching specialist skill.
6. Score categories only from observed evidence. `Unknown` is better than an invented grade.

## Categories
- Architecture & dependency boundaries
- Correctness & Unity lifecycle
- Serialization / scene / prefab safety
- CPU / GPU / GC / memory / loading
- Testing & regression confidence
- Multiplayer correctness & authority
- Security / secrets / client trust
- Build & platform health
- Asset/content pipeline
- Dependency/package health
- Maintainability & diagnostics

## Severity
`Critical`: exploit/data loss/build blocker/crash class issue.
`High`: likely production defect, severe performance risk or fragile architecture.
`Medium`: meaningful debt or probable future defect.
`Low`: cleanup/consistency with limited risk.

## Required report format
Start with an executive summary and confidence level. Then include scores, evidence-backed findings, and a prioritized remediation sequence. For every finding include affected files/symbols, why it matters, evidence, recommended fix and verification method.

Do not report generic Unity advice as a project finding.
