import configparser
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import sql
import os

app = Flask(__name__)

# Add CORS support
CORS(app)

# Database connection details
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
search_api_port = os.getenv('SEARCH_API_PORT')
db_password = os.getenv('DB_PASSWORD')

def get_db_connection():
    """Create a database connection."""
    return psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

@app.route('/search', methods=['GET'])
def search():
    """Search the database for a term and return results."""
    search_term = request.args.get('term', '')

    # Connect to the database
    connection = get_db_connection()
    cursor = connection.cursor()

    # Query to retrieve search results with full-text search
    if search_term:
        query = sql.SQL("""
            SELECT *, ts_rank(to_tsvector('english', summary), to_tsquery('english', %s)) AS rank,
                   ts_headline('english', summary, to_tsquery('english', %s)) AS headline
            FROM agenda_items
            WHERE to_tsvector('english', summary) @@ to_tsquery('english', %s)
            ORDER BY rank DESC
            LIMIT 10;
        """)
        cursor.execute(query, (search_term, search_term, search_term))  # Provide the search term three times
    else:
        query = sql.SQL("""
            SELECT * FROM agenda_items LIMIT 10;
        """)
        cursor.execute(query)  # No parameters needed for this query

    results = cursor.fetchall()

    # Convert results to JSON
    columns = [desc[0] for desc in cursor.description]
    results_json = [dict(zip(columns, row)) for row in results]

    # Close the cursor and connection
    cursor.close()
    connection.close()

    return jsonify(results_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(search_api_port))
