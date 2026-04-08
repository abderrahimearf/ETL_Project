from airflow.utils.email import send_email
from datetime import datetime

def notify_dbt_failure(context):
    """
    Fonction de rappel (callback) pour envoyer un email personnalisé 
    en cas d'échec d'un test dbt.
    """
    # Extraction des métadonnées du contexte Airflow
    dag_id = context.get('dag').dag_id
    task_id = context.get('task_instance').task_id
    log_url = context.get('task_instance').log_url
    execution_date = context.get('execution_date').strftime('%d/%m/%Y %H:%M:%S')
    exception = context.get('exception')

    # Destinataire (Mets ton email ici)
    recipient = "chaatoufilyas03@gmail.com"
    
    subject = f"⚠️ ALERTE QUALITÉ DATA : Échec sur {dag_id}"

    # Corps de l'email en HTML
    html_content = f"""
    <div style="font-family: Arial, sans-serif; border: 1px solid #dcdcdc; padding: 20px;">
        <h2 style="color: #d9534f;">🚨 Rapport d'échec du Pipeline Olist</h2>
        <p>Le monitoring a détecté une anomalie lors de l'exécution des tests de qualité.</p>
        
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Pipeline (DAG)</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{dag_id}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Tâche en échec</td>
                <td style="padding: 8px; border: 1px solid #ddd; color: #d9534f;">{task_id}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border: 1px solid #ddd; font-weight: bold;">Date d'exécution</td>
                <td style="padding: 8px; border: 1px solid #ddd;">{execution_date}</td>
            </tr>
        </table>

        <h3 style="color: #333;">Détails de l'erreur :</h3>
        <div style="background-color: #f8f9fa; padding: 10px; border-left: 5px solid #d9534f;">
            <code>{exception}</code>
        </div>

        <p style="margin-top: 20px;">
            <a href="{log_url}" style="background-color: #0275d8; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Consulter les logs complets sur Airflow
            </a>
        </p>
        
        <hr style="margin-top: 30px;">
        <p style="font-size: 12px; color: #777;">
            <i>Ceci est un message automatique généré par le système de Monitoring Olist (Stack ELK + Airflow).</i>
        </p>
    </div>
    """

    # Envoi de l'email
    send_email(to=recipient, subject=subject, html_content=html_content)