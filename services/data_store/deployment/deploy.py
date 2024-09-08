import logging
import argparse
from deployment.utils import push_image, build_and_tag_image, load_image_to_minikube, update_deployment_manifest, deploy_to_kubernetes, configure_context
import os
from kubernetes import client, config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "data-store"

def set_environment_variables(local: bool):
    configure_context(local)
    """Set environment variables for the Kubernetes deployment."""
    # Load the Kubernetes configuration
    config.load_kube_config()

    # Initialize the API client
    apps_v1 = client.AppsV1Api()

    # Define environment variables
    env_vars = {
        "DB_NAME": os.environ.get("POSTGRES_DB"),
        "DB_USER": os.environ.get("POSTGRES_USER"),
        "DB_PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "DB_HOST": "postgres",
        "DB_PORT": "5432"
    }

    # Get the current deployment
    namespace = "citizen-dashboard"
    deployment_name = SERVICE
    deployment = apps_v1.read_namespaced_deployment(deployment_name, namespace)

    # Update environment variables
    for container in deployment.spec.template.spec.containers:
        if container.name == SERVICE:
            for var, value in env_vars.items():
                # Check if the environment variable already exists
                existing_var = next((env for env in container.env if env.name == var), None)
                if existing_var:
                    existing_var.value = value
                else:
                    container.env.append(client.V1EnvVar(name=var, value=value))

    # Apply the updated deployment
    apps_v1.patch_namespaced_deployment(name=deployment_name, namespace=namespace, body=deployment)
    logger.info("Environment variables set successfully.")

def procedure(tag, local):
    build_and_tag_image(SERVICE, tag)
    
    if not local:
        push_image(f'korabel/cd-{SERVICE}', tag)
    else:
        load_image_to_minikube(SERVICE, tag)
    
    update_deployment_manifest(SERVICE, tag)
    deploy_to_kubernetes(SERVICE, local)
    set_environment_variables(local)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true')
    parser.add_argument('-t', '--tag', default='local')
    args = parser.parse_args()
    procedure(tag=args.tag, local=args.local)