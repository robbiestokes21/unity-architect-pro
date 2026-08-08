#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]; errors=[]
files=['.mcp.json','mcp/marketplace-config.json','mcp/vscode-mcp.json','mcp/stdio-config.json']
documents={}
for relative in files:
    try: documents[relative]=json.loads((ROOT/relative).read_text(encoding='utf-8'))
    except Exception as exc: errors.append(relative+': '+str(exc))
for relative in files[:2]:
    server=documents.get(relative,{}).get('mcpServers',{}).get('unityMCP',{})
    if server.get('type')!='http': errors.append(relative+': unityMCP type must be http')
    if server.get('url')!='http://localhost:8080/mcp': errors.append(relative+': endpoint must remain loopback-only')
vscode=documents.get(files[2],{}).get('servers',{}).get('unityMCP',{})
if vscode.get('type')!='http' or vscode.get('url')!='http://localhost:8080/mcp': errors.append(files[2]+': invalid VS Code HTTP configuration')
stdio=documents.get(files[3],{}).get('mcpServers',{}).get('unityMCP',{})
if stdio.get('command')!='uvx' or stdio.get('args',[])[-2:]!=['--transport','stdio']: errors.append(files[3]+': invalid stdio configuration')
serialized='\n'.join(json.dumps(value) for value in documents.values()).lower()
for forbidden in ['api_key','token','password','authorization']:
    if forbidden in serialized: errors.append('MCP configuration contains forbidden credential field: '+forbidden)
required=['mcp/README.md','skills/mcp-unity/SKILL.md']
for relative in required:
    if not (ROOT/relative).is_file(): errors.append('missing '+relative)
if errors: raise SystemExit('\n'.join('ERROR: '+error for error in errors))
print('MCP validation: OK')
