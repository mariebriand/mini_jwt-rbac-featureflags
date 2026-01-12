#!/bin/bash

# Stop and remove any previous container (optional cleanup)
docker rm -f mini_jwt-rbac-featureflags 2>/dev/null || true

# Build the image
docker build -t mini_jwt-rbac-featureflags .

# Run container
# - Mount the current folder (so DB + code changes persist)
# - Mount a dedicated ./data folder for DB & input files
docker run -d --name mini_jwt-rbac-featureflags \
	-p 8000:8000 \
	-v "$(pwd)":/app \
	-v "$(pwd)/data":/data \
	mini_jwt-rbac-featureflags