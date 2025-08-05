#!/bin/bash

# Build script for Code Index MCP Docker image
# Usage: ./build-docker.sh [tag]

set -e

# Default tag
TAG=${1:-latest}
IMAGE_NAME="code-index-mcp"

echo "Building Code Index MCP Docker image..."
echo "Image: $IMAGE_NAME:$TAG"

# Build the Docker image
docker build -t $IMAGE_NAME:$TAG .

echo "✅ Docker image built successfully!"
echo "Image: $IMAGE_NAME:$TAG"

# Optional: Push to registry (uncomment if you have a registry)
# echo "Pushing to registry..."
# docker tag $IMAGE_NAME:$TAG yourusername/$IMAGE_NAME:$TAG
# docker push yourusername/$IMAGE_NAME:$TAG

echo "🎉 Ready for dr.binary deployment!"
echo ""
echo "Next steps:"
echo "1. Push this image to a container registry (Docker Hub, GitHub Container Registry, etc.)"
echo "2. Update the .vscode/mcp.json file with your registry URL"
echo "3. Deploy to dr.binary" 