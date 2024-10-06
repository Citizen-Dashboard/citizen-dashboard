import bs4
from bs4 import Comment, NavigableString
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from validators import url
import re



class WebScraper:
    """
    A custom implementation of reusable webScraper that can be pre-configured with a strainer to extract from a webpage.

    Attributes:
        Strainer: A BeautifulSoup Strainer 
        https://www.crummy.com/software/BeautifulSoup/bs4/doc/#bs4.SoupStrainer
    """

    @property
    def strainer(self):
        return self.__strainer
    
    @strainer.setter
    def strainer(self, value:bs4.SoupStrainer):
        """Strainer is the selectors to extract from the web page"""

        if(not isinstance(value, bs4.SoupStrainer)):
            raise TypeError("strainer must be an instance of bs4.SoupStrainer")

        self.__strainer = value
    
    def scrapePage(self, pageUrl):
        self.validateURL(pageUrl)
        try:
            loader = WebBaseLoader(
                web_path=pageUrl,
                bs_kwargs=dict(
                    parse_only=self.__strainer
                )
            )

            # return loader.scrape('html.parser')
            return loader.scrape()
        except BaseException as err:
            print('Eror while trying to get document', err)
            raise Exception("Unable to fetch web document")
    

    def PageAsDocument(self, pageUrl):
        self.validateURL(pageUrl)

        loader = WebBaseLoader(
            web_path=pageUrl,
            bs_kwargs=dict(
                parse_only=self.__strainer
            )
        )

        loader.load()

    def validateURL(self, pageUrl):
        if(not url(pageUrl)):
            raise ValueError("pageUrl must be a valid URL")

        if(not self.__strainer):
            raise ValueError("Strainer is not initialized")
        




class tmmis_agenda_items_scraper:
    """Scrapes the Agenda items page and breaks down the page into list of agenda items"""
    def __init__(self, meetingReferenceNumber:str):
        self.__bot = WebScraper()
        # setup the strainer to return the entire html
        self.__bot.strainer = bs4.SoupStrainer(True)
        self.meetingReferenceNumber = meetingReferenceNumber
        self.__agendaItemsUrl = f"https://secure.toronto.ca/council/report.do?meeting={meetingReferenceNumber}&type=agenda"
        self.agendaItemsDocList = [] 
        self.agendaItemsTextList = []
    

    def getAgendaItems(self):
        """parses the Agenda Items from the meeting Agenda URL
        
        Attributes:
            pageUrl: The Agenda Item page URL
            meetingReferenceNumber: Meeting reference Number in the format <YYYY>.<CommitteeCode><MeetingNumber>
        """

        agendaItemHeadingPrefix = self.meetingReferenceNumber.split(".")[1]
        
        self.soup = self.__bot.scrapePage(self.__agendaItemsUrl)

        def agendaItemHeadingSelector(tag):
            return (isinstance(tag, bs4.Tag) 
                    and tag.name == "h3" 
                    and isinstance(tag.contents[0],NavigableString)
                    and re.search( f"^{agendaItemHeadingPrefix}\.[0-9]+\s+", tag.string) is not None)
        
        def agendaItemSectionHeadingSelector(tag):
            return (isinstance(tag, bs4.Tag) 
                    and tag.name == "h4" 
                    and isinstance(tag.contents[0],NavigableString))

        # traverse soup to find agenda items
        # Items start with h3. Content between two h3 tags are related to a single agenda item.
        # h4 tags within the agenda item denote the next subheading within the agenda
        #
        # Strategy:
        # get list of all h3Tags in the format <h3><YYYY>.<CommitteeCode><MeetingNumber> ...</h3>
        # Iterate through each h3Tag, add up text of all its next siblings until we find the next h3Tag.
        # this will be a single Agenda Item
        # Convert this to a string format prefixed with [Agenda Item].....[Agenda Item]
        
        h3Tags = self.soup.find_all(agendaItemHeadingSelector)
        
        for h3Tag in h3Tags:
            # agendaItemContent = f"[agendaItem]{h3Tag.string}"
            agendaItemContent = f"{h3Tag.string}"
            nextSibling = h3Tag.next_sibling
            while (nextSibling is not None and
                   not agendaItemHeadingSelector(nextSibling)):
                if(agendaItemSectionHeadingSelector(nextSibling)):
                    # agendaItemContent += f" [sectionHeading]{nextSibling.string}[SectionHeading]"
                    agendaItemContent += f" {nextSibling.string}"
                else:
                    agendaItemContent += ' '.join(map(str, nextSibling.stripped_strings))
                
                nextSibling = nextSibling.next_sibling

            agendaItemContent = f"{agendaItemContent}[agendaItem]"
            self.agendaItemsDocList.append(Document(
                page_content=agendaItemContent,
                metadata={
                    "source": self.__agendaItemsUrl, 
                    "meetingReferenceNumber":self.meetingReferenceNumber
                }
            ))
            self.agendaItemsTextList.append(agendaItemContent)
            # print(agendaItemContent)
        
        return (self.agendaItemsTextList, self.agendaItemsDocList)





