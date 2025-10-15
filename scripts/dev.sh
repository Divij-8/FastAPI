#!/usr/bin/env bash
set -euo pipefail

# Build and start using docker compose
export DOCKER_BUILDKIT=1
docker compose up --build
