# Unity MCP connection

Unity Architect Pro ships configuration and operating rules for [CoplayDev MCP for Unity](https://github.com/CoplayDev/unity-mcp), an optional third-party MIT-licensed bridge. The bridge is not vendored or installed automatically.

## Install and connect

1. In the target Unity project, open Package Manager and add `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#v10.0.0`. Review newer releases before changing the pinned version.
2. Open **Window → MCP for Unity**, start the bridge, and use its client configuration action. The default local HTTP endpoint is `http://localhost:8080/mcp`.
3. Claude Code plugin users can use the root `.mcp.json`. Review and approve the project-scoped server when Claude prompts, then inspect it with `claude mcp get unityMCP` or `/mcp`.
4. Marketplace authors can paste `marketplace-config.json` into the MCP config field. VS Code uses the different top-level structure in `vscode-mcp.json`.
5. If the client cannot use HTTP, install `uv` and adapt `stdio-config.json`. On Windows, replace `uvx` with its absolute executable path if it is not on `PATH`.

## Connection contract

- Bind to loopback unless remote access, authentication, and network exposure have been deliberately reviewed.
- Treat project MCP configuration as executable authority. Users must review and approve it.
- Discover resources and tools at runtime. Names and payloads can change between MCP for Unity releases.
- Read editor/project state before mutations. With multiple Editors, explicitly select the target instance.
- Serialize state-changing calls around compilation, domain reload, asset import, scene reload, Play Mode, tests, and builds.
- After script edits, wait until compilation completes and inspect current Console errors before continuing.
- Verify mutations by reading state back; use screenshots, tests, Console evidence, profiler output, or build results as appropriate.
- Never expose the bridge publicly without its documented remote authentication controls. Never place credentials in committed MCP JSON.

The authoritative installation and transport details are maintained in the [MCP for Unity installation guide](https://coplaydev.github.io/unity-mcp/getting-started/install). Unity Architect Pro remains capability-based so a different Unity bridge can be used when it satisfies the same safety and evidence contract.
