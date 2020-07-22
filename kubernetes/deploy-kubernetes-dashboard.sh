#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Help for this script found here: 
# https://docs.aws.amazon.com/eks/latest/userguide/dashboard-tutorial.html#dashboard-metrics-server

# Deploy the kubernetes metrics server
kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/download/v0.3.6/components.yaml

# Deploy the Kuberenetes Dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.0-beta8/aio/deploy/recommended.yaml

# Apply AWS Service account
kubectl apply -f $DIR/auth/eks-admin-service-account.yaml
