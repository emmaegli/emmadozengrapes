#!/bin/bash

SERVICES=$(docker-compose -f ./api/production.yml ps --services)
REGISTRY_URL=129087907154.dkr.ecr.us-east-1.amazonaws.com/kaniecki-blog

aws ecr get-login-password | docker login --username AWS --password-stdin $REGISTRY_URL

echo "Tagging images of all of our services"
while read -r service; do
    eval "docker tag kaniecki_blog_${service} ${REGISTRY_URL}:latest"
done <<< "$SERVICES"

echo "Uploading our images to ECR... This may take a while..."
docker push $REGISTRY_URL
