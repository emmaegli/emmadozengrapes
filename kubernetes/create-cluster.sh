#!/bin/bash

eksctl create cluster \
--name skirmish-prod \
--version 1.16 \
--region us-east-1 \
--nodegroup-name standard-workers \
--node-type t3.small \
--nodes 1 \
--nodes-min 1 \
--nodes-max 3 \
--ssh-access \
--ssh-public-key $HOME/.ssh/id_rsa.pub \
--managed
