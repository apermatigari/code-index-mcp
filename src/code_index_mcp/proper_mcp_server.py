#!/usr/bin/env python
"""
Proper MCP Server that follows the MCP protocol specification
"""

import json
import sys
import os
from pathlib import Path

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
    # Wait for the initialize request from the client
    while True:
        try:
            message = read_message()
            if message is None:
                break
                
            # Handle initialize request
            if message.get("method") == "initialize":
                send_message({
                    "jsonrpc": "2.0",
                    "id": message.get("id"),
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
                break
                
        except Exception as e:
            send_message({
                "jsonrpc": "2.0",
                "id": message.get("id") if 'message' in locals() else None,
                "error": {
                    "code": -1,
                    "message": str(e)
                }
            })
            break
    
    # Send initialized notification
    send_message({
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {}
    })
    
    # Keep the server running and handle requests
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
            # Handle any other requests
            elif message.get("id"):
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