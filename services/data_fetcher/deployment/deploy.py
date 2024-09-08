import logging
import argparse
from deployment.utils import push_image, build_and_tag_image, load_image_to_minikube, update_deployment_manifest, deploy_to_kubernetes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "data-fetcher"

def procedure(tag, local):
    """
    Builds and deploys the data-fetcher service.

    Args:
    - tag (str): The tag for the Docker image.
    - local (bool): Indicates whether the deployment is local or not.
    """
    # Build and tag the Docker image
    build_and_tag_image(SERVICE, tag)
    
    # Push the image to DockerHub if not local, otherwise load it into Minikube
    if not local:
        # Push the image to DockerHub for cloud deployment
        push_image(f'korabel/cd-{SERVICE}', tag)
    else:
        # Load the image into Minikube for local deployment
        load_image_to_minikube(SERVICE, tag)
    
    # Update the deployment manifest with the new image tag
    update_deployment_manifest(SERVICE, tag)
    
    # Deploy the service to Kubernetes
    deploy_to_kubernetes(SERVICE, local)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true', default=True, help='Indicates a local deployment')
    parser.add_argument('-t', '--tag', default='local', help='The tag for the Docker image')
    args = parser.parse_args()
    procedure(tag=args.tag, local=args.local)