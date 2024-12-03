import requests
from datetime import datetime

PAGE_SIZE = 10000

def fetch_data(from_date: str, to_date: str):
    # Validate input dates
    if not validate_datetime(from_date) or not validate_datetime(to_date):
        raise ValueError("Invalid date format. Expected format: YYYY-MM-DDTHH:MM:SS.sssZ")
    
    csrf_url = 'https://secure.toronto.ca/council/api/csrf.json'
    url = "https://secure.toronto.ca/council/api/multiple/agenda-items.json"
    session = requests.Session()

    # GET request to obtain CSRF token
    response = session.get(csrf_url)
    response.raise_for_status()

    # Extract CSRF token from cookies
    cookies = session.cookies.get_dict()
    xsrf_token = cookies.get('XSRF-TOKEN')
    if not xsrf_token:
        raise Exception('XSRF token is missing')

    querystring = {"pageNumber": 0, "pageSize": PAGE_SIZE, "sortOrder": "meetingDate"}

    # Adjust payload as needed or accept parameters from the API endpoint
    payload = {
        "includeTitle": True,
        "includeSummary": True,
        "includeRecommendations": True,
        "includeDecisions": True,
        "meetingFromDate": from_date,
        "meetingToDate": to_date
    }
    headers = {
        "Content-Type": "application/json",
        "X-XSRF-TOKEN": xsrf_token
    }

    response = session.post(url, json=payload, headers=headers, params=querystring, cookies=cookies)
    response.raise_for_status()
    data = response.json()
    return data

def validate_datetime(datetime_string: str):
    try:
        datetime.strptime(datetime_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        return True
    except ValueError:
        return False
