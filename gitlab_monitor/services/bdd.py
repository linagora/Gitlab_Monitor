# # --- Copyright (c) 2024 Linagora
# # licence       : Apache 2.0
# # - Flavien Perez fperez@linagora.com
# # - Maïlys Jara mjara@linagora.com


from gitlab_monitor.services.models import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# TODO: variables a exportés en var d'env
db_user = "superset"
db_password = "superset"
db_host = "localhost" # TODO: VM name ou node name pour k8s ?
db_port = "5432"
db_name = "superset"

# TODO: poetry add psycopg2 - erreur
DB_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

class Database:

    def _initialize_database(self):
        # Créer un moteur de base de données
        print("get in initialize database function")
        engine = create_engine(DB_URL)

        try:
            connexion = engine.connect()
            print("Success !")

            # TODO: drop all à enlever une fois le process OK
            Base.metadata.drop_all(bind=engine)
            # Créer les tables dans la base de données
            Base.metadata.create_all(bind=engine)

            # Se connecte à la session de la base de donnée
            Session = sessionmaker(bind=engine)
            self.session = Session()

        except Exception as e:
            print(e)

    def get_session(self):
        return self.session
