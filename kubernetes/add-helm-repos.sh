#!/bin/bash

# Add the zalando helm repo so we can install postgres operator
# https://github.com/zalando/postgres-operator
helm repo add zalando https://raw.githubusercontent.com/zalando/postgres-operator/master/charts/postgres-operator/

helm repo update