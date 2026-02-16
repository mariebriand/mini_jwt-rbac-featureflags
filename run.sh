#!/bin/bash

# Stop and remove any previous container (optional cleanup)
docker rm -f mini_jwt-rbac-featureflags 2>/dev/null || true

# Build the image
docker build -t mini_jwt-rbac-featureflags .

# Run container
# - Mount the app folder (live core reload)
# - Mount the data folder (persist database)

docker run -d --name mini_jwt-rbac-featureflags \
	-p 8000:8000 \
	-v "$(pwd)/app":/app/app \
	-v "$(pwd)/data":/data \
	-v "$(pwd)/tests":/app/tests \
	mini_jwt-rbac-featureflags