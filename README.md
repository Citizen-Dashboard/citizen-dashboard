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