import sqlite3
import pandas as pd
import os
from treinar_modelo import treinar_modelo # Importa a função do outro script

# --- Definição dos Caminhos ---
# Obtém o diretório raiz do projeto de forma dinâmica
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'banco_churn.db')
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'dados_churn_para_ml.csv')

def tarefa_etl():
    """
    Tarefa de ETL: Extrai dados do SQLite, transforma (se necessário) e salva como CSV.
    """
    print("--- INICIANDO TAREFA DE ETL ---")
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM telco_churn", conn)
        conn.close()

        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        df.to_csv(DATA_PATH, index=False)
        print(f"Dados extraídos com sucesso para: {DATA_PATH}")
        print("--- TAREFA DE ETL CONCLUÍDA ---")
        return True
    except Exception as e:
        print(f"Erro durante o ETL: {e}")
        return False

def tarefa_treinamento():
    """
    Tarefa de Treinamento: Chama a função para treinar o modelo de machine learning.
    """
    print("\n--- INICIANDO TAREFA DE TREINAMENTO ---")
    try:
        treinar_modelo()
        print("--- TAREFA DE TREINAMENTO CONCLUÍDA ---")
    except Exception as e:
        print(f"Erro durante o treinamento: {e}")

# --- Execução Principal ---
if __name__ == "__main__":
    print("Iniciando o pipeline de Machine Learning...")
    
    # Executa a tarefa de ETL primeiro
    if tarefa_etl():
        # Se o ETL for bem-sucedido, executa o treinamento
        tarefa_treinamento()
        
    print("\nPipeline finalizado.")