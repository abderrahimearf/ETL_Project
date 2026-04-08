import os
import shutil

def cleanup_old_logs(log_root="/opt/airflow/logs", keep_last_n=3):
    """
    Parcourt le dossier des logs et ne conserve que les N dernières 
    exécutions pour chaque tâche de chaque DAG.
    """
    if not os.path.exists(log_root):
        print(f"Le dossier {log_root} n'existe pas.")
        return

    # 1. Parcourir les dossiers des DAGs (ex: 'pipeline')
    for dag_id in os.listdir(log_root):
        dag_path = os.path.join(log_root, dag_id)
        if not os.path.isdir(dag_path):
            continue
            
        # 2. Parcourir les dossiers des Tasks (ex: 'dbt_silver')
        for task_id in os.listdir(dag_path):
            task_path = os.path.join(dag_path, task_id)
            if not os.path.isdir(task_path):
                continue
            
            # 3. Lister toutes les exécutions (run_id / dossiers de dates)
            runs = [os.path.join(task_path, r) for r in os.listdir(task_path)]
            runs = [r for r in runs if os.path.isdir(r)]
            
            # Trier par date de modification (les plus anciens au début)
            runs.sort(key=os.path.getmtime)
            
            # 4. Suppression si on dépasse la limite
            if len(runs) > keep_last_n:
                runs_to_delete = runs[:-keep_last_n]
                for run_path in runs_to_delete:
                    try:
                        shutil.rmtree(run_path)
                        print(f"Nettoyage : Log supprimé -> {run_path}")
                    except Exception as e:
                        print(f"Erreur lors de la suppression de {run_path}: {e}")
                        