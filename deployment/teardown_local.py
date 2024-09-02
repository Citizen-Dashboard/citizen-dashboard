from kubernetes import client, config

def delete_core_resources(core_api_instance, namespace):
    """Delete core resources in the namespace."""
    print(f"Deleting core resources in namespace: {namespace}")
    core_api_instance.delete_collection_namespaced_pod(namespace=namespace)
    core_api_instance.delete_collection_namespaced_service(namespace=namespace)
    core_api_instance.delete_collection_namespaced_config_map(namespace=namespace)
    core_api_instance.delete_collection_namespaced_secret(namespace=namespace)
    core_api_instance.delete_collection_namespaced_persistent_volume_claim(namespace=namespace)

def delete_apps_resources(apps_api_instance, namespace):
    """Delete application resources in the namespace."""
    print(f"Deleting application resources in namespace: {namespace}")
    apps_api_instance.delete_collection_namespaced_deployment(namespace=namespace)
    apps_api_instance.delete_collection_namespaced_replica_set(namespace=namespace)
    apps_api_instance.delete_collection_namespaced_stateful_set(namespace=namespace)
    apps_api_instance.delete_collection_namespaced_daemon_set(namespace=namespace)

def delete_namespace(core_api_instance, namespace):
    """Delete the namespace."""
    print(f"Deleting namespace: {namespace}")
    core_api_instance.delete_namespace(name=namespace)

def main():
    # Load kube config
    config.load_kube_config()

    # Create API instances
    core_v1_api = client.CoreV1Api()
    apps_v1_api = client.AppsV1Api()
    
    namespace = "citizen-dashboard"

    # Perform deletions
    delete_core_resources(core_v1_api, namespace)
    delete_apps_resources(apps_v1_api, namespace)
    delete_namespace(core_v1_api, namespace)

if __name__ == "__main__":
    main()
