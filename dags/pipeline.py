from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
import os

# --- IMPORT DE TA FONCTION D'ALERTE PERSONNALISÉE ---
from scripts.alerts import notify_dbt_failure

# 1. Gestion des chemins (Pathing)
AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', '/opt/airflow')
DBT_PROJECT_DIR = f"{AIRFLOW_HOME}/dbt_project/mon_analyse_olist"

# Ajout du dossier dags au chemin de recherche Python
DAG_FOLDER = os.path.dirname(os.path.abspath(__file__))
if DAG_FOLDER not in sys.path:
    sys.path.append(DAG_FOLDER)

# Import de ta fonction d'ingestion
from scripts.ingestion_data import load_to_postgres

# 2. Configuration par défaut
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=0.5),
}

# 3. Définition du DAG
with DAG(
    dag_id='pipeline', 
    default_args=default_args,
    description='Pipeline complet : Ingestion (Bronze) -> dbt (Silver & Gold)',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['olist', 'etl', 'dbt_sqlserver']
) as dag:

    # ÉTAPE 1 : Ingestion des CSV vers le schéma 'bronze' (Python)
    task_ingest = PythonOperator(
        task_id='ingest_csv_to_bronze',
        python_callable=load_to_postgres
    )

    # ÉTAPE 2 :
    task_dbt_silver = BashOperator(
        task_id='dbt_silver',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select silver --profiles-dir .',
    )

    # ÉTAPE 3 :
    task_dbt_gold = BashOperator(
        task_id='dbt_gold',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --select marts --profiles-dir .',
    )

    # ÉTAPE 4 : Tests de Qualité avec Alerte Email
    task_dbt_test = BashOperator(
        task_id='dbt_tests',
        bash_command=f'cd {DBT_PROJECT_DIR} && dbt test --profiles-dir .',
        # AJOUT DE L'ALERTE ICI
        on_failure_callback=notify_dbt_failure 
    )

task_ingest >> task_dbt_silver >> task_dbt_gold >> task_dbt_test