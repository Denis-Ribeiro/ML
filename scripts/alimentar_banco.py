import pandas as pd
import sqlite3
import os

# --- Definição dos Caminhos ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_PATH = os.path.join(PROJECT_ROOT, 'data', 'churn_kaggle.csv')
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'banco_churn.db')
TABLE_NAME = 'telco_churn' # Nome da tabela correta

def carregar_dados_do_kaggle_para_db():
    """
    Lê o arquivo CSV do Kaggle e o insere em uma tabela no banco de dados SQLite.
    Substitui a tabela se ela já existir para garantir dados limpos.
    """
    if not os.path.exists(CSV_PATH):
        print(f"Erro: Arquivo CSV não encontrado em {CSV_PATH}")
        return

    print(f"Lendo dados do arquivo: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)

    print(f"Conectando ao banco de dados: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    print(f"Carregando dados para a tabela '{TABLE_NAME}'...")
    df.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)

    conn.close()
    print("Dados carregados com sucesso no banco de dados!")

if __name__ == "__main__":
    carregar_dados_do_kaggle_para_db()