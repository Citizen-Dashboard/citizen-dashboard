from flask import Flask, jsonify, request
import psycopg2
from elasticsearch import Elasticsearch, helpers
import os

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
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM city_council_meetings;")
    columns = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

def index_data_in_elasticsearch(data):
    """Index data into Elasticsearch."""
    es = Elasticsearch([ES_HOST])
    actions = [
        {
            "_index": "city_council_meetings",
            "_source": record,
        }
        for record in data
    ]
    helpers.bulk(es, actions)

@app.route('/ingest', methods=['POST'])
def ingest_data():
    """Trigger ingestion from PostgreSQL to Elasticsearch."""
    try:
        data = fetch_data_from_postgres()
        index_data_in_elasticsearch(data)
        return jsonify({"message": "Data successfully ingested.", "record_count": len(data)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/healthz', methods=['GET'])
def healthz():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
