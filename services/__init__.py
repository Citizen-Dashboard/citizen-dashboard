from .data_fetcher.deployment import deploy_data_fetcher
from .data_store.deployment import deploy_data_store
from .kafka.deployment import deploy_kafka
from .postgres.deployment import deploy_postgres

__all__ = (
    'deploy_data_fetcher',
    'deploy_data_store',
    'deploy_kafka',
    'deploy_postgres'
)