from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

server = 'localhost'
database = 'Tier'
username = 'sa'
password = 'Admin123!'
driver = 'ODBC Driver 17 for SQL Server'
schema = "dbo"

# Création de l'URL de connexion
connection_url = URL.create(
    "mssql+pyodbc",
    username=username,
    password=password,
    host=server,
    database=database,
    query={
        "driver": driver,
        "TrustServerCertificate": "yes"
    }
)

try:
    # Création du moteur SQLAlchemy
    engine = create_engine(connection_url)

    # Ouverture de la connexion et exécution d'une requête de test
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1 AS test_connexion, DB_NAME() AS nom_base"))
        row = result.fetchone()

        print("Connexion réussie")
        print("Résultat test :", row.test_connexion)
        print("Base connectée :", row.nom_base)

except Exception as e:
    print("Erreur de connexion :", e)