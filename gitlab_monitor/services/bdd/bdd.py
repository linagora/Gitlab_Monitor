
# # --- Copyright (c) 2024 Linagora
# # licence       : GNU GENERAL PUBLIC LICENSE
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gitlab_monitor.services.bdd.models import Base


# Load and retrieve environment variables
load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

DB_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


class Database:

    def _initialize_database(self):
        # Create a database engine
        engine = create_engine(DB_URL)

        engine.connect()
        Base.metadata.create_all(bind=engine)

        # Connect to the database session
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_session(self):
        return self.session
