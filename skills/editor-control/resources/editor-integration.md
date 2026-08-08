# Recommended Unity Editor Integration Capabilities

The plugin ships an optional recommended MCP for Unity configuration in `.mcp.json` and `mcp/`, while keeping runtime behavior capability-based. When choosing/configuring that or another integration, prefer one that exposes most of these capabilities:

- identify open Unity project and editor version
- read compilation status/errors
- refresh/import assets
- inspect Editor.log / Console entries
- query and control Play Mode
- execute a public static Editor method
- inspect scene hierarchy and components
- create/update GameObjects/components or allow executing Editor scripts
- run Unity Test Framework tests with filters
- capture screenshots/Game View when visual verification matters

## Tool discovery rule
Claude must inspect the tools exposed in the current session and map them to these capabilities. It must not assume names such as `run_method_in_unity`, `unity_play_control`, or `run_unity_tests` exist unless the connected integration actually exposes them.

For MCP connections, use the `mcp-unity` handshake: confirm connection, read Editor/project state, explicitly select among multiple instances, and only then map observed tools/resources to capabilities.

## Concurrency rule
Calls that can trigger compilation, domain reload, scene reload, Play Mode transition, asset import or test execution must be serialized. Wait for completion before the next Unity state-changing action.

## Fallback
If no editor integration is available, create a temporary Editor script with a public static entry point and provide/run it through an available Unity batchmode/CLI path when possible. Otherwise leave the project in a state where the user can invoke the action manually from a menu item.
