import requests
from datetime import datetime
import time
from bs4 import BeautifulSoup
import re
from app_logging.logger import File_Console_Logger

# Sample Agenda Item
# {
#             "id": "ID_136274",
#             "termId": 8,
#             "agendaItemId": 136274,
#             "councilAgendaItemId": 136274,
#             "decisionBodyId": 2744,
#             "meetingId": 24669,
#             "itemProcessId": 6,
#             "decisionBodyName": "Confronting Anti-Black Racism Advisory Committee",
#             "meetingDate": 1725422400000,
#             "reference": "2024.CR4.3",
#             "termYear": "2024",
#             "agendaCd": "CR",
#             "meetingNumber": "4",
#             "itemStatus": "RECEIVED",
#             "agendaItemTitle": "Data for Equity",
#             "agendaItemSummary": "<p>The purpose of the presentation is to provide an overview of the City&rsquo;s Data for Equity Strategy and share key components and information on the work, including a focus on Black Data Governance.</p>",
#             "agendaItemRecommendation": "",
#             "decisionRecommendations": "<p>The&nbsp;Confronting Anti-Black Racism Advisory Committee received the item for information.&nbsp;</p>",
#             "decisionAdvice": "<p>Debbie Burke-Benn, Director, Equity and Human Rights, People and Equity; Srijoni Rahman, Manager, Equity and Data for Equity Unit, People and Equity; Jemal Demeke, Researcher, Wellesley Institute; and Fiqir Worku, Researcher, Black Health Alliance, gave a presentation on&nbsp;Data for Equity.</p>",
#             "subjectTerms": "boards of management, committee meetings, equity; boards of directors; boards of governors, employment equity; fair wage; pay equity",
#             "backgroundAttachmentId": [
#                 248116,
#                 248471
#             ],
#             "agendaItemAddress": []
#         }

logger = File_Console_Logger(__name__)


