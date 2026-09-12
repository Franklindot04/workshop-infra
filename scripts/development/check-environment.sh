#!/usr/bin/env bash

set -euo pipefail

echo "Checking workshop-infra development environment..."

command -v git >/dev/null
command -v docker >/dev/null

echo "Git: $(git --version)"
echo "Docker: $(docker --version)"

echo "Development environment is ready."
