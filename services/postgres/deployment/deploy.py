import os
import logging
import argparse


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SERVICE = "postgres"

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

def procedure(local):
    if local:
        execute(f"kubectl config use-context minikube")
    
    logger.info(f"Deploying service {SERVICE} to {'minikube' if local else 'cloud k8s cluster'}")

    execute(f"cp -rf services/{SERVICE}/deployment/psql-configmap.yaml services/{SERVICE}/deployment/_psql-configmap.yaml")
    execute("sed -i {} 's/_POSTGRES_DB_/{}/g' services/{}/deployment/_psql-configmap.yaml".
            format("" if isGNU() else "''", os.environ.get('POSTGRES_DB'), SERVICE))
    execute("sed -i {} 's/_POSTGRES_USER_/{}/g' services/{}/deployment/_psql-configmap.yaml".
            format("" if isGNU() else "''", os.environ.get('POSTGRES_USER'), SERVICE))
    execute("sed -i {} 's/_POSTGRES_PASSWORD_/{}/g' services/{}/deployment/_psql-configmap.yaml".
            format("" if isGNU() else "''", os.environ.get('POSTGRES_PASSWORD'), SERVICE))
    
    execute(f"kubectl apply -f services/{SERVICE}/deployment/psql-configmap.yaml")
    execute(f"kubectl apply -f services/{SERVICE}/deployment/psql-pv.yaml")
    execute(f"kubectl apply -f services/{SERVICE}/deployment/psql-claim.yaml")
    execute(f"kubectl apply -f services/{SERVICE}/deployment/psql-main.yaml")
    execute(f"kubectl apply -f services/{SERVICE}/deployment/psql-service.yaml")
    execute(f"kubectl apply -f services/{SERVICE}/deployment/pgadmin-main.yaml")
    execute(f"kubectl apply -f services/{SERVICE}/deployment/pgadmin-service.yaml")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Citizen Dashboard Deployer',
                                     description='Builds and deploys Citizen Dashboard components')
    parser.add_argument('-l', '--local', action='store_true')
    args = parser.parse_args()
    procedure(local=args.local)