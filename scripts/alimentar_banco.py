import pandas as pd
import sqlite3
import os
import random
from faker import Faker

# --- Inicialização e Definição de Caminhos ---
fake = Faker('pt_BR')
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CSV_PATH = os.path.join(PROJECT_ROOT, 'data', 'churn_kaggle.csv')
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'banco_churn.db')
TABLE_NAME = 'telco_churn'

def gerar_dados_randomicos(num_registros=100):
    """
    Gera uma lista de novos clientes com dados randômicos,
    seguindo a mesma estrutura do dataset do Kaggle.
    """
    novos_clientes = []
    for _ in range(num_registros):
        tenure = random.randint(1, 72)
        monthly_charges = round(random.uniform(18.0, 120.0), 2)
        
        cliente = {
            'customerID': fake.uuid4(),
            'gender': random.choice(['Male', 'Female']),
            'SeniorCitizen': random.choice([0, 1]),
            'Partner': random.choice(['Yes', 'No']),
            'Dependents': random.choice(['Yes', 'No']),
            'tenure': tenure,
            'PhoneService': random.choice(['Yes', 'No']),
            'MultipleLines': random.choice(['Yes', 'No', 'No phone service']),
            'InternetService': random.choice(['DSL', 'Fiber optic', 'No']),
            'OnlineSecurity': random.choice(['Yes', 'No', 'No internet service']),
            'OnlineBackup': random.choice(['Yes', 'No', 'No internet service']),
            'DeviceProtection': random.choice(['Yes', 'No', 'No internet service']),
            'TechSupport': random.choice(['Yes', 'No', 'No internet service']),
            'StreamingTV': random.choice(['Yes', 'No', 'No internet service']),
            'StreamingMovies': random.choice(['Yes', 'No', 'No internet service']),
            'Contract': random.choice(['Month-to-month', 'One year', 'Two year']),
            'PaperlessBilling': random.choice(['Yes', 'No']),
            'PaymentMethod': random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)']),
            'MonthlyCharges': monthly_charges,
            'TotalCharges': round(tenure * monthly_charges, 2),
            'Churn': random.choice(['Yes', 'No'])
        }
        novos_clientes.append(cliente)
    
    return pd.DataFrame(novos_clientes)

def carregar_dados_e_adicionar_randomicos():
    """
    Lê o CSV do Kaggle, gera dados randômicos, combina os dois
    e insere o resultado no banco de dados.
    """
    # 1. Carregar dados base do Kaggle
    if not os.path.exists(CSV_PATH):
        print(f"Erro: Arquivo CSV não encontrado em {CSV_PATH}")
        return
    print(f"Lendo dados base do arquivo: {CSV_PATH}")
    df_kaggle = pd.read_csv(CSV_PATH)
    
    # 2. Gerar novos dados randômicos
    num_novos_clientes = 500 # Você pode mudar este número
    print(f"Gerando {num_novos_clientes} novos registros randômicos...")
    df_random = gerar_dados_randomicos(num_novos_clientes)

    # 3. Combinar os dois DataFrames
    print("Combinando dados do Kaggle com os dados randômicos...")
    df_final = pd.concat([df_kaggle, df_random], ignore_index=True)
    
    # 4. Salvar o DataFrame final no banco de dados
    print(f"Conectando ao banco de dados: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    
    print(f"Carregando {len(df_final)} registros totais para a tabela '{TABLE_NAME}'...")
    # 'if_exists='replace'' garante uma carga limpa toda vez
    df_final.to_sql(TABLE_NAME, conn, if_exists='replace', index=False)
    
    conn.close()
    print("Dados combinados foram carregados com sucesso no banco de dados!")

if __name__ == "__main__":
    carregar_dados_e_adicionar_randomicos()