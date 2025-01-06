# # --- Copyright (c) 2024 Linagora
# # licence       : GPL v3
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com

"""Database module to manage the database connection."""

import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from gitlab_monitor.services.bdd.models import Base


# Load and retrieve environment variables
load_dotenv()
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
k8s_ip = os.getenv("K8S_IP")
k8s_port = os.getenv("K8S_PORT")
db_name = os.getenv("DB_NAME")

DB_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{k8s_ip}:{k8s_port}/{db_name}"


class Database:  # pylint: disable=too-few-public-methods
    """Initialize the database connection."""

    def __init__(self):
        """Constructor of the the database connection."""
        self._session = None

    def _initialize_database(self) -> Session:
        """Initialize the database connection."""
        # Create a database engine
        engine = create_engine(DB_URL)

        engine.connect()
        Base.metadata.create_all(bind=engine)

        # Connect to the database session
        session = sessionmaker(bind=engine)
        return session()

    @property
    def session(self) -> Session:
        """Property getter for the database session.

        This ensures that the database session is initialized before returning it.

        :return: the database session.
        :rtype: Session
        """
        if self._session is None:
            self._session = self._initialize_database()
            return self._session
        return self._session
