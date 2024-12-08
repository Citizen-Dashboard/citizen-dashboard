# app/main.py

from flask import Flask, jsonify, request

from data_fetcher import fetch_data, validate_datetime

app = Flask(__name__)

@app.route('/fetch-data', methods=['GET'])
def fetch_data_endpoint():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    # Validate input dates
    if not from_date or not to_date:
        return jsonify({'error': 'from_date and to_date parameters are required'}), 400

    if not validate_datetime(from_date) or not validate_datetime(to_date):
        return jsonify({'error': 'Invalid date format. Expected format: YYYY-MM-DDTHH:MM:SS.sssZ'}), 400

    try:
        data = fetch_data(from_date, to_date)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/healthz', methods=['GET'])
def healthz():
    return "OK", 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
