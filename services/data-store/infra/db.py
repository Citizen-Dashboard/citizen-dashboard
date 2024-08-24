import json
import os
import re
import logging

from sqlalchemy import create_engine, text, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

Base = declarative_base()

class AgendaItem(Base):
    __tablename__ = 'agenda_items'  # The name of the table in PostgreSQL

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)  # Primary key with an auto-incrementing sequence
    name = Column(String(50), nullable=False)  # String column with a max length of 50, not nullable
    email = Column(String(100), nullable=False, unique=True)  # String column with a max length of 100, not nullable and unique


class SQLDB:
    def __init__(self) -> None:
        self.DB_NAME = os.getenv('DB_NAME')
        self.DB_USER = os.getenv('DB_USER')
        self.DB_HOST = os.getenv('DB_HOST')
        self.DB_PORT = os.getenv('DB_PORT')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD')

        self._connect_to_db()

        self._create_tables_if_needed()

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def _connect_to_db(self):
        self.engine = create_engine(f'postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    def _create_tables_if_needed(self):
        Base.metadata.create_all(self.engine)

    def add_record(self, name, email):
        new_user = AgendaItem(name=name, email=email)
        self.session.add(new_user)
        self.session.commit()

    def slugify(column_name):
        return re.sub(r'[^a-z0-9_]', '', column_name.lower().replace(' ', '_'))
