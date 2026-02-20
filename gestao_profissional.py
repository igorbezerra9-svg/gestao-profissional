import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Gestão Profissional", layout="wide")

# ====== LOGO NO TOPO ======
import os
logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
st.image(logo_path, width=200)

st.markdown("""
<style>
body {background-color: #0e1117; color: white;}
.card {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}
.big-number {
    font-size: 22px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

def montar(blocos, multiplicador):
    dados = []
    saldo = 0
    bet = 1

    for qtd, ficha in blocos:
        for _ in range(qtd):
            custo = ficha
            saldo += custo
            vitoria = ficha * multiplicador
            lucro = vitoria - saldo

            dados.append([
                bet,
                round(custo,2),
                round(saldo,2),
                round(vitoria,2),
                round(lucro,2)
            ])
            bet += 1

    return pd.DataFrame(
        dados,
        columns=["Nº Bets", "Custo", "Saldo", "Vitória", "Lucro"]
    )

tab1, tab2 = st.tabs(["📊 Estratégia", "💼 Gerenciamento de Banca"])

# ==============================
# ABA 1 - ESTRATÉGIA
# ==============================

with tab1:

    st.title("💼 GESTÃO PROFISSIONAL DE FICHAS")

    valor_base = st.number_input("💰 Valor base da ficha", min_value=1.0, value=10.0)

    estrategia = st.selectbox(
        "📌 Escolha a estratégia",
        [
            "3 FICHAS",
            "4 FICHAS",
            "5 FICHAS",
            "6 FICHAS CONSERVADORA",
            "6 FICHAS AGRESSIVA",
            "9 FICHAS"
        ]
    )

    if estrategia == "3 FICHAS":
        df = montar([(11, valor_base),(6, valor_base*2),(6, valor_base*4),
                     (6, valor_base*8),(2, valor_base*16)],12)
        perfil = "🔴 Muito Agressiva"

    elif estrategia == "4 FICHAS":
        df = montar([(7, valor_base),(4, valor_base*2),(4, valor_base*4),
                     (4, valor_base*8),(4, valor_base*16),
                     (4, valor_base*32),(3, valor_base*64)],9)
        perfil = "🟠 Agressiva"

    elif estrategia == "5 FICHAS":
        df = montar([(6, valor_base),(4, valor_base*2.8),
                     (4, valor_base*6.8),(1, valor_base*13.6)],7.2)
        perfil = "🟡 Moderada"

    elif estrategia == "6 FICHAS CONSERVADORA":
        df = montar([(5, valor_base),(3, valor_base*2),
                     (3, valor_base*4)],6)
        perfil = "🟢 Conservadora"

    elif estrategia == "6 FICHAS AGRESSIVA":
        df = montar([(6, valor_base),(3, valor_base*2),
                     (3, valor_base*4),(3, valor_base*8),
                     (1, valor_base*16)],6)
        perfil = "🟠 Agressiva"

    elif estrategia == "9 FICHAS":
        df = montar([(2, valor_base),(2, valor_base*2),
                     (2, valor_base*4),(2, valor_base*8),
                     (2, valor_base*16),(2, valor_base*32),
                     (1, valor_base*64)],4)
        perfil = "🔴 Extremamente Agressiva"

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"<div class='card'><div>Banca Necessária</div><div class='big-number'>R$ {df['Saldo'].max():,.2f}</div></div>", unsafe_allow_html=True)

    with col2:
        st.markdown(f"<div class='card'><div>Lucro Mínimo</div><div class='big-number'>R$ {df['Lucro'].min():,.2f}</div></div>", unsafe_allow_html=True)

    with col3:
        st.markdown(f"<div class='card'><div>Lucro Máximo</div><div class='big-number'>R$ {df['Lucro'].max():,.2f}</div></div>", unsafe_allow_html=True)

    with col4:
        st.markdown(f"<div class='card'><div>Perfil</div><div class='big-number'>{perfil}</div></div>", unsafe_allow_html=True)

    st.markdown("---")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=(len(df) + 1) * 35
    )

# ==============================
# ABA 2 - GERENCIAMENTO
# ==============================

with tab2:

    st.header("📈 GERENCIAMENTO DE BANCA")

    usuario = st.text_input("👤 Seu nome")

    if usuario:

        arquivo = f"historico_{usuario}.csv"

        if os.path.exists(arquivo):
            historico = pd.read_csv(arquivo)
        else:
            historico = pd.DataFrame(columns=["Data","Resultado","Banca"])

        banca_atual = historico["Banca"].iloc[-1] if not historico.empty else 0.0

        st.subheader(f"💼 Banca Atual: R$ {banca_atual:,.2f}")

        st.markdown("### 📊 Registrar Resultado")
        resultado_dia = st.number_input("Resultado do Dia (lucro ou prejuízo)", value=0.0)

        if st.button("Registrar Resultado"):
            nova_banca = banca_atual + resultado_dia
            nova_linha = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y"),
                "Resultado": resultado_dia,
                "Banca": nova_banca
            }])
            historico = pd.concat([historico, nova_linha], ignore_index=True)
            historico.to_csv(arquivo, index=False)
            st.success("Resultado salvo!")
            st.rerun()

        st.markdown("---")
        st.markdown("### 🔄 Ajustar Banca Manualmente")

        nova_banca_manual = st.number_input("Definir novo valor de banca", value=banca_atual)

        if st.button("Salvar Ajuste de Banca"):
            nova_linha = pd.DataFrame([{
                "Data": datetime.now().strftime("%d/%m/%Y"),
                "Resultado": 0,
                "Banca": nova_banca_manual
            }])
            historico = pd.concat([historico, nova_linha], ignore_index=True)
            historico.to_csv(arquivo, index=False)
            st.success("Banca ajustada com sucesso!")
            st.rerun()

        st.markdown("---")

        if st.button("🧹 Resetar Histórico"):
            if os.path.exists(arquivo):
                os.remove(arquivo)
            st.success("Histórico apagado!")
            st.rerun()

        if not historico.empty:
            st.markdown("### 📋 Histórico")

            st.dataframe(
                historico,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### 📈 Evolução da Banca")
            st.line_chart(historico.set_index("Data")["Banca"])
