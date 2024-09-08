import logging
import argparse
from kubernetes import client, config, utils
from deployment.utils import configure_context, replace_in_file
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "postgres"

def update_configmap():
    """
    Updates the Postgres configmap with environment variables.
    """
    logger.info('Updating Postgres configmap with environment variables...')
    replacements = {
        '_POSTGRES_DB_': os.environ.get('POSTGRES_DB'),
        '_POSTGRES_USER_': os.environ.get('POSTGRES_USER'),
        '_POSTGRES_PASSWORD_': os.environ.get('POSTGRES_PASSWORD')
    }
    configmap_path = os.path.join('services', SERVICE, 'deployment', 'psql-configmap.yaml')
    replace_in_file(configmap_path, replacements)
    logger.info('Postgres configmap updated successfully.')

def deploy_to_kubernetes(service: str, local: bool):
    """
    Deploys the Postgres service to Kubernetes.

    Args:
    - service (str): The name of the service.
    - local (bool): Indicates whether the deployment is local or not.
    """
    logger.info('Starting deployment process...')
    configure_context(local)
    logger.info(f"Deploying service {service} to {'minikube' if local else 'cloud k8s cluster'}")

    # Update the configmap with environment variables
    update_configmap()

    # Load the Kubernetes configuration
    logger.info('Loading Kubernetes configuration...')
    config.load_kube_config()

    # Create the API client
    logger.info('Creating API client...')
    api_client = client.ApiClient()

    # Apply the Kubernetes configurations
    config_dir = os.path.join('services', service, 'deployment')
    configs = [
        'psql-configmap.yaml',
        'psql-pv.yaml',
        'psql-claim.yaml',
        'psql-main.yaml',
        'psql-service.yaml',
        'pgadmin-main.yaml',
        'pgadmin-service.yaml'
    ]
    for config in configs:
        config_path = os.path.join(config_dir, config)
        logger.info(f"Applying {config}...")
        utils.create_from_yaml(api_client, config_path)
        logger.info(f"{config} applied successfully.")

    logger.info('Deployment process completed.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true')
    args = parser.parse_args()
    deploy_to_kubernetes(SERVICE, local=args.local)