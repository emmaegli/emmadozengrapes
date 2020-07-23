#!/bin/bash

eksctl create cluster \
--name blogs-prod \
--version 1.17 \
--region us-east-1 \
--zones=us-east-1a,us-east-1b \
--nodegroup-name standard-workers \
--node-type t3.micro \
--nodes 1 \
--nodes-min 1 \
--nodes-max 3 \
--ssh-access \
--ssh-public-key $HOME/.ssh/id_rsa.pub \
--managed
