#!/usr/bin/env python
"""
Development convenience script to run the Code Index MCP server.
"""
import sys
import os
import traceback
from pathlib import Path

# Add src directory to path
script_dir = Path(__file__).parent
src_path = script_dir / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from code_index_mcp.server import main

    if __name__ == "__main__":
        print("Starting Code Index MCP server...", file=sys.stderr)
        print(f"Added path: {src_path}", file=sys.stderr)
        print(f"Python version: {sys.version}", file=sys.stderr)
        main()
except ImportError as e:
    print(f"Import Error: {e}", file=sys.stderr)
    print(f"Current sys.path: {sys.path}", file=sys.stderr)
    print("Traceback:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
except Exception as e:
    print(f"Error starting server: {e}", file=sys.stderr)
    print("Traceback:", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
