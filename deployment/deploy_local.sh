#!/bin/bash

python services/kafka/deployment/deploy.py -l
python services/postgres/deployment/deploy.py -l
python services/data-fetcher/deployment/deploy.py -l -t dev-generic-local
python services/data-store/deployment/deploy.py -l -t dev-generic-local
