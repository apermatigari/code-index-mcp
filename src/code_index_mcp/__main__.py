#!/usr/bin/env python
"""
Entry point for running the Code Index MCP server as a module.
"""

import sys
import os
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Import and run the main function
from code_index_mcp.server import main

if __name__ == "__main__":
    main()
