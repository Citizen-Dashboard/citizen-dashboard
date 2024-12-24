import asyncio
import logging
import os
from pyhelm3 import Client, Chart
from kubernetes_asyncio import client, config
from kubernetes_asyncio.client import ApiException
from kubernetes_asyncio.client.api_client import ApiClient
from typing import Optional, Dict

# ============================
# Configuration and Constants
# ============================

# Environment Variables for Sensitive Data
KUBECONFIG_PATH = os.getenv('KUBECONFIG_PATH', None)  # Optional: Specify custom kubeconfig path
RELEASE_NAME = os.getenv('HELM_RELEASE_NAME', 'civic-dashboard')
NAMESPACE_NAME = os.getenv('HELM_NAMESPACE', 'civic-dashboard')
HELM_CHART_PATH = os.getenv('HELM_CHART_PATH', '../civic-dashboard/civic-dashboard/')  # Ensure this path is secure
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

# ============================
# Logger Setup
# ============================

def setup_logger() -> logging.Logger:
    """
    Set up the root logger for the script with configurable log levels.
    """
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))  # Dynamic log level based on environment

    # Clear existing handlers to avoid duplicate logs
    logger.handlers = []

    # Create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

    # Create formatter and add it to the handler
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)

    return logger

# ============================
# Namespace Management
# ============================

async def create_namespace(namespace_name: str, labels: Optional[Dict[str, str]] = None, logger: Optional[logging.Logger] = None):
    """
    Create a Kubernetes namespace with optional labels.
    """
    if logger is None:
        logger = logging.getLogger()

    try:
        # Load Kubernetes configuration securely
        if KUBECONFIG_PATH:
            await config.load_kube_config(config_file=KUBECONFIG_PATH)
            logger.debug(f"Loaded kubeconfig from specified path: {KUBECONFIG_PATH}.")
        else:
            await config.load_kube_config()
            logger.debug("Loaded kubeconfig from default location.")

        async with ApiClient() as api:
            v1 = client.CoreV1Api(api)
            logger.debug("Initialized CoreV1Api client.")

            # Define the namespace metadata with labels if provided
            metadata = client.V1ObjectMeta(name=namespace_name)
            if labels:
                metadata.labels = labels
                logger.debug(f"Added labels to namespace metadata: {labels}")

            # Define the namespace object
            namespace = client.V1Namespace(metadata=metadata)
            logger.debug(f"Namespace object created: {namespace}")

            # Create the namespace
            await v1.create_namespace(body=namespace)
            logger.info(f"Namespace '{namespace_name}' created successfully.")

    except ApiException as e:
        if e.status == 409:
            logger.warning(f"Namespace '{namespace_name}' already exists.")
        else:
            logger.error(f"API exception when creating namespace: {e}")
            raise
    except Exception as ex:
        logger.error(f"An unexpected error occurred while creating namespace: {ex}")
        raise

# ============================
# Helm Deployment
# ============================

async def deploy_helm_release(release_name: str, chart_path: str, namespace: str, logger: Optional[logging.Logger] = None):
    """
    Deploy or upgrade a Helm release.
    """
    if logger is None:
        logger = logging.getLogger()

    if not os.path.isdir(chart_path):
        logger.error(f"Chart path '{chart_path}' does not exist or is not a directory.")
        raise FileNotFoundError(f"Chart path '{chart_path}' does not exist or is not a directory.")

    try:
        helm_client = Client()
        logger.debug("Helm client initialized.")

        # Load the Helm chart
        try:
            chart = await helm_client.get_chart(chart_path)
            logger.debug(f"Helm chart loaded from path: '{chart_path}'.")
        except Exception as chart_ex:
            logger.error(f"Failed to load Helm chart from '{chart_path}': {chart_ex}")
            raise

        # Install or upgrade the Helm release
        await helm_client.install_or_upgrade_release(
            release_name=release_name,
            chart=chart,
            namespace=namespace,
            wait=False,
            timeout="300s",
            cleanup_on_fail=True,
            atomic=True,
        )
        logger.info(f"Helm release '{release_name}' deployed/updated successfully in namespace '{namespace}'.")

    except ApiException as e:
        logger.error(f"API exception during Helm deployment: {e}")
        raise
    except Exception as ex:
        logger.error(f"An unexpected error occurred during Helm deployment: {ex}")
        raise

# ============================
# Main Execution
# ============================

async def main():
    """
    Main function to orchestrate namespace creation and Helm deployment.
    """
    logger = setup_logger()
    logger.info("Starting Helm deployment script.")

    # Define any labels for the namespace (optional)
    namespace_labels = {
        "environment": "production",
        "team": "devops"
    }

    try:
        # Create Kubernetes namespace
        await create_namespace(NAMESPACE_NAME, labels=namespace_labels, logger=logger)

        # Deploy Helm release
        await deploy_helm_release(
            release_name=RELEASE_NAME,
            chart_path=HELM_CHART_PATH,
            namespace=NAMESPACE_NAME,
            logger=logger
        )

        logger.info("Helm deployment script completed successfully.")

    except Exception as e:
        logger.critical(f"Deployment script failed: {e}")
        raise
    finally:
        # Flush and close logging handlers
        logging.shutdown()

# ============================
# Entry Point
# ============================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDeployment script interrupted by user.")
    except Exception as e:
        print(f"\nDeployment script terminated with an error: {e}")
