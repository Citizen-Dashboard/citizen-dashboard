import os
import logging
import subprocess
from docker import from_env as docker_from_env
from kubernetes import client, config
import datetime
import yaml  # Import PyYAML

logger = logging.getLogger(__name__)

def execute(cmd):
    """Execute a shell command and handle errors."""
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to execute command (exit code {e.returncode}): \"{cmd}\". Aborting")
        exit(1)

def configure_context(local: bool):
    """Configure the Kubernetes context based on local or cloud deployment."""
    if local:
        execute(f"kubectl config use-context minikube")

def replace_in_file(file_path, replacements):
    """Replace placeholders in a file with actual values."""
    with open(file_path, 'r') as file:
        content = file.read()
    
    for placeholder, value in replacements.items():
        content = content.replace(placeholder, value)
    
    with open(file_path, 'w') as file:
        file.write(content)

def push_image(repo_name, tag):
    """Push a docker image to a specified repository with a tag."""
    docker_client = docker_from_env()
    logger.info("Logging into DockerHub")
    docker_client.login(username=os.environ.get("DOCKER_USER"), password=os.environ.get("DOCKER_PASSWORD"))
    logger.info("Uploading image to DockerHub")
    docker_client.images.push(f'{repo_name}:{tag}')
    logger.info("Image pushed successfully")

def build_and_tag_image(service, tag):
    """Build and tag a Docker image for a given service."""
    service_dir = service.replace("-", "_")
    docker_client = docker_from_env()
    logger.info(f"Building service {service} container")
    image, build_logs = docker_client.images.build(path=os.path.join('services', service_dir), tag=f'korabel/cd-{service}:{tag}')
    for chunk in build_logs:
        if 'stream' in chunk:
            logger.info(chunk['stream'].strip())
    return image

def load_image_to_minikube(service, tag):
    """Load a Docker image into Minikube."""
    logger.info("Uploading image to minikube...")
    execute(f"minikube image load korabel/cd-{service}:{tag}")

def update_deployment_manifest(service, tag):
    service_dir = service.replace("-", "_")
    """Update the deployment manifest with the correct image name."""
    file_path = os.path.join('services', service_dir, 'deployment', 'deployment.yaml')
    replace_in_file(file_path, {
        '_IMAGENAME_': f'korabel/cd-{service}:{tag}'
    })

def deploy_to_kubernetes(service: str, local: bool):
    """Deploy a service to Kubernetes."""
    configure_context(local)
    config.load_kube_config()
    k8s_client = client.AppsV1Api()
    service_dir = service.replace("-", "_")
    
    # Use PyYAML to load the deployment manifest
    file_path = os.path.join('services', service_dir, 'deployment', '_deployment.yaml')
    with open(file_path, 'r') as file:
        deployment_manifest = yaml.safe_load(file)
    
    logger.info(f"Deploying service {service} to {'minikube' if local else 'cloud k8s cluster'}")
    k8s_client.create_namespaced_deployment(namespace="citizen-dashboard", body=deployment_manifest)
    
    logger.info("Restarting deployment")
    k8s_client.patch_namespaced_deployment(
        name=service, 
        namespace="citizen-dashboard", 
        body={"spec": {"template": {"metadata": {"annotations": {"kubectl.kubernetes.io/restartedAt": str(datetime.datetime.now())}}}}}
    )