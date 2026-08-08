#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
subprocess.check_call([sys.executable,str(ROOT/'scripts/validate_mcp.py')])
config=json.loads((ROOT/'.mcp.json').read_text())['mcpServers']['unityMCP']
assert config=={'type':'http','url':'http://localhost:8080/mcp'}
skill=(ROOT/'skills/mcp-unity/SKILL.md').read_text()
for token in ['Required handshake','select the intended project','compilation','read state back','loopback-only']:
    assert token in skill,token
print('MCP integration tests: OK')
