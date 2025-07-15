from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sqlite3
import pandas as pd
import sys
import os

# Adiciona o diretório de scripts ao Python path para importar nossos módulos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'scripts'))

from treinar_modelo import treinar_modelo

# Define os caminhos relativos à localização do arquivo da DAG
DAGS_FOLDER = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(DAGS_FOLDER, '..', '..'))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'banco_churn.db')
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'dados_churn_para_ml.csv')

def tarefa_etl():
    """Extrai dados do SQLite e os salva como CSV."""
    print(f"Conectando ao banco de dados em {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    
    # Lê os dados da tabela de clientes para um DataFrame do pandas
    df = pd.read_sql_query("SELECT * FROM clientes", conn)
    conn.close()

    # Garante que o diretório de destino exista
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    
    # Salva o DataFrame em um arquivo CSV
    df.to_csv(DATA_PATH, index=False)
    print(f"Dados extraídos e salvos em {DATA_PATH}")

# Argumentos padrão para a DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 7, 1),
    'retries': 1,
}

with DAG(
    'pipeline_churn_clientes',
    default_args=default_args,
    description='Um pipeline de ML de ponta a ponta para previsão de churn',
    schedule_interval='@daily',  # Isso significa que o pipeline é executado uma vez por dia
    catchup=False,
) as dag:

    etl = PythonOperator(
        task_id='executar_etl',
        python_callable=tarefa_etl,
    )

    treinamento = PythonOperator(
        task_id='executar_treinamento_modelo',
        python_callable=treinar_modelo, # Chama a função do nosso script
    )

    # Define a dependência das tarefas: ETL deve ser executado antes do treinamento
    etl >> treinamento