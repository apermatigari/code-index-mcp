#!/usr/bin/env python
"""
Minimal MCP Server for dr.binary compatibility
"""

import json
import sys
import os
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

def send_message(message):
    """Send a message to the MCP client."""
    json.dump(message, sys.stdout)
    sys.stdout.write('\n')
    sys.stdout.flush()

def read_message():
    """Read a message from the MCP client."""
    line = sys.stdin.readline()
    if not line:
        return None
    return json.loads(line)

def main():
    """Main MCP server loop."""
    # Send initialization message
    send_message({
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "serverInfo": {
                "name": "CodeIndexer",
                "version": "1.0.0"
            }
        }
    })
    
    # Keep the server running
    while True:
        try:
            message = read_message()
            if message is None:
                break
                
            # Handle ping/pong for keepalive
            if message.get("method") == "ping":
                send_message({
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "result": {}
                })
            else:
                # Echo back any other message
                send_message({
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
                    "result": {"message": "CodeIndexer MCP Server is running"}
                })
                
        except Exception as e:
            send_message({
                "jsonrpc": "2.0",
                "id": message.get("id") if 'message' in locals() else None,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            })

if __name__ == "__main__":
    main() 