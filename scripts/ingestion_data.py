import os
import csv
import logging
import traceback
import dlt
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("OlistBulkLoader")


POSTGRES_HOST = "host.docker.internal"
POSTGRES_PORT = "5432"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "admin"
DATABASE_TARGET = "Olist"
SCHEMA_TARGET = "bronze"
DATA_FOLDER = "/opt/airflow/data"

def normalize_name(name: str) -> str:
    """Nettoie le nom du fichier pour créer un nom de table propre."""
    table_name = (
        name.replace(".csv", "")
        .replace("olist_", "")
        .replace("_dataset", "")
        .lower()
    )
    if "category_name_translation" in table_name:
        table_name = "product_category_translation"
    return table_name

def csv_rows(path: str):
    """Générateur qui lit le CSV ligne par ligne."""
    try:
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                yield row
    except Exception as e:
        logger.error(f"❌ Erreur lors de la lecture du fichier {path}: {str(e)}")
        raise

def load_to_postgres():
    start_time = datetime.now()
    logger.info(f"🚀 Lancement du Pipeline DLT | Cible: {DATABASE_TARGET}.{SCHEMA_TARGET}")

    try:
        # Construction de la chaîne de connexion
        credentials = (
            f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
            f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{DATABASE_TARGET}"
        )

        # Configuration de la convention de nommage directe
        os.environ["NAMING_CONVENTION"] = "direct"

        # Initialisation du pipeline
        pipeline = dlt.pipeline(
            pipeline_name="olist_bulk_loader",
            destination="postgres",
            dataset_name=SCHEMA_TARGET
        )

        # 1. Préparation des ressources
        if not os.path.exists(DATA_FOLDER):
            logger.error(f"📂 Le dossier de données {DATA_FOLDER} est introuvable !")
            return

        files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
        logger.info(f"🔍 {len(files)} fichiers CSV détectés dans {DATA_FOLDER}")

        all_resources = []
        for file in files:
            table_name = normalize_name(file)
            path = os.path.join(DATA_FOLDER, file)
            
            logger.info(f"📦 Création de la ressource DLT pour la table: '{table_name}'")

            def get_rows(p=path):
                yield from csv_rows(p)

            resource = dlt.resource(
                get_rows, 
                name=table_name, 
                write_disposition="replace"
            )
            all_resources.append(resource)

        # 2. Exécution du chargement
        logger.info("⚡ Début de l'injection batch (bulk load) vers Postgres...")
        load_info = pipeline.run(
            all_resources,
            credentials=credentials
        )
        
        # 3. Monitoring des résultats (Post-Load Analysis)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        logger.info("--- RAPPORT D'INGESTION ---")
        logger.info(f"✅ Statut final: SUCCESS")
        logger.info(f"⏱️ Durée totale: {duration:.2f} secondes")
        
        # Log simple
        logger.info("📥 Chargement terminé avec succès")
        
        # Log détaillé (utile pour le debug profond)
        logger.debug(f"Détails techniques DLT: {load_info}")

    except Exception as e:
        logger.critical("🚨 ERREUR FATALE LORS DE L'INGESTION")
        logger.error(f"Détails de l'exception: {str(e)}")
        logger.error(traceback.format_exc())
        # On relève l'erreur pour qu'Airflow marque la tâche en rouge (FAILED)
        raise e

if __name__ == "__main__":
    load_to_postgres()