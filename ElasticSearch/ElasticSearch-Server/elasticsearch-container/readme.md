# How to deploy Elastic search and Kibana locally
The docker compose file deploys ElasticSearch and Kibana in two docker containers.

## Steps:
1. Make sure Docker daemon is running.
2. Navigate to elastic-server folder
3. Create a .env file with the following attributes:
   ```shell
        COMPOSE_PROJECT_NAME="elastic-dev"
        elasticUserName="elastic-local"
        ELASTIC_PASSWORD="<Random Password string>"
        ELASTIC_CLUSTER_NAME="elastic_cluster_1"
        KIBANA_USERNAME="kibana-local"
        KIBANA_PASSWORD="<Random password string>"

        discovery.type="single-node"
        xpack.security.http.ssl.enabled="false"
        xpack.license.self_generated.type="trial"
        xpack.security.enabled="false"
   ```

4. Build docker images
   ```bash
   $ docker-compose build
   ```

5. Run the docker container
   ```bash
   $ docker-compose up
   ```

## Verify containers
ElasticSearch will be running on `http://localhost:9200`. Try hitting the url and login with the `ELASTIC_PASSWORD` configured in the `.env` file.
Open Kibana console by hitting `http://localhost:5601`.