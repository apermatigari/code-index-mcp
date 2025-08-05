"""
Code Index MCP Server with HTTP Endpoints
"""

import os
import sys
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import AsyncIterator, Dict, Any

# Third-party imports
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from mcp import types
from mcp.server.fastmcp import FastMCP, Context

# Local imports
from .project_settings import ProjectSettings
from .services import (
    ProjectService, IndexService, SearchService,
    FileService, SettingsService, FileWatcherService
)
from .services.settings_service import manage_temp_directory
from .utils import (
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
    base_path = ""
    print("Initializing Code Indexer MCP server...")
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
http_app = FastAPI()
http_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@http_app.get("/health")
async def health_check():
    return {"status": "ok", "service": "code-index-mcp"}

@http_app.post("/mcp/execute")
async def execute_command(request: Request):
    try:
        payload = await request.json()
        response = await mcp.handle_http_request(payload)
        return response
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

# [PASTE ALL OTHER @mcp.resource AND @mcp.tool DECORATORS HERE]
# Keep all your existing resource and tool functions exactly as they were

def main():
    """Run either in stdio mode or HTTP mode based on environment"""
    if os.getenv("RAILWAY"):
        import uvicorn
        uvicorn.run(http_app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
    else:
        mcp.run()

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    try:
        main()
        # Keep container alive in production
        if os.getenv("RAILWAY"):
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        pass