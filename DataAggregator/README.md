This project is a data aggregator for the City of Toronto's Agenda Items. It is a Python application that fetches data from the City's public website, processes the data, and pushes to a kafka topic for consumption by other applications. 

Everytime the aggregator is run, it pulls agenda-items from past `nth` to `mth` day window, pushes them to a kafka topic and exists.
In production, a scheduler can be configured to run the aggregator periodically.

The number of days data to pull is configured by the environment variables:
    ```bash
    # Fetch agenda items from past nth day
    Fetch_from_Past_nth_day=10
    # Fetch agenda items to past nth day
    Fetch_to_Past_nth_day=2
    ```

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (Docker Desktop for Windows)
- Docker Compose
- Poetry

### Installation

* Make sure you have the prerequisites installed.
* Create and activate venv for project:
  
    UNIX/LINUX
    ```bash
    python -m venv ./.venv
    source ./.venv/Scripts/activate
    ```

    WINDOWS
    ```bash
    python -m venv ./.venv
    ./.venv/Scripts/activate
    ```


* Navigate to the `/data-aggregator` directory and run the following command to install the project dependencies using Poetry:

    ```bash
    poetry install
    ```

### Create .env file
Create a `.env` file in `/data-aggregator/data_aggregator` folder to configure environment variables. Use the `local-env-file` as reference. Update the kafka port numbers from the next step.
Feel free to change the values, but make sure to update the KAFKA topic and group values in `.env` file in the `ElasticSearch-Server` and `ElasticSearch-Client` project.

### Installing Kafka
Follow the instructions at [developer.confluent.io](https://developer.confluent.io/get-started/python/#kafka-setup) to install kafka in your **LOCAL** environment.
once the kafka cluster is up and running, copy the `Plaintext Ports` printed in your terminal to the `.env` file in the `/data_aggregator` directory of the project.

### Running the Application

To run the application, Navigate to the `/data-aggregator` directory and use the following command:

```bash
poetry run python ./data_aggregator/main.py
```


### Logging

Logs are generated in the `/logs` directory.