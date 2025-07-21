import sqlite3
import pandas as pd
import os
import sys
from datetime import datetime
import git # Importa a biblioteca GitPython

# Importa as funções dos outros scripts
from alimentar_banco import carregar_dados_e_adicionar_randomicos
from treinar_modelo import treinar_modelo

# --- CONFIGURAÇÕES DO PROJETO ---
# 1. Coloque a URL do seu repositório GitHub aqui
GITHUB_REPO_URL = "https://github.com/Denis-Ribeiro/ML"

# 2. Definição dos Caminhos
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'banco_churn.db')
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'dados_churn_para_ml.csv')


# --- Funções do Pipeline ---

def tarefa_alimentar_banco():
    """Executa a alimentação e geração de dados."""
    print("--- INICIANDO TAREFA DE ALIMENTAÇÃO DO BANCO ---")
    try:
        carregar_dados_e_adicionar_randomicos()
        print("--- TAREFA DE ALIMENTAÇÃO DO BANCO CONCLUÍDA ---")
        return True
    except Exception as e:
        print(f"Erro durante a alimentação do banco: {e}")
        return False

def tarefa_etl():
    """Tarefa de ETL: Extrai dados do SQLite e salva como CSV."""
    print("\n--- INICIANDO TAREFA DE ETL ---")
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
    """Tarefa de Treinamento: Chama a função para treinar o modelo."""
    print("\n--- INICIANDO TAREFA DE TREINAMENTO ---")
    try:
        treinar_modelo()
        print("--- TAREFA DE TREINAMENTO CONCLUÍDA ---")
        return True
    except Exception as e:
        print(f"Erro durante o treinamento: {e}")
        return False

def tarefa_git_push():
    """Adiciona, commita e envia TODAS as alterações do projeto para a URL do GitHub definida no código."""
    print("\n--- INICIANDO TAREFA DE DEPLOY NO GITHUB ---")
    try:
        repo = git.Repo(PROJECT_ROOT)
        
        # Garante que o 'origin' aponta para a URL correta
        if 'origin' in repo.remotes:
            origin = repo.remotes.origin
            if origin.url != GITHUB_REPO_URL:
                origin.set_url(GITHUB_REPO_URL)
                print(f"URL do 'origin' atualizada para: {GITHUB_REPO_URL}")
        else:
            origin = repo.create_remote('origin', GITHUB_REPO_URL)
            print(f"Repositório remoto 'origin' criado para: {GITHUB_REPO_URL}")
        
        # --- MUDANÇA PRINCIPAL AQUI ---
        # Adiciona TODAS as alterações (novos arquivos, modificações, exclusões) ao staging
        repo.git.add(all=True)
        
        # Cria uma mensagem de commit com data e hora
        commit_message = f"Atualização do projeto via pipeline - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        if repo.is_dirty(untracked_files=True):
            repo.index.commit(commit_message)
            print(f"Commit criado: '{commit_message}'")
            
            origin.push()
            print("Push para o GitHub realizado com sucesso!")
            print("--- TAREFA DE DEPLOY NO GITHUB CONCLUÍDA ---")
        else:
            print("Nenhuma alteração no projeto para commitar. Deploy não necessário.")

    except Exception as e:
        print(f"Erro durante o deploy no GitHub: {e}")

# --- Execução Principal do Pipeline Completo ---
if __name__ == "__main__":
    print("=================================================")
    print("INICIANDO PIPELINE DE MACHINE LEARNING DE PONTA A PONTA")
    print("=================================================")
    
    if tarefa_alimentar_banco():
        if tarefa_etl():
            if tarefa_treinamento():
                tarefa_git_push()
            
    print("\n=================================================")
    print("PIPELINE FINALIZADO.")
    print("=================================================")