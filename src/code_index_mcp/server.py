"""
Code Index MCP Server with HTTP Endpoints
"""

import os
import sys
import time
from pathlib import Path
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import AsyncIterator, Dict, Any

# Third-party imports
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mcp import types
from mcp.server.fastmcp import FastMCP, Context

# Add src directory to path for imports
current_dir = Path(__file__).parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Absolute imports
from code_index_mcp.project_settings import ProjectSettings
from code_index_mcp.services import (
    ProjectService, IndexService, SearchService,
    FileService, SettingsService, FileWatcherService
)
from code_index_mcp.utils import (
    handle_mcp_resource_errors, handle_mcp_tool_errors
)

@dataclass
class CodeIndexerContext:
    """Context for the Code Indexer MCP server."""
    base_path: str
    settings: ProjectSettings
    file_count: int = 0
    file_index: dict = field(default_factory=dict)
    index_cache: dict = field(default_factory=dict)
    file_watcher_service: FileWatcherService = None

@asynccontextmanager
async def indexer_lifespan(_server: FastMCP) -> AsyncIterator[CodeIndexerContext]:
    """Manage the lifecycle of the Code Indexer MCP server."""
    # Use current working directory or script directory as base path
    base_path = os.getcwd()
    if not base_path or not os.path.exists(base_path):
        # Fallback to script directory
        base_path = str(Path(__file__).parent.parent.parent)
    
    print("Initializing Code Indexer MCP server...")
    print(f"Base path: {base_path}")
    
    settings = ProjectSettings(base_path, skip_load=True)
    context = CodeIndexerContext(
        base_path=base_path,
        settings=settings,
        file_watcher_service=None
    )

    try:
        print("Server ready. Waiting for user to set project path...")
        yield context
    finally:
        if context.file_watcher_service:
            print("Stopping file watcher service...")
            context.file_watcher_service.stop_monitoring()
        if context.base_path and context.index_cache:
            print(f"Saving index for project: {context.base_path}")
            settings.save_index(context.index_cache)

# Create the MCP server
mcp = FastMCP("CodeIndexer", lifespan=indexer_lifespan, dependencies=["pathlib"])

# Create FastAPI HTTP app
http_app = FastAPI(title="Code Index MCP Server", version="1.0.0")
http_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@http_app.get("/")
async def root():
    """Root endpoint for the web server."""
    return {
        "message": "Code Index MCP Server is running",
        "status": "ok",
        "service": "code-index-mcp",
        "endpoints": {
            "health": "/health",
            "mcp_execute": "/mcp/execute"
        }
    }

@http_app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "code-index-mcp"}

@http_app.post("/mcp/execute")
async def execute_command(request: Request):
    """MCP protocol execution endpoint."""
    try:
        payload = await request.json()
        # For HTTP mode, we'll need to implement proper MCP protocol handling
        # For now, return a basic response indicating the endpoint is available
        return {"status": "ok", "message": "MCP endpoint available", "payload": payload}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ----- Original MCP Resources/Tools -----
@mcp.resource("config://code-indexer")
@handle_mcp_resource_errors
def get_config() -> str:
    ctx = mcp.get_context()
    return ProjectService(ctx).get_project_config()

@mcp.resource("files://{file_path}")
@handle_mcp_resource_errors
def get_file_content(file_path: str) -> str:
    ctx = mcp.get_context()
    return FileService(ctx).get_file_content(file_path)

def main():
    """Run either in stdio mode or HTTP mode based on environment"""
    # Check if we're in Railway or any cloud environment
    is_railway = os.getenv("RAILWAY") == "true"
    is_cloud = os.getenv("PORT") is not None or is_railway
    
    print(f"Environment: {'Railway/Cloud' if is_cloud else 'Local'}")
    print(f"RAILWAY env var: {os.getenv('RAILWAY')}")
    print(f"PORT env var: {os.getenv('PORT')}")
    
    if is_cloud:
        import uvicorn
        port = int(os.getenv("PORT", 8000))
        print(f"Starting HTTP server on port {port}")
        uvicorn.run(
            http_app, 
            host="0.0.0.0", 
            port=port,
            log_level="info"
        )
    else:
        print("Starting MCP server in stdio mode")
        mcp.run()

if __name__ == '__main__':
    try:
        main()
        
        # Keep container alive in production
        if os.getenv("RAILWAY") == "true":
            while True:
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server crashed: {str(e)}")
        sys.exit(1)