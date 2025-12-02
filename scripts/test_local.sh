#!/bin/bash

# Define variables
IMAGE_NAME="diabetes-prediction-lambda"
PORT=9000

echo "Building Docker image..."
docker build -t $IMAGE_NAME ./deploy

echo "Running Docker container locally on port $PORT..."
# Run the container in the background
docker run -d -p $PORT:8080 --name $IMAGE_NAME-container $IMAGE_NAME

echo "Waiting for container to start..."
sleep 5

echo "Sending test request..."
curl -X POST "http://localhost:$PORT/2015-03-31/functions/function/invocations" \
    -H "Content-Type: application/json" \
    -d '{"features": [1, 85, 66, 29, 0, 26.6, 0.351, 31]}'

echo -e "\n\nLogs:"
docker logs $IMAGE_NAME-container

echo -e "\nStopping and removing container..."
docker stop $IMAGE_NAME-container
docker rm $IMAGE_NAME-container
