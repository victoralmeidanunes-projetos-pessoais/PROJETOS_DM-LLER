# =========================================
# IMPORTS
# =========================================

import streamlit as st
from PIL import Image
from streamlit_pdf_viewer import pdf_viewer
import os
import pandas as pd

# =========================================
# CONFIG PÁGINA
# =========================================

st.set_page_config(
    page_title="Campanhas",
    layout="wide"
)

# =========================================
# PASTA PRINCIPAL
# =========================================

PASTA_RAIZ = "MECÂNICAS"

# =========================================
# EXTENSÕES
# =========================================

EXTENSOES_IMAGEM = [".png", ".jpg", ".jpeg", ".webp"]
EXTENSOES_PDF = [".pdf"]
EXTENSOES_EXCEL = [".xlsx", ".xlsb", ".xlsm"]

# =========================================
# CSS (INALTERADO)
# =========================================

st.markdown("""
<style>
html, body, [class*="css"] {
    background-color: #f5f5f5;
    color: #131203;
}

.block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0d4caa 0%,#0a3d86 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

.logo-container {
    background: rgba(255,255,255,0.08);
    border-radius: 0px;
    padding: 0px;
    margin-bottom: 1px;
    backdrop-filter: blur(6px);
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {
    color: #ffffff !important;
    font-weight: 500;
}

[data-testid="stSidebar"] h1 {
    color: white !important;
    font-size: 26px !important;
    font-weight: 700 !important;
}

.stSelectbox div[data-baseweb="select"] {
    background-color: rgba(255,255,255,0.96);
    border-radius: 12px;
    border: none;
}

.stSelectbox div[data-baseweb="select"] > div {
    color: #131203 !important;
    font-weight: 500;
}

.stTextInput input {
    background-color: rgba(255,255,255,0.96) !important;
    color: #131203 !important;
    border-radius: 12px !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# =========================================
# LOGO (MANTIDO)
# =========================================

logo = Image.open("imagens/logo.png")

with st.sidebar:
    st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
    st.image(logo, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.title("FILTROS")

# =========================================
# CONTADORES (MANTIDO CORRIGIDO)
# =========================================

contagem_pautas = {}
contagem_fornecedores = {}

if os.path.exists(PASTA_RAIZ):

    for pauta_nome in os.listdir(PASTA_RAIZ):

        caminho_pauta = os.path.join(PASTA_RAIZ, pauta_nome)

        if not os.path.isdir(caminho_pauta):
            continue

        total_pauta = 0

        for fornecedor_nome in os.listdir(caminho_pauta):

            caminho_fornecedor = os.path.join(caminho_pauta, fornecedor_nome)

            if not os.path.isdir(caminho_fornecedor):
                continue

            arquivos_validos = [
                arq for arq in os.listdir(caminho_fornecedor)
                if os.path.splitext(arq)[1].lower() in EXTENSOES_IMAGEM + EXTENSOES_PDF
                and not arq.startswith("~$")
            ]

            qtd = len(arquivos_validos)

            total_pauta += qtd

            contagem_fornecedores[fornecedor_nome] = contagem_fornecedores.get(fornecedor_nome, 0) + qtd

        contagem_pautas[pauta_nome] = total_pauta

total_campanhas = sum(contagem_pautas.values())

st.header("CAMPANHAS ATIVAS")
st.caption(f"{total_campanhas} campanhas ativas cadastradas")

# =========================================
# RESUMO (MANTIDO)
# =========================================

for pauta_nome in sorted(contagem_pautas.keys()):

    st.markdown(f"""
    <div style="
        background-color:#A8B9DC;
        padding:6px;
        border-radius:5px;
        text-align:center;
        color:white;
        font-weight:700;
        margin-bottom:8px;
    ">
        📁 {pauta_nome} | {contagem_pautas[pauta_nome]} campanhas
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================
# LISTAS / FILTROS
# =========================================

pautas = sorted([p for p in os.listdir(PASTA_RAIZ) if os.path.isdir(os.path.join(PASTA_RAIZ,p))])

pauta = st.sidebar.selectbox("Pauta", ["Todas"] + pautas)

fornecedores = sorted(list(set(
    f
    for p in (pautas if pauta == "Todas" else [pauta])
    for f in os.listdir(os.path.join(PASTA_RAIZ, p))
    if os.path.isdir(os.path.join(PASTA_RAIZ, p, f))
)))

fornecedor = st.sidebar.selectbox("Fornecedor", ["Todos"] + fornecedores)

pesquisa = st.sidebar.text_input("Pesquisar")

# =========================================
# FEED
# =========================================

st.subheader("MECÂNICAS 📃")

contador = 0

for p in (pautas if pauta == "Todas" else [pauta]):

    caminho_pauta = os.path.join(PASTA_RAIZ, p)

    for f in os.listdir(caminho_pauta):

        if fornecedor != "Todos" and f != fornecedor:
            continue

        caminho_fornecedor = os.path.join(caminho_pauta, f)

        arquivos = os.listdir(caminho_fornecedor)

        # 🔥 AGRUPA POR NOME BASE (REMOVE DUPLICAÇÃO)
        agrupados = {}

        for arq in arquivos:

            if arq.startswith("~$"):
                continue

            nome_base = os.path.splitext(arq)[0]
            ext = os.path.splitext(arq)[1].lower()

            if ext not in EXTENSOES_IMAGEM + EXTENSOES_PDF:
                continue

            if pesquisa and pesquisa.lower() not in arq.lower():
                continue

            agrupados.setdefault(nome_base, []).append(arq)

        # =====================================
        # RENDER
        # =====================================

        for nome_base, arquivos_grp in agrupados.items():

            contador += 1

            st.markdown(f"### {f}")
            st.caption(p)

            # ===== IMAGEM / PDF =====
            for arq in arquivos_grp:

                caminho = os.path.join(caminho_fornecedor, arq)
                ext = os.path.splitext(arq)[1].lower()

                if ext in EXTENSOES_IMAGEM:
                    st.image(Image.open(caminho), use_container_width=True)

                elif ext in EXTENSOES_PDF:
                    pdf_viewer(caminho, width="100%", height=850)

            # ===== EXCEL RELACIONADO =====
            for arq_excel in arquivos:

                if arq_excel.startswith("~$"):
                    continue

                if os.path.splitext(arq_excel)[1].lower() not in EXTENSOES_EXCEL:
                    continue

                if os.path.splitext(arq_excel)[0] == nome_base:

                    excel_path = os.path.join(caminho_fornecedor, arq_excel)

                    st.download_button(
                        "📥 Baixar Excel",
                        open(excel_path, "rb"),
                        file_name=arq_excel
                    )

            st.divider()

st.sidebar.divider()
st.sidebar.write(f"CAMPANHAS ATIVAS: {contador}")