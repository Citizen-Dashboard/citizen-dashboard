from ctto_rag_demo.agenda_item_parser.topic_history_parser import topic_history_parser
from dotenv import load_dotenv

load_dotenv()

def test_html_retrieval():
    agendaItemRefNumbers = ["2024.EC14.1"]

    parser = topic_history_parser(agendaItemRefNumbers[0])

    parser.scrape() 