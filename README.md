# Citizen Dashboard

## Scraper
Citizen Dashboard makes involvement in civic discourse engaging, intuitive and fun! Currently, only the data acquisition utility is functional. To begin, simply run:

```citizen-dashboard-backend/scripts/data_fetcher.py```

What this does:
- Pull voting record data for Toronto City Council (`citizen-dashboard-backend/scripts/fetch_voting_records.py`).
- Using voting record data, create list of unique agenda items.
- Pull and parse HTML data by feeding unique agenda item ID to City Council website's API with random wait intervals in between requests (there may be several parsing strategies to choose from, but they should all be located under the directory `citizen-dashboard-backend/scripts/scraper`).

The script should generate two files in the `data` directory:
- `combined_voting_data.parquet` - Contains the combined voting data for City Council.
- `items_info.parquet` - Contains parsed agenda item information from the City Council website.

## Setting up Docker Environment
1. Initialize docker swarm. Set advertise address ```docker swarm init --advertise-addr <eth0 ip addr>```
2. Create secret for SQL database


## Environments
Citizen-Dashboard project supports deployment to a k8s cluster. We currently have one such cluster running for production (hosted in DigitalOcean). For local development/testing/experimintation project supports deployment onto a local minikube cluster.

1. **Deploy directly to production cluster** - currently configured for any push to the main branch. Once changes are committed, Github action will pick it up, build and deploy to k8s cluster in DigitalOcean
> [!CAUTION] 
> There is currently no proper gatekeeping on this procedure, if pushed code has breaking changes, production is down

2. **Deploy to a local environment** - requires some setting up, see next section for details

## Setting up local developement environment
> [!NOTE] 
> We are all developing on personal laptops, each with different OS type and/or version. As much as we are trying to use tools that are as standard as possible, discrepancies can and will pop up. If you enounter a problem please share.

### Prerequisites
1. **Python** - the build procedures that run locally do not require fancy new python versions - let's agree on '>3.9' :smile:
2. **Docker** - docker deamon should be installed and running on your machine
3. **[kubectl](https://kubernetes.io/docs/reference/kubectl/)** - any of the latest versions will do
4. **[minikube](https://minikube.sigs.k8s.io/docs/)** - please lookup any guide on the web, there are a lot. If you are a mac (Apple silicon) user you can follow [this](https://devopscube.com/minikube-mac/) one


### Delpoy locally
Now we can move on to actually deploying the project
1. Start your minukube by running ```minikube start```. At this point minikube will configure itself and spawn, and eventually register itself into a local k8s configuration file. If everything went well, you should now see your minikube cluster by invoking ```kubectl config get-contexts``` and see the minikube container running by calling ```docker ps```

2. Now we need to define some environment variables. These are variables that configure infrastructure componenets inside the cluster ([kafka](https://kafka.apache.org/) and [postgres](https://www.postgresql.org/) and [dockerhub](https://hub.docker.com/)). Obiously, as this data is sensitive (credentials), we cannot add it in plain text to the repo, please ask project admins for it.
```
    POSTGRES_DB=***
    POSTGRES_USER=***
    POSTGRES_PASSWORD=***
    DOCKER_USERNAME=***
    DOCKER_PASSWORD=***
```

3. Create a new namespace called citizen-dashboad in you minikube by running ```kubectl create namespace citizen-dashboard```

4. Deploy your local code to minikube by running ```./deployment/deploy_local.sh```

> [!NOTE] 
> When running this deployment for the first time on your machine, it could take a while as it builds our service images for the first time. The next time you run it should be quicker as some of the image layers are already cached locally



