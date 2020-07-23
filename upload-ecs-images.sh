#!/bin/bash

SERVICES=$(docker-compose -f ./production.yml ps --services)
REGISTRY_URL=129087907154.dkr.ecr.us-east-1.amazonaws.com/emmadozengrapes

aws ecr get-login-password --profile personal --region us-east-1 | docker login --username AWS --password-stdin $REGISTRY_URL

echo "Tagging images of all of our services"
while read -r service; do
    eval "docker tag emmadozengrapes_production_${service} ${REGISTRY_URL}:latest"
done <<< "$SERVICES"

echo "Uploading our images to ECR... This may take a while..."
docker push $REGISTRY_URL
