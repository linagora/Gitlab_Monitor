# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from services.models import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Database:

    def _initialize_database(self):
        # Créer un moteur de base de données
        DATABASE_URL = "postgresql://username:password@hostname:port/database_name"
        engine = create_engine(DATABASE_URL)

        # Créer les tables dans la base de données
        Base.metadata.create_all(engine)

        # Se connecte à la session de la base de donnée
        Session = sessionmaker(bind=engine)
        self.session = Session(engine)

    def get_session(self):
        return self.session
