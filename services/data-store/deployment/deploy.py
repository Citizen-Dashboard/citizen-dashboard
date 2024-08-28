import os
import logging
import argparse


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "data-store"

def execute(cmd):
    resp = os.system(cmd)
    if resp != 0:
        logger.error(f"Failed to execute build/deploy procedure (exit code {resp}): \"{cmd}\". Aborting")
        exit(1)    

def isGNU():
    resp = os.popen("echo $OSTYPE").read()
    if resp.startswith("darwin"):
        return False
    return True

def procedure(tag, local):
    tag = tag.replace("/", "-")

    logger.info(f"Building service {SERVICE} container")
    execute(f"docker buildx build services/{SERVICE}/. -t korabel/cd-{SERVICE}:{tag}")

    if not local:
        logger.info("Logging into DockerHub")
        if os.environ.get("DOCKER_USER") is None or os.environ.get("DOCKER_PASSWORD") is None:
            logger.error("Cannot push image to DockerHub. User and Password must be provided via DOCKER_USER and DOCKER_PASSWORD env variables")
            exit(1)
        execute(f"echo $DOCKER_PASSWORD | docker login --username {os.environ.get('DOCKER_USER')} --password-stdin docker.io")
        
        logger.info("Uploading image to DockerHub")
        execute(f"docker image push korabel/cd-{SERVICE}:{tag}")
    else:
        logger.info("Uploading image to minikube...")
        execute(f"minikube image load korabel/cd-{SERVICE}:{tag}")
    
    if local:
        execute(f"kubectl config use-context minikube")
    
    logger.info(f"Injecting image name to deployment manifest")
    execute(f"cp -rf services/{SERVICE}/deployment/deployment.yaml services/{SERVICE}/deployment/_deployment.yaml")
    execute("sed -i {} 's/_IMAGENAME_/korabel\/cd-{}:{}/g' services/{}/deployment/_deployment.yaml".
            format("" if isGNU() else "''", SERVICE, tag, SERVICE))

    logger.info(f"Deploying service to {'minikube' if local else 'cloud k8s cluster'}")
    execute(f"kubectl apply -f services/{SERVICE}/deployment/_deployment.yaml")
    execute(f"kubectl apply -f services/{SERVICE}/deployment/service.yaml")

    logger.info(f"Configuring environment variables for {SERVICE} pods")
    execute(f"kubectl set env deployment/{SERVICE} DB_NAME={os.environ.get('POSTGRES_DB')} -n citizen-dashboard")
    execute(f"kubectl set env deployment/{SERVICE} DB_USER={os.environ.get('POSTGRES_USER')} -n citizen-dashboard")
    execute(f"kubectl set env deployment/{SERVICE} DB_PASSWORD={os.environ.get('POSTGRES_PASSWORD')} -n citizen-dashboard")
    execute(f"kubectl set env deployment/{SERVICE} DB_HOST=postgres -n citizen-dashboard")
    execute(f"kubectl set env deployment/{SERVICE} DB_PORT=5432 -n citizen-dashboard")

    execute(f"kubectl rollout restart deployment {SERVICE} -n citizen-dashboard")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true')
    parser.add_argument('-t', '--tag', default='local')
    args = parser.parse_args()
    procedure(tag=args.tag, local=args.local)