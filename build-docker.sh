#!/usr/bin/env bash

if [ -z "$1" ]
  then
    echo "No environment supplied. Please tell this script which environment to start (local/staging/production)"
    exit
fi

echo "Builing the $1 docker configuration..."
# Run everything in the background with -d
docker-compose -f "$1".yml build "${@:2}"