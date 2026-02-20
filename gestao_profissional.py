import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="CVL8 - Gestão Profissional",
    layout="wide"
)

# ====== ESTILO PERSONALIZADO ======
st.markdown("""
<style>
.stApp {
    background-color: #f5f5f5;
}

.logo-container {
    text-align: center;
    margin-bottom: 20px;
}

.titulo {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: #c9a227;
}

.subtitulo {
    text-align: center;
    color: gray;
    margin-bottom: 40px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# ====== TOPO COM MARCA ======
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image("logo.png", width=200)
st.markdown('<div class="titulo">CVL8 - Gestão Profissional</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitulo">Sistema de Controle Estratégico</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ====== INICIALIZAR DADOS ======
if "dados" not in st.session_state:
    st.session_state.dados = pd.DataFrame(columns=["Data", "Descrição", "Valor"])

# ====== FORMULÁRIO ======
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("Adicionar Registro")

data = st.date_input("Data", datetime.today())
descricao = st.text_input("Descrição")
valor = st.number_input("Valor", step=1.0)

if st.button("Salvar"):
    novo = pd.DataFrame([[data, descricao, valor]],
                        columns=["Data", "Descrição", "Valor"])
    st.session_state.dados = pd.concat(
        [st.session_state.dados, novo],
        ignore_index=True
    )
    st.success("Registro salvo com sucesso!")

st.markdown('</div>', unsafe_allow_html=True)

# ====== TABELA ======
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("Registros")

st.dataframe(st.session_state.dados, use_container_width=True)

total = st.session_state.dados["Valor"].sum()

st.markdown(f"### Total: R$ {total:,.2f}")

st.markdown('</div>', unsafe_allow_html=True)
