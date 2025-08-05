@echo off
echo Building Code Index MCP Docker image...

set TAG=%1
if "%TAG%"=="" set TAG=latest
set IMAGE_NAME=code-index-mcp

echo Image: %IMAGE_NAME%:%TAG%

docker build -t %IMAGE_NAME%:%TAG% .

if %ERRORLEVEL% EQU 0 (
    echo ✅ Docker image built successfully!
    echo Image: %IMAGE_NAME%:%TAG%
    echo.
    echo 🎉 Ready for dr.binary deployment!
    echo.
    echo Next steps:
    echo 1. Push this image to a container registry ^(Docker Hub, GitHub Container Registry, etc.^)
    echo 2. Update the .vscode/mcp.json file with your registry URL
    echo 3. Deploy to dr.binary
) else (
    echo ❌ Docker build failed!
)

pause 