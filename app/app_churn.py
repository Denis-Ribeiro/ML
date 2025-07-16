import streamlit as st
import pandas as pd
import joblib
import os
from datetime import datetime

# --- Configuração da Página ---
st.set_page_config(page_title="Previsor de Churn Telco", layout="wide")

# --- Carregar Modelo e Colunas ---
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'modelo.pkl')

@st.cache_resource
def carregar_modelo():
    try:
        data = joblib.load(MODEL_PATH)
        
        # Pega a data de modificação do arquivo do modelo
        mod_time = os.path.getmtime(MODEL_PATH)
        model_date = datetime.fromtimestamp(mod_time).strftime('%d/%m/%Y às %H:%M:%S')

        return data['model'], data['columns'], model_date
    except FileNotFoundError:
        st.error("Arquivo do modelo não encontrado. Execute o pipeline de treinamento primeiro.")
        return None, None, None

model, model_columns, model_date = carregar_modelo()

# --- Barra Lateral (Sidebar) ---
st.sidebar.title("Sobre o Modelo")
if model_date:
    st.sidebar.info(f"Modelo treinado em: \n**{model_date}**")

# --- Interface da Aplicação ---
st.title("Previsão de Churn de Clientes (Dataset Kaggle)")
st.write("Insira os detalhes do cliente para prever a probabilidade de churn.")
st.write("---")

if model is not None:
    # --- Coleta de Dados do Usuário ---
    st.header("Informações do Cliente")
    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox("Gênero", ("Male", "Female"))
        senior_citizen = st.selectbox("Cliente Idoso (Senior Citizen)?", ("No", "Yes"))
        partner = st.selectbox("Possui Parceiro(a)?", ("No", "Yes"))
        dependents = st.selectbox("Possui Dependentes?", ("No", "Yes"))

    with col2:
        tenure = st.slider("Tempo de Contrato (Meses)", 1, 72, 24)
        phone_service = st.selectbox("Serviço de Telefone?", ("No", "Yes"))
        internet_service = st.selectbox("Serviço de Internet", ("DSL", "Fiber optic", "No"))
        contract = st.selectbox("Tipo de Contrato", ("Month-to-month", "One year", "Two year"))

    with col3:
        paperless_billing = st.selectbox("Fatura Digital (Paperless Billing)?", ("No", "Yes"))
        payment_method = st.selectbox("Método de Pagamento", 
                                     ("Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"))
        monthly_charges = st.number_input("Cobrança Mensal", 0.0, 150.0, 70.0)
        total_charges = tenure * monthly_charges # Estimativa simples

    # --- Lógica de Previsão ---
    if st.button("Prever Churn", type="primary"):
        # ... (código da previsão continua o mesmo) ...
        input_dict = {
            'gender': [gender], 'SeniorCitizen': [1 if senior_citizen == 'Yes' else 0],
            'Partner': [partner], 'Dependents': [dependents], 'tenure': [tenure],
            'PhoneService': [phone_service], 'PaperlessBilling': [paperless_billing],
            'MonthlyCharges': [monthly_charges], 'TotalCharges': [total_charges],
            'InternetService': [internet_service], 'Contract': [contract],
            'PaymentMethod': [payment_method]
        }
        df_input = pd.DataFrame(columns=model_columns); df_input.loc[0] = 0
        temp_df = pd.DataFrame(input_dict); temp_df = pd.get_dummies(temp_df, drop_first=True)
        for col in temp_df.columns:
            if col in df_input.columns:
                df_input[col] = temp_df[col]
        prediction = model.predict(df_input); prediction_proba = model.predict_proba(df_input)
        st.write("---")
        st.header("Resultado da Previsão")
        if prediction[0] == 1:
            st.error(f"Previsão: **Churn (Sim)** | Probabilidade: {prediction_proba[0][1]:.2%}")
        else:
            st.success(f"Previsão: **Não Churn (Não)** | Probabilidade: {prediction_proba[0][0]:.2%}")