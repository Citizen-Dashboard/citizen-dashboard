
# Civic Dashboard

The Citizen Dashboard is a Kubernetes-based platform that provides a suite of services for managing data, search, and synchronization. These services are containerized, orchestrated via Helm and Minikube, and designed for scalable deployments.

---

## Services Overview

The following services make up the Citizen Dashboard:

| **Service Name**                  | **Description**                               | **Port(s)** | **API Endpoints**                 |
|-----------------------------------|-----------------------------------------------|-------------|------------------------------------|
| `civic-dashboard-data-fetcher`  | Fetches data from external APIs.              | 5000/TCP    | `/fetch-data`, `/healthz`         |
| `civic-dashboard-data-store`    | Manages and stores data fetched or processed. | 8000/TCP    | `/store-data`, `/healthz`         |
| `civic-dashboard-elasticsearch` | Full-text search and indexing service.        | 9200/TCP    | N/A                                |
| `civic-dashboard-postgres`      | Database for structured data storage.         | 5432/TCP    | N/A                                |
| `civic-dashboard-search-api`    | Handles search queries using Elasticsearch.   | 5000/TCP    | `/search`, `/healthz`             |
| `civic-dashboard-sync-elastic`  | Syncs data to Elasticsearch.                  | 5000/TCP    | `/ingest`, `/healthz`             |
| `pgadmin`                         | Web-based database administration tool.       | 8080/TCP    | Web Interface                      |

---

## API Documentation

### **Data Fetcher Service**
#### Endpoint: `/fetch-data`
- **Method**: `GET`
- **Description**: Fetches data from external APIs between the specified date range.
- **Parameters**:
  - `from_date` (required): Start date (`YYYY-MM-DDTHH:MM:SS.sssZ` format).
  - `to_date` (required): End date (`YYYY-MM-DDTHH:MM:SS.sssZ` format).
- **Response**:
  - **200 OK**: JSON array of fetched records.
  - **400 Bad Request**: Invalid or missing parameters.
  - **500 Internal Server Error**: Server error while fetching data.

#### Health Check Endpoint: `/healthz`
- **Method**: `GET`
- **Response**: `200 OK` if the service is healthy.

---

### **Data Store Service**
#### Endpoint: `/store-data`
- **Method**: `POST`
- **Description**: Fetches data from the `Data Fetcher` service and stores it in PostgreSQL.
- **Request Body**:
  - `from_date` (required): Start date (`YYYY-MM-DDTHH:MM:SS.sssZ` format).
  - `to_date` (required): End date (`YYYY-MM-DDTHH:MM:SS.sssZ` format).
- **Response**:
  - **200 OK**: Data successfully stored.
  - **400 Bad Request**: Invalid or missing parameters.
  - **500 Internal Server Error**: Error in fetching or storing data.

#### Health Check Endpoint: `/healthz`
- **Method**: `GET`
- **Response**: `200 OK` if the service is healthy.

---

### **Search API Service**
#### Endpoint: `/search`
- **Method**: `GET`
- **Description**: Queries Elasticsearch for search results.
- **Parameters**:
  - `query` (required): The search term.
- **Response**:
  - **200 OK**: JSON array of search results.
  - **400 Bad Request**: Missing `query` parameter.
  - **500 Internal Server Error**: Error in querying Elasticsearch.

#### Health Check Endpoint: `/healthz`
- **Method**: `GET`
- **Response**: `200 OK` if the service is healthy.

---

### **Sync Elasticsearch Service**
#### Endpoint: `/ingest`
- **Method**: `POST`
- **Description**: Syncs data from PostgreSQL to Elasticsearch.
- **Response**:
  - **200 OK**: Data successfully ingested.
  - **500 Internal Server Error**: Error in syncing data.

#### Health Check Endpoint: `/healthz`
- **Method**: `GET`
- **Response**: `200 OK` if the service is healthy.

---

## Installation and Setup

### Prerequisites

#### **Minikube**
Install Minikube:
- **Windows**:
  ```bash
  choco install minikube
  ```
- **Ubuntu**:
  ```bash
  curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
  sudo install minikube-linux-amd64 /usr/local/bin/minikube
  ```
- **macOS**:
  ```bash
  brew install minikube
  ```

#### **Helm**
Install Helm:
- **Windows**:
  ```bash
  choco install kubernetes-helm
  ```
- **Ubuntu**:
  ```bash
  curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
  ```
- **macOS**:
  ```bash
  brew install helm
  ```

#### **Kubernetes CLI**
Install `kubectl`:
- **Windows**:
  ```bash
  choco install kubernetes-cli
  ```
- **Ubuntu**:
  ```bash
  sudo apt install kubectl
  ```
- **macOS**:
  ```bash
  brew install kubectl
  ```

---

### Setup Instructions

1. **Start Minikube**:
   ```bash
   minikube start --driver=<driver_name>
   ```

2. **Create Namespace**:
   ```bash
   kubectl create namespace civic-dashboard
   ```

3. **Add GHCR Secret**:
   ```bash
   kubectl create secret docker-registry ghcr-secret      --docker-server=ghcr.io      --docker-username=github_username      --docker-password=your_ghcr_token      --docker-email=github_email      --namespace=civic-dashboard
   ```

4. **Deploy the Application**:
   ```bash
   ./deploy.sh
   ```

5. **Verify Deployment**:
   ```bash
   kubectl get pods -n civic-dashboard
   ```

---

## Teardown Instructions

1. Uninstall Helm release:
   ```bash
   helm uninstall civic-dashboard --namespace civic-dashboard
   ```

2. Delete the namespace:
   ```bash
   kubectl delete namespace civic-dashboard
   ```

---

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m "Add feature"`.
4. Push the branch: `git push origin feature-name`.
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
