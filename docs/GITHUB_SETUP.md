# GitHub setup

Create an empty repository named `unity-architect-pro` under `robbiestokes21`, then push this repository to `main`. Enable Issues, Actions, Discussions if desired, and GitHub Security Advisories. Protect `main` by requiring the `Validate Plugin` workflow. Create releases from tags such as `v2.0.0-alpha.3`; the release workflow packages the plugin automatically.

Marketplace install metadata should continue to point at the repository root. Test locally with `claude --plugin-dir .` before tagging.
