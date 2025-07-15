import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os

# --- Definição dos Caminhos ---
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'dados_churn_para_ml.csv')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'app', 'modelo.pkl')
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

def treinar_modelo():
    """Carrega os dados do Kaggle, treina um modelo e o salva."""
    print("Lendo dados para treinamento...")
    df = pd.read_csv(DATA_PATH)

    # --- Pré-processamento Específico para o Dataset Telco ---
    # A coluna TotalCharges tem espaços em branco para clientes novos.
    # Convertemos para numérico, e os espaços se tornarão NaN (Not a Number).
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    
    # Removemos as linhas com valores faltando (NaN)
    df.dropna(inplace=True)

    # Removemos o ID do cliente (customerID), que não é útil para o modelo
    df = df.drop('customerID', axis=1)

    # Convertendo a coluna alvo 'Churn' para 0 e 1
    le = LabelEncoder()
    df['Churn'] = le.fit_transform(df['Churn'])

    # Convertendo todas as outras colunas categóricas em numéricas usando One-Hot Encoding
    df = pd.get_dummies(df, drop_first=True)

    # --- Treinamento do Modelo ---
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Treinando o modelo RandomForest...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # --- Avaliação ---
    y_pred = model.predict(X_test)
    print(f"Acurácia do Modelo: {accuracy_score(y_test, y_pred):.4f}")

    # --- Salva o Modelo e as Colunas ---
    # É crucial salvar as colunas que o modelo espera receber!
    model_data = {'model': model, 'columns': X.columns}
    joblib.dump(model_data, MODEL_PATH)
    print(f"Modelo e colunas salvos em {MODEL_PATH}")

if __name__ == "__main__":
    treinar_modelo()