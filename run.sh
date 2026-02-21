#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="flux-automation"
CONTAINER_NAME="flux-automation"

cleanup() {
    echo "Cleaning up..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true
}

trap cleanup EXIT

cleanup

docker build -t "$IMAGE_NAME" .

docker run \
    --name "$CONTAINER_NAME" \
    --env-file .env \
    -p 8000:8000 \
    "$IMAGE_NAME"
