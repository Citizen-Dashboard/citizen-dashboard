import logging
import argparse
from deployment.utils import execute, configure_context, replace_in_file
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "postgres"

def update_configmap():
    replacements = {
        '_POSTGRES_DB_': os.environ.get('POSTGRES_DB'),
        '_POSTGRES_USER_': os.environ.get('POSTGRES_USER'),
        '_POSTGRES_PASSWORD_': os.environ.get('POSTGRES_PASSWORD')
    }
    replace_in_file(f'services/{SERVICE}/deployment/psql-configmap.yaml', replacements)

def deploy_to_kubernetes(service: str, local: bool):
    configure_context(local)
    logger.info(f"Deploying service {service} to {'minikube' if local else 'cloud k8s cluster'}")

    update_configmap()
    execute(f"kubectl apply -f services/{service}/deployment/psql-configmap.yaml")
    execute(f"kubectl apply -f services/{service}/deployment/psql-pv.yaml")
    execute(f"kubectl apply -f services/{service}/deployment/psql-claim.yaml")
    execute(f"kubectl apply -f services/{service}/deployment/psql-main.yaml")
    execute(f"kubectl apply -f services/{service}/deployment/psql-service.yaml")
    execute(f"kubectl apply -f services/{service}/deployment/pgadmin-main.yaml")
    execute(f"kubectl apply -f services/{service}/deployment/pgadmin-service.yaml")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true')
    args = parser.parse_args()
    deploy_to_kubernetes(local=args.local)
