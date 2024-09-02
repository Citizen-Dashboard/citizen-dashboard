import logging
import argparse
from deployment.utils import execute, configure_context

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "kafka"

def deploy_to_kubernetes(service: str, local: bool):
    configure_context(local)
    logger.info(f"Deploying service {service} to {'minikube' if local else 'cloud k8s cluster'}")

    execute(f"kubectl apply -f services/{service}/deployment/zookeeper.yaml")
    execute(f"kubectl apply -f services/{service}/deployment/kafka.yaml")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true')
    args = parser.parse_args()
    deploy_to_kubernetes(local=args.local)
