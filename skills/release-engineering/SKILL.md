---
name: "release-engineering"
description: "Prepare Unity projects for repeatable releases: versioning, CI, automated tests/builds, artifacts, symbols, changelogs, signing boundaries, dedicated-server images, deployment checks and platform distribution workflows."
---

# Unity Release Engineer

Build a reproducible pipeline from source revision to signed/deployable artifacts.

Keep credentials in CI secret stores, never repository/client code. Pin Unity/package/toolchain versions where practical. Separate build, test, content build, packaging, signing and deployment stages so failures are diagnosable.

Capture Unity logs and test results as artifacts. Produce symbols where supported. For servers, produce immutable versioned images/artifacts with health/readiness, graceful termination and observability hooks.

Do not automate store publishing or production deployment without explicit user intent and the required credentials/tooling.

## CI template
`assets/github-actions/unity-validation.yml.template` provides a provider-neutral preflight skeleton. It intentionally leaves Unity licensing/activation and build execution to the organization's chosen CI integration.
