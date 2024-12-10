from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch
import os

app = Flask(__name__)

# Elasticsearch configuration
ES_HOST = os.getenv("ES_HOST", "localhost")
ES_PORT = os.getenv("ES_PORT", "9200")


@app.route('/search', methods=['GET'])
def search_data():
    """Search data in Elasticsearch."""
    es = Elasticsearch(f"http://{ES_HOST}:{ES_PORT}")
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Query parameter is required."}), 400

    try:
        response = es.search(
            index="city_council_meetings",
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["*"]
                    }
                }
            }
        )
        results = [
            {
                "id": hit["_id"],
                "source": hit["_source"]  # Remove truncation logic, include the full source
            }
            for hit in response['hits']['hits']
        ]
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/healthz', methods=['GET'])
def healthz():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
