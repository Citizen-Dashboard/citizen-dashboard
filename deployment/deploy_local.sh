#!/bin/bash

kubectl create namespace citizen-dashboard
python3 services/kafka/deployment/deploy.py -l
python3 services/postgres/deployment/deploy.py -l
python3 services/data-fetcher/deployment/deploy.py -l -t dev-generic-local
python3 services/data-store/deployment/deploy.py -l -t dev-generic-local
