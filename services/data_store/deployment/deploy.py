import logging
import argparse
from deployment.utils import execute, push_image, build_and_tag_image, load_image_to_minikube, update_deployment_manifest, deploy_to_kubernetes
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "data-store"

def set_environment_variables():
    """Set environment variables for the Kubernetes deployment."""
    env_vars = {
        "DB_NAME": os.environ.get("POSTGRES_DB"),
        "DB_USER": os.environ.get("POSTGRES_USER"),
        "DB_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "DB_HOST": "postgres",
        "DB_PORT": "5432"
    }
    for var, value in env_vars.items():
        execute(f"kubectl set env deployment/{SERVICE} {var}={value} -n citizen-dashboard")

def procedure(tag, local):
    build_and_tag_image(SERVICE, tag)
    
    if not local:
        push_image(f'korabel/cd-{SERVICE}', tag)
    else:
        load_image_to_minikube(SERVICE, tag)
    
    update_deployment_manifest(SERVICE, tag)
    deploy_to_kubernetes(SERVICE, local)
    set_environment_variables()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true')
    parser.add_argument('-t', '--tag', default='local')
    args = parser.parse_args()
    procedure(tag=args.tag, local=args.local)
