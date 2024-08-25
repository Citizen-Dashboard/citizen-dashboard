import json
import os
import re
import logging

from sqlalchemy import create_engine, text, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

Base = declarative_base()

class AgendaItem(Base):
    __tablename__ = 'agenda_items'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True) 
    meeting_id = Column(String(50))
    vote = Column(String(10000), nullable=True)
    motions = Column(String(10000), nullable=True)
    background_info = Column(String(10000), nullable=True)
    decision = Column(String(10000), nullable=True)
    rulings = Column(String(10000), nullable=True)
    communications = Column(String(10000), nullable=True)
    speakers = Column(String(10000), nullable=True)
    origin = Column(String(10000), nullable=True)
    summary = Column(String(10000), nullable=True)
    recommendations = Column(String(10000), nullable=True)

class SqlDB:
    def __init__(self) -> None:
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_PORT = os.getenv('DB_PORT')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')

        self._connect_to_db()

        if os.getenv('CLEAN_DB'):
            AgendaItem.__table__.drop()

        self._create_db_if_needed()
        self._create_tables_if_needed()

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def _connect_to_db(self):
        self.engine = create_engine(f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    def _create_db_if_needed(self):
        if not database_exists(self.engine.url):
            logger.info(f"Database {self.engine.url} does not exist. Creating...")
            create_database(self.engine.url)
        else:
            logger.info(f"Found database {self.engine.url}. Moving on")

    def _create_tables_if_needed(self):
        AgendaItem.metadata.create_all(self.engine)

    def add_record(self, data):
        new_item = AgendaItem(meeting_id=data.get('meeting_id'),
                              vote=data.get('Vote'),
                              motions=data.get('Motions'),
                              background_info=data.get('Background Information'),
                              decision=data.get('Decision'),
                              rulings=data.get('Rulings'),
                              communications=data.get('Communications'),
                              speakers=data.get('Speakers'),
                              origin=data.get('Origin'),
                              summary=data.get('Summary'),
                              recommendations=data.get('Recommendations') )
        self.session.add(new_item)
        self.session.commit()

    def slugify(column_name):
        return re.sub(r'[^a-z0-9_]', '', column_name.lower().replace(' ', '_'))
