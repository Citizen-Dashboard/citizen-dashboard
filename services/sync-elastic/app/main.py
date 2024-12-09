from flask import Flask, jsonify, request
import psycopg2
from elasticsearch import Elasticsearch, helpers
import os
import traceback

app = Flask(__name__)

# Database configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "your_db_name")
DB_USER = os.getenv("DB_USER", "your_db_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_db_password")

# Elasticsearch configuration
ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")

def fetch_data_from_postgres():
    """Fetch data from PostgreSQL."""
    app.logger.info("Connecting to PostgreSQL database.")
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        app.logger.info("Fetching data from the 'city_council_meetings' table.")
        cur.execute("SELECT * FROM city_council_meetings;")
        columns = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        app.logger.info(f"Fetched {len(rows)} records from the database.")
        cur.close()
        conn.close()
        return [dict(zip(columns, row)) for row in rows]
    except Exception as e:
        app.logger.error(f"Error fetching data from PostgreSQL: {e}")
        app.logger.error(traceback.format_exc())
        raise

def index_data_in_elasticsearch(data):
    """Index data into Elasticsearch."""
    app.logger.info("Connecting to Elasticsearch.")
    try:
        es = Elasticsearch([ES_HOST])
        app.logger.info("Preparing data for bulk indexing.")
        actions = [
            {
                "_index": "city_council_meetings",
                "_source": record,
            }
            for record in data
        ]
        helpers.bulk(es, actions)
        app.logger.info(f"Successfully indexed {len(data)} records into Elasticsearch.")
    except Exception as e:
        app.logger.error(f"Error indexing data into Elasticsearch: {e}")
        app.logger.error(traceback.format_exc())
        raise

@app.route('/ingest', methods=['POST'])
def ingest_data():
    """Trigger ingestion from PostgreSQL to Elasticsearch."""
    app.logger.info("Ingestion request received.")
    try:
        app.logger.info("Fetching data from PostgreSQL.")
        data = fetch_data_from_postgres()
        app.logger.info("Indexing data into Elasticsearch.")
        index_data_in_elasticsearch(data)
        app.logger.info("Ingestion completed successfully.")
        return jsonify({"message": "Data successfully ingested.", "record_count": len(data)})
    except Exception as e:
        app.logger.error(f"Error during ingestion: {e}")
        app.logger.error(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

@app.route('/healthz', methods=['GET'])
def healthz():
    app.logger.info("Health check endpoint called.")
    return "OK", 200

if __name__ == '__main__':
    app.logger.info("Starting Flask application.")
    app.run(host='0.0.0.0', port=5000)
