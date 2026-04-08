from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Gestion des chemins pour importer ton script
AIRFLOW_HOME = os.getenv('AIRFLOW_HOME', '/opt/airflow')
sys.path.append(AIRFLOW_HOME)

# Import de la fonction depuis ton nouveau script
from scripts.log_management import cleanup_old_logs

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
with DAG(
    dag_id='maintenance_cleanup_logs',
    default_args=default_args,
    description='Nettoyage automatique : garde les 3 derniers logs par tâche',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily', # Se lance une fois par jour à minuit
    catchup=False,
    tags=['maintenance', 'logs']
) as dag:

    task_cleanup = PythonOperator(
        task_id='cleanup_airflow_logs',
        python_callable=cleanup_old_logs,
        op_kwargs={'log_root': f"{AIRFLOW_HOME}/logs", 'keep_last_n': 3}
    )
