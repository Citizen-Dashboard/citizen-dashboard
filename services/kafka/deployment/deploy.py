import logging
import argparse
import os
from kubernetes import client, config, utils
from kubernetes.client.rest import ApiException
from deployment.utils import configure_context

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "kafka"

def deploy_to_kubernetes(service: str, local: bool):
    configure_context(local)
    logger.info(f"Deploying service {service} to {'minikube' if local else 'cloud k8s cluster'}")

    zookeeper_path = os.path.join('services', service, 'deployment', 'zookeeper.yaml')
    kafka_path = os.path.join('services', service, 'deployment', 'kafka.yaml')

    # Load the Kubernetes configuration
    config.load_kube_config()

    # Create the API client
    api_client = client.ApiClient()
    v1 = client.CoreV1Api(api_client)

    try:
        # Check if the service already exists
        existing_services = v1.list_service_for_all_namespaces()
        for svc in existing_services.items:
            if svc.metadata.name == service:
                logger.warning(f"Service {service} already exists. Skipping deployment.")
                return

        # Apply the YAML files
        utils.create_from_yaml(api_client, zookeeper_path)
        utils.create_from_yaml(api_client, kafka_path)
        logger.info(f"Successfully deployed {service}.")

    except ApiException as e:
        if e.status == 409:
            logger.error(f"Conflict: {e.reason}. Service might already exist or port is in use.")
        else:
            logger.error(f"Failed to deploy service: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true')
    args = parser.parse_args()
    deploy_to_kubernetes(SERVICE, local=args.local)