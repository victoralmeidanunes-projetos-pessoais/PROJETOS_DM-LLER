# =========================================
# IMPORTS
# =========================================

import streamlit as st
from PIL import Image
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import os

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
# CSS
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
    background: linear-gradient(180deg, #0d4caa 0%, #0a3d86 100%);
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

[data-testid="stAlert"] {
    border-radius: 12px;
}

[data-testid="stVerticalBlock"] {
    gap: 0.25rem;
}

.excel-box {
    background-color: white;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #E5E5E5;
    margin-top: 15px;
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# FUNÇÃO EXCEL
# =========================================

def ler_excel(caminho_excel):

    try:

        if caminho_excel.endswith(".xlsb"):

            abas = pd.ExcelFile(caminho_excel, engine="pyxlsb").sheet_names
            aba_escolhida = abas[0]

            for aba in abas:
                if "geral" in aba.lower():
                    aba_escolhida = aba
                    break

            df = pd.read_excel(
                caminho_excel,
                sheet_name=aba_escolhida,
                engine="pyxlsb"
            )

        else:

            abas = pd.ExcelFile(caminho_excel).sheet_names
            aba_escolhida = abas[0]

            for aba in abas:
                if "geral" in aba.lower():
                    aba_escolhida = aba
                    break

            df = pd.read_excel(
                caminho_excel,
                sheet_name=aba_escolhida
            )

        df = df.dropna(how="all")
        df = df.dropna(axis=1, how="all")
        df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed")]
        df = df.head(25)

        return df

    except Exception as erro:
        return erro

# =========================================
# LOGO
# =========================================

logo = Image.open("imagens/logo.png")

with st.sidebar:

    st.image(logo, use_container_width=True)
    st.title("FILTROS")

# =========================================
# CONTADORES (mantido igual)
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

            quantidade = len(arquivos_validos)
            total_pauta += quantidade

            contagem_fornecedores[fornecedor_nome] = contagem_fornecedores.get(fornecedor_nome, 0) + quantidade

        contagem_pautas[pauta_nome] = total_pauta

total_campanhas = sum(contagem_pautas.values())

st.header("CAMPANHAS ATIVAS")
st.caption(f"{total_campanhas} campanhas ativas cadastradas")

st.divider()

# =========================================
# FILTROS
# =========================================

pautas = sorted([p for p in os.listdir(PASTA_RAIZ) if os.path.isdir(os.path.join(PASTA_RAIZ, p))])

pauta = st.sidebar.selectbox("Pauta", ["Todas"] + pautas)

fornecedores = []

pastas_para_ler = pautas if pauta == "Todas" else [pauta]

for p in pastas_para_ler:
    for f in os.listdir(os.path.join(PASTA_RAIZ, p)):
        if os.path.isdir(os.path.join(PASTA_RAIZ, p, f)):
            fornecedores.append(f)

fornecedores = sorted(list(set(fornecedores)))

fornecedor = st.sidebar.selectbox("Fornecedor", ["Todos"] + fornecedores)

pesquisa = st.sidebar.text_input("Pesquisar")

# =========================================
# FEED
# =========================================

contador = 0

for p in pastas_para_ler:

    caminho_pauta = os.path.join(PASTA_RAIZ, p)

    for f in os.listdir(caminho_pauta):

        if fornecedor != "Todos" and f != fornecedor:
            continue

        caminho_fornecedor = os.path.join(caminho_pauta, f)

        arquivos = sorted(os.listdir(caminho_fornecedor), reverse=True)

        for arquivo in arquivos:

            if arquivo.startswith("~$"):
                continue

            if pesquisa and pesquisa.lower() not in arquivo.lower():
                continue

            caminho_arquivo = os.path.join(caminho_fornecedor, arquivo)

            extensao = os.path.splitext(arquivo)[1].lower()
            nome_base = os.path.splitext(arquivo)[0]

            if extensao not in EXTENSOES_IMAGEM + EXTENSOES_PDF:
                continue

            contador += 1

            with st.container():

                st.markdown(f"## {f}")
                st.caption(p)

                # =====================================
                # PDF / IMAGEM
                # =====================================

                if extensao in EXTENSOES_IMAGEM:

                    try:
                        st.image(Image.open(caminho_arquivo), use_container_width=True)
                    except:
                        st.error("Erro imagem")

                elif extensao in EXTENSOES_PDF:

                    try:
                        pdf_viewer(caminho_arquivo, width="100%", height=850)

                        with open(caminho_arquivo, "rb") as pdf_file:
                            st.download_button(
                                "📥 Baixar PDF",
                                pdf_file,
                                file_name=arquivo,
                                mime="application/pdf"
                            )

                    except Exception as e:
                        st.error("Erro PDF")
                        st.write(e)

                # =====================================
                # EXCEL RELACIONADO
                # =====================================

                excel_encontrado = None

                for arq in os.listdir(caminho_fornecedor):

                    if arq.startswith("~$"):
                        continue

                    if os.path.splitext(arq)[0] == nome_base:
                        if arq.endswith(tuple(EXTENSOES_EXCEL)):
                            excel_encontrado = os.path.join(caminho_fornecedor, arq)
                            break

                if excel_encontrado:

                    st.markdown("### 📊 Acompanhamento")

                    resultado = ler_excel(excel_encontrado)

                    if isinstance(resultado, pd.DataFrame):
                        st.dataframe(resultado, use_container_width=True, height=350)

                    # =====================================
                    # PREVIEW DO WATCHDOG (NOVO)
                    # =====================================

                    preview_path = None

                    for img in os.listdir(caminho_fornecedor):

                        if img.startswith("~$"):
                            continue

                        if img.lower().endswith(".png") and "preview" in img.lower():
                            if nome_base in img:
                                preview_path = os.path.join(caminho_fornecedor, img)
                                break

                    if preview_path and os.path.exists(preview_path):

                        st.markdown("### 🖼 Preview automático")

                        try:
                            st.image(
                                Image.open(preview_path),
                                use_container_width=True,
                                caption="Células ativas (auto gerado)"
                            )
                        except:
                            st.warning("Erro preview")

                st.divider()

st.sidebar.write(f"CAMPANHAS ATIVAS: {contador}")