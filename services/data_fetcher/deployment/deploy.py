import logging
import argparse
from deployment.utils import push_image, build_and_tag_image, load_image_to_minikube, update_deployment_manifest, deploy_to_kubernetes

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "data-fetcher"

def procedure(tag, local):
    build_and_tag_image(SERVICE, tag)
    
    if not local:
        push_image(f'korabel/cd-{SERVICE}', tag)
    else:
        load_image_to_minikube(SERVICE, tag)
    
    update_deployment_manifest(SERVICE, tag)
    deploy_to_kubernetes(SERVICE, local)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true', default=True)
    parser.add_argument('-t', '--tag', default='local')
    args = parser.parse_args()
    procedure(tag=args.tag, local=args.local)
