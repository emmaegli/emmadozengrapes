#!/bin/bash

if [ -z "$1" ]
  then
    echo "No environment supplied. Please tell this script which environment to start (local/staging/production)"
    exit
fi

echo "Stopping docker..."
docker-compose -f "$1".yml down

while true; do
    read -p "Would you like to kill all containers? (y/N)" yn
    case $yn in
        [Yy]* ) docker rm -f $(docker ps -q -a); break;;
        * ) exit;;
    esac
done