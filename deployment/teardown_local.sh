#!/bin/bash
# Teardown script to remove all Kubernetes components

kubectl delete all --all --namespace citizen-dashboard
kubectl delete pvc --all --namespace citizen-dashboard
kubectl delete ns citizen-dashboard