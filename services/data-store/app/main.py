import psycopg2
import json
import os
import requests
from datetime import datetime, timedelta

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'your_db_name')
DB_USER = os.environ.get('DB_USER', 'your_db_user')
DB_PASSWORD = os.environ.get('postgres-password', 'your_db_password')
DB_PORT = os.environ.get('DB_PORT', '5432')

FETCHER_HOST = os.environ.get('FETCHER_HOST', 'data-fetcher-service')
FETCHER_PORT = os.environ.get('FETCHER_PORT', '5000')

def fetch_data_from_api(from_date: str, to_date: str):
    url = f'http://{FETCHER_HOST}:{FETCHER_PORT}/fetch-data'
    params = {
        'from_date': from_date,
        'to_date': to_date
    }
    response = requests.get(url, params=params, timeout=300)
    response.raise_for_status()
    data = response.json()
    return data

def insert_data_into_db(data):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cur = conn.cursor()

        insert_query = """
        INSERT INTO city_council_meetings (
            id, term_id, agenda_item_id, council_agenda_item_id, decision_body_id,
            meeting_id, item_process_id, decision_body_name, meeting_date, reference,
            term_year, agenda_cd, meeting_number, item_status, agenda_item_title,
            agenda_item_summary, agenda_item_recommendation, decision_recommendations,
            decision_advice, subject_terms, background_attachment_ids,
            agenda_item_address, addresses, geo_locations, ward_ids
        ) VALUES (
            %(id)s, %(termId)s, %(agendaItemId)s, %(councilAgendaItemId)s, %(decisionBodyId)s,
            %(meetingId)s, %(itemProcessId)s, %(decisionBodyName)s, to_timestamp(%(meetingDate)s / 1000), %(reference)s,
            %(termYear)s, %(agendaCd)s, %(meetingNumber)s, %(itemStatus)s, %(agendaItemTitle)s,
            %(agendaItemSummary)s, %(agendaItemRecommendation)s, %(decisionRecommendations)s,
            %(decisionAdvice)s, %(subjectTerms)s, %(backgroundAttachmentId)s,
            %(agendaItemAddress)s, %(address)s, %(geoLocation)s, %(wardId)s
        ) ON CONFLICT (reference) DO NOTHING
        """

        records = data.get('Records', [])
        for record in records:
            # Prepare the record
            record_prepared = {
                'id': record.get('id'),
                'termId': record.get('termId'),
                'agendaItemId': record.get('agendaItemId'),
                'councilAgendaItemId': record.get('councilAgendaItemId'),
                'decisionBodyId': record.get('decisionBodyId'),
                'meetingId': record.get('meetingId'),
                'itemProcessId': record.get('itemProcessId'),
                'decisionBodyName': record.get('decisionBodyName'),
                'meetingDate': record.get('meetingDate'),
                'reference': record.get('reference'),
                'termYear': record.get('termYear'),
                'agendaCd': record.get('agendaCd'),
                'meetingNumber': record.get('meetingNumber'),
                'itemStatus': record.get('itemStatus'),
                'agendaItemTitle': record.get('agendaItemTitle'),
                'agendaItemSummary': record.get('agendaItemSummary'),
                'agendaItemRecommendation': record.get('agendaItemRecommendation'),
                'decisionRecommendations': record.get('decisionRecommendations'),
                'decisionAdvice': record.get('decisionAdvice'),
                'subjectTerms': record.get('subjectTerms'),
                'backgroundAttachmentId': json.dumps(record.get('backgroundAttachmentId')),
                'agendaItemAddress': json.dumps(record.get('agendaItemAddress')),
                'address': json.dumps(record.get('address')),
                'geoLocation': json.dumps(record.get('geoLocation')),
                'wardId': json.dumps(record.get('wardId')),
            }
            cur.execute(insert_query, record_prepared)

        conn.commit()
        cur.close()
        conn.close()
        print(f"Inserted {len(records)} records into the database.")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return False

def main():
    try:
        # Example: Fetch data from yesterday to today
        today = datetime.utcnow()
        yesterday = today - timedelta(days=1)
        from_date = yesterday.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
        to_date = today.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

        data = fetch_data_from_api(from_date, to_date)
        print("Fetched data from API.")
        insert_data_into_db(data)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