class adgendaItemFetcher:

    def __init__(self):
        """Initializes the object with necessary attributes and performs operations to obtain CSRF token.
        
        In this method:
        - Initializes the CSRF URL and agenda item URL.
        - Creates a session with custom headers.
        - Sends a GET request to obtain the CSRF token.
        - Extracts the CSRF token from the response cookies.
        - Sets the session validity based on the presence of the CSRF token.
        - Raises an exception if the CSRF token is missing.
        """
        
        csrf_url = 'https://secure.toronto.ca/council/api/csrf.json'
        self.agenda_item_url = "https://secure.toronto.ca/council/api/multiple/agenda-items.json"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'})
        self.sessionValid = True

        # GET request to obtain CSRF token
        response = self.session.get(csrf_url)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract CSRF token from cookies
        cookies = self.session.cookies.get_dict()
        self.xsrf_token = cookies.get('XSRF-TOKEN')  
        if not self.xsrf_token:
            self.sessionValid = False
            raise Exception('XSRF token is missing')



    def _fetchAgendaItems(self,meetingsFromDateUTC:datetime, meetingToDateUTC:datetime, pageNumber:int=1):
        """Fetch agenda items for a given date range and page number.
        
        Args:
            meetingsFromDateUTC (datetime): The start date for fetching agenda items.
            meetingToDateUTC (datetime): The end date for fetching agenda items.
            pageNumber (int, optional): The page number to fetch agenda items from. Defaults to 1.
        
        Returns:
            dict: A dictionary containing the fetched agenda items.
        
        Raises:
            Exception: If there is an error while fetching agenda items.
        """
        
        try:
            meetingsFromDateUTC = meetingsFromDateUTC.replace(hour=0, minute=0, second=0, microsecond=0)
            meetingToDateUTC = meetingToDateUTC.replace(hour=0, minute=0, second=0, microsecond=0)
            logger.debug(f"Fetching agenda Items page:{pageNumber} for date range {meetingsFromDateUTC} - {meetingToDateUTC}")
            querystring = {"pageNumber":pageNumber,"pageSize":200,"sortOrder":"meetingDate"}
            
            payload = {
                "includeTitle": "True",
                "includeSummary": "True",
                "includeRecommendations": "True",
                "includeDecisions": "True",
                "meetingFromDate": meetingsFromDateUTC.strftime("%Y-%m-%dT%H:%M:%S%z"),
                "meetingToDate": meetingToDateUTC.strftime("%Y-%m-%dT%H:%M:%S%z")
            }
            headers = {
                "Content-Type": "application/json",
                "X-XSRF-TOKEN": self.xsrf_token,
                "content-type": "application/json"
            }
        
        except Exception as e:
            logger.error("Exception while trying to build payload:", e)
            raise(e)

        try:
            req = requests.Request("POST", self.agenda_item_url, headers=headers, json=payload, params=querystring)
            prepared = self.session.prepare_request(req)
            # self._pretty_print_POST(prepared)

            response = self.session.send(prepared)

            # print(response.json())
            return response.json()
        except Exception as e:
            logger.error("Exception while fetching agenda items:", e)
            raise(e)


    def getAgendaItems(self,meetingsFromDateUTC:datetime, meetingToDateUTC:datetime):
        """Fetches agenda items for meetings within a specified date range.
        
        In this method:
        - Initializes variables for tracking pagination and storing agenda items.
        - Iterates through pages of agenda items until all pages are fetched.
            Wait 1 second between each page to avoid getting rate limited.
        - Consolidates agenda items from each page into a single list.
        
        Args:
            meetingsFromDateUTC (datetime): The start date for fetching agenda items.
            meetingToDateUTC (datetime): The end date for fetching agenda items.
        
        Returns:
            list: A list of agenda items fetched within the specified date range.
        """
        
        
        
        nextPage=-1
        hasNextPage = True
        agendaItemsList = []
        meetingsFromDateUTC = meetingsFromDateUTC.replace(hour=0, minute=0, second=0, microsecond=0)
        meetingToDateUTC = meetingToDateUTC.replace(hour=0, minute=0, second=0, microsecond=0)
        logger.info(f"Fetching agenda Items for date range {meetingToDateUTC.isoformat()} - {meetingToDateUTC.isoformat()}")
        
        while hasNextPage:
            nextPage+=1
            # sleep 1 second so we don't get rate limited
            time.sleep(1)
            resp = self._fetchAgendaItems(meetingsFromDateUTC, meetingToDateUTC, nextPage)
            
            #check if response is valid
            if(resp.get("Result") == "OK"):
                records = resp.get("Records")
                logger.debug(f"Fetched Page {nextPage} with {len(records)} records")
                totalPages = resp.get("TotalPages")
                hasNextPage= True if (totalPages>nextPage+1) else False 
                # sanitize agenda items by calling _cleanAgendaItem method    
                cleanedAgendaItems = [self._cleanAgendaItem(item) for item in records]
                logger.debug(f"Sanitized {len(records)} agenda items")
                #consolidate agenda Items
                agendaItemsList.extend(cleanedAgendaItems)
            else:
                logger.error("Error Occurred while fetching agenda Items Page {0}. Recieved response status {1}".format(nextPage, resp.get("Result")))
                hasNextPage=False

        logger.info(f"Fetched {len(agendaItemsList)} agenda items for date range {meetingsFromDateUTC} - {meetingToDateUTC}")
        return agendaItemsList
    
    def _cleanAgendaItem(self, agendaItem):
        keysToKeep = {'id', 'agendaItemId', 'decisionBodyId', 'decisionBodyName', 'meetingId', \
                      'meetingDate', 'reference','termYear', 'agendaCd', 'itemStatus','agendaItemTitle', \
                       'agendaItemSummary', 'agendaItemRecommendation', 'decisionRecommendations', 'decisionAdvice', 'subjectTerms','wardId'}
        cleanedAgendaItem = new_dict = {k: v for k, v in agendaItem.items() if k in keysToKeep}
        
        # # convert timestamp to iso datetime format
        # cleanedAgendaItem["meetingDate"] = datetime.fromtimestamp(agendaItem["meetingDate"]/1000).strftime("%Y-%m-%dT%H:%M:%S%z")
        
        #convert html text fields to plain text fields 
        if "agendaItemSummary" in agendaItem:
            cleanedAgendaItem["agendaItemSummary"] = self._html_to_plain_text(agendaItem["agendaItemSummary"])
        if "agendaItemRecommendation" in agendaItem:
            cleanedAgendaItem["agendaItemRecommendation"] = self._html_to_plain_text(agendaItem["agendaItemRecommendation"])
        if "decisionRecommendations" in agendaItem:
            cleanedAgendaItem["decisionRecommendations"] = self._html_to_plain_text(agendaItem["decisionRecommendations"])
        if "decisionAdvice" in agendaItem:
            cleanedAgendaItem["decisionAdvice"] = self._html_to_plain_text(agendaItem["decisionAdvice"])
        if "subjectTerms" in agendaItem:
            cleanedAgendaItem["subjectTerms"] = self._html_to_plain_text(agendaItem["subjectTerms"])

        return cleanedAgendaItem


    def _html_to_plain_text(self, html_text):
        """
        Convert HTML text to plain text.

        Args:
            html_text (str): The HTML text to convert.

        Returns:
            str: The plain text version of the input HTML.
        """
        soup = BeautifulSoup(html_text, 'html.parser')
        plain_text = soup.get_text(separator=' ')
        return re.sub(r'\s+', ' ', plain_text).strip()
    
            
    def _pretty_print_POST(self, req):
        """Prints the POST request in a formatted manner.
        
            In this method:
            - Concatenates the request method and URL.
            - Formats and joins the request headers.
            - Prints the request body.
        
            Args:
                req: The POST request object to be printed.
        """
        
        
        
        print('{}\n{}\r\n{}\r\n\r\n{}'.format(
            '-----------START-----------',
            req.method + ' ' + req.url,
            '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
            req.body,
        ))