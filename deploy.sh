#!/bin/bash

echo "Deploying Swarved RAG Backend..."

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

docker compose down
docker compose build --no-cache
docker compose up -d

echo "Waiting for service to start..."
sleep 15

docker compose ps
echo ""
curl -s http://localhost:8000/health | python3 -m json.tool

echo "Deployed! API: http://localhost:8000"