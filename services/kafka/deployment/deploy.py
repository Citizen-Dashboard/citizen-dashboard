import os
import logging
import argparse


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "kafka"

def execute(cmd):
    resp = os.system(cmd)
    if resp != 0:
        logger.error(f"Failed to execute build/deploy procedure (exit code {resp}): \"{cmd}\". Aborting")
        exit(1)    

def procedure(local):
    if local:
        execute(f"kubectl config use-context minikube")
    
    logger.info(f"Deploying service to {'minikube' if local else 'cloud k8s cluster'}")

    execute(f"kubectl apply -f services/{SERVICE}/deployment/zookeeper.yaml")
    execute(f"kubectl apply -f services/{SERVICE}/deployment/kafka.yaml")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true')
    args = parser.parse_args()
    procedure(local=args.local)