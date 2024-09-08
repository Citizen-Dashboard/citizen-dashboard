import logging
from kubernetes import client, config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def delete_core_resources(core_api_instance, namespace):
    """Delete core resources in the namespace."""
    logger.info(f"Deleting core resources in namespace: {namespace}")
    try:
        core_api_instance.delete_collection_namespaced_pod(namespace=namespace)
        logger.info(f"Successfully deleted pods in namespace '{namespace}'")
    except client.ApiException as e:
        logger.warning(f"Failed to delete pods in namespace '{namespace}': {str(e)}")
    try:
        core_api_instance.delete_collection_namespaced_service(namespace=namespace)
        logger.info(f"Successfully deleted services in namespace '{namespace}'")
    except client.ApiException as e:
        logger.warning(f"Failed to delete services in namespace '{namespace}': {str(e)}")
    try:
        core_api_instance.delete_collection_namespaced_config_map(namespace=namespace)
        logger.info(f"Successfully deleted config maps in namespace '{namespace}'")
    except client.ApiException as e:
        logger.warning(f"Failed to delete config maps in namespace '{namespace}': {str(e)}")
    try:
        core_api_instance.delete_collection_namespaced_secret(namespace=namespace)
        logger.info(f"Successfully deleted secrets in namespace '{namespace}'")
    except client.ApiException as e:
        logger.warning(f"Failed to delete secrets in namespace '{namespace}': {str(e)}")
    try:
        core_api_instance.delete_collection_namespaced_persistent_volume_claim(namespace=namespace)
        logger.info(f"Successfully deleted persistent volume claims in namespace '{namespace}'")
    except client.ApiException as e:
        logger.warning(f"Failed to delete persistent volume claims in namespace '{namespace}': {str(e)}")

def delete_apps_resources(apps_api_instance, namespace):
    """Delete application resources in the namespace."""
    logger.info(f"Deleting application resources in namespace: {namespace}")
    try:
        apps_api_instance.delete_collection_namespaced_deployment(namespace=namespace)
        logger.info(f"Successfully deleted deployments in namespace '{namespace}'")
    except client.ApiException as e:
        logger.warning(f"Failed to delete deployments in namespace '{namespace}': {str(e)}")
    try:
        apps_api_instance.delete_collection_namespaced_replica_set(namespace=namespace)
        logger.info(f"Successfully deleted replica sets in namespace '{namespace}'")
    except client.ApiException as e:
        logger.warning(f"Failed to delete replica sets in namespace '{namespace}': {str(e)}")
    try:
        apps_api_instance.delete_collection_namespaced_stateful_set(namespace=namespace)
        logger.info(f"Successfully deleted stateful sets in namespace '{namespace}'")
    except client.ApiException as e:
        logger.warning(f"Failed to delete stateful sets in namespace '{namespace}': {str(e)}")
    try:
        apps_api_instance.delete_collection_namespaced_daemon_set(namespace=namespace)
        logger.info(f"Successfully deleted daemon sets in namespace '{namespace}'")
    except client.ApiException as e:
        logger.warning(f"Failed to delete daemon sets in namespace '{namespace}': {str(e)}")

def delete_namespace(core_api_instance, namespace):
    """Delete the namespace."""
    logger.info(f"Deleting namespace: {namespace}")
    try:
        core_api_instance.delete_namespace(name=namespace)
        logger.info(f"Successfully deleted namespace '{namespace}'")
    except client.ApiException as e:
        if e.status == 404:
            logger.info(f"Namespace '{namespace}' does not exist. Skipping deletion.")
        else:
            logger.error(f"An error occurred while deleting namespace '{namespace}': {str(e)}")

def main():
    try:
        # Load kube config
        logger.info("Loading kube config")
        config.load_kube_config()

        # Create API instances
        logger.info("Creating API instances")
        core_v1_api = client.CoreV1Api()
        apps_v1_api = client.AppsV1Api()
        
        namespace = "citizen-dashboard"

        # Perform deletions
        delete_core_resources(core_v1_api, namespace)
        delete_apps_resources(apps_v1_api, namespace)
        delete_namespace(core_v1_api, namespace)
        logger.info("Deletion process completed")
    except Exception as e:
        logger.error(f'An unexpected error occurred during the overall process: {str(e)}')

if __name__ == "__main__":
    main()