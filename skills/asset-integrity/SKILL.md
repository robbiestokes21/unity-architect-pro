---
name: "asset-integrity"
description: "Audit Unity asset/meta GUID integrity, missing references, duplicate GUID risks, import settings, Resources usage, scene/prefab dependencies, and accidental asset churn. Use before releases, migrations, large refactors, or suspicious merge conflicts."
---
# Asset Integrity

Unity asset identity is GUID-based. Never regenerate/delete `.meta` files casually for tracked assets.

Audit:
- missing `.meta` for tracked assets and orphan `.meta` files
- duplicate GUIDs
- broken GUID/fileID references where detectable
- missing scripts and missing materials/textures
- merge-conflicted YAML
- unintended large binary or import-setting churn
- Resources/StreamingAssets growth and duplication
- platform-specific import overrides
- editor-only assets leaking into player content
- Addressables group/catalog consistency when used

Use `scripts/scan_asset_integrity.py` for a conservative filesystem-level preflight. It does not replace Unity's import database or Editor validation.
