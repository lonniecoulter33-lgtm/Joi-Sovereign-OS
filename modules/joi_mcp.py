"""
MCP (Model Context Protocol) Integration

MCP lets Joi connect to external tool servers (Spotify, GitHub, Obsidian, etc).
This module auto-discovers MCP servers and registers their tools.

SETUP:
  1. Install MCP servers (see https://github.com/modelcontextprotocol)
  2. Configure server paths in .env:
     JOI_MCP_SERVERS=server1.json,server2.json
  3. Joi will auto-load tools from those servers on startup

NOTE: Full MCP implementation requires the `mcp` Python package.
      This is a stub for future expansion.
"""
import os
import json

MCP_SERVERS_CONFIG = os.getenv("JOI_MCP_SERVERS", "").strip()

if MCP_SERVERS_CONFIG:
    print(f"  MCP servers configured: {MCP_SERVERS_CONFIG}")
    print("  (MCP integration stub loaded -- install `mcp` package for full support)")
else:
    print("  No MCP servers configured (set JOI_MCP_SERVERS in .env to enable)")

# TODO: When user installs MCP servers, implement:
# - Read server configs
# - Connect to MCP servers via stdio/http
# - Auto-register their tools dynamically
# - Forward tool calls to MCP servers
