FROM apache/airflow:2.11.0-python3.10

USER root
# Installation des dépendances système nécessaires pour PostgreSQL et dlt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential libpq-dev gcc curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER airflow
WORKDIR /opt/airflow

# Mise à jour de pip
RUN pip install --no-cache-dir --upgrade pip

# Installation des dépendances du projet uniquement
COPY --chown=airflow:root requirements.txt /requirements.txt
RUN curl -sSL "https://raw.githubusercontent.com/apache/airflow/constraints-2.11.0/constraints-3.10.txt" -o /tmp/constraints.txt && \
    pip install --no-cache-dir \
        --constraint /tmp/constraints.txt \
        -r /requirements.txt

ENV PATH="/home/airflow/.local/bin:${PATH}"