from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging

def verify_logging():
    logger = logging.getLogger("airflow.task")
    logger.info("Vérification PFE : Ceci est un log de test pour ELK !")
    logger.info("Si tu vois ce message dans Airflow, la lecture ES fonctionne.")
    return "Log envoyé avec succès"

with DAG(
    dag_id='test_elk_connection',
    start_date=datetime(2026, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    test_task = PythonOperator(
        task_id='verify_log_flow',
        python_callable=verify_logging
    )

