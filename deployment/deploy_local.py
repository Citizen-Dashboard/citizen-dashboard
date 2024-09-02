from kubernetes import client, config
from kubernetes.client.rest import ApiException
from services import deploy_data_fetcher, deploy_data_store, deploy_kafka, deploy_postgres

def create_namespace(api_instance, namespace):
    """Create a Kubernetes namespace if it doesn't already exist."""
    try:
        api_instance.read_namespace(name=namespace)
        print(f"Namespace '{namespace}' already exists.")
    except ApiException as e:
        if e.status == 404:
            print(f"Creating namespace: {namespace}")
            namespace_body = client.V1Namespace(metadata=client.V1ObjectMeta(name=namespace))
            api_instance.create_namespace(body=namespace_body)
        else:
            raise


def main():
    # Load kube config
    config.load_kube_config()

    # Create API instance for CoreV1
    core_v1_api = client.CoreV1Api()

    namespace = "citizen-dashboard"

    # Create the namespace if it doesn't exist
    create_namespace(core_v1_api, namespace)

    # Deploy services
    deploy_kafka("kafka", True)
    deploy_postgres("postgres", True)
    deploy_data_store("data-store", True)
    deploy_data_fetcher("data-fetcher", True)

if __name__ == "__main__":
    main()
