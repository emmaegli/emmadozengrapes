#!/usr/bin/env bash

function stop_docker()
{
    echo "CTRL_C received."
    while true; do
        read -p "Would you like to bring down the docker network? (Y/n)" yn
        case $yn in
            [Nn]* ) exit;;
            * ) docker-compose -f "$1".yml down; break;;
        esac
    done
}

if [ -z "$1" ]
  then
    echo "No environment supplied. Please tell this script which environment to start (local/staging/production)"
    exit
fi

echo "Starting docker with the $1 configuration..."
# Run everything in the background with -d
docker-compose -f "$1".yml up -d


# this is a trap for ctrl + c 
trap "stop_docker $1" SIGINT

echo "Tailing the log files of all of the containers..."
# Tail out all of the logs
docker-compose -f "$1".yml logs --tail=0 --follow