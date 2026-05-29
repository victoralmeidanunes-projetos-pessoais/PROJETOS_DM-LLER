# =========================================
# IMPORTS
# =========================================

import streamlit as st
from PIL import Image
from streamlit_pdf_viewer import pdf_viewer
import pandas as pd
import os

# =========================================
# CONFIG
# =========================================

st.set_page_config(
    page_title="Campanhas",
    layout="wide"
)

PASTA_RAIZ = "MECÂNICAS"

EXT_IMAGEM = [".png", ".jpg", ".jpeg", ".webp"]
EXT_PDF = [".pdf"]
EXT_EXCEL = [".xlsx", ".xlsb", ".xlsm"]

# =========================================
# CSS (mantido)
# =========================================

st.markdown("""
<style>

html, body, [class*="css"] {
    background-color: #f5f5f5;
    color: #131203;
}

.block-container {
    padding: 1rem 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0d4caa,#0a3d86);
}

.excel-box {
    background: white;
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# FUNÇÃO EXCEL
# =========================================

def ler_excel(caminho):

    try:
        abas = pd.ExcelFile(caminho).sheet_names
        aba = abas[0]

        for a in abas:
            if "geral" in a.lower():
                aba = a
                break

        df = pd.read_excel(caminho, sheet_name=aba)

        df = df.dropna(how="all").dropna(axis=1, how="all")
        df = df.loc[:, ~df.columns.astype(str).str.contains("Unnamed")]

        return df.head(20)

    except Exception as e:
        return e

# =========================================
# CONTADOR (SOMENTE PDF - CORRETO)
# =========================================

contagem_pautas = {}
contagem_fornecedores = {}

for pauta in os.listdir(PASTA_RAIZ):

    caminho_pauta = os.path.join(PASTA_RAIZ, pauta)

    if not os.path.isdir(caminho_pauta):
        continue

    total_pdf_pauta = 0

    fornecedores_tmp = {}

    for f in os.listdir(caminho_pauta):

        caminho_f = os.path.join(caminho_pauta, f)

        if not os.path.isdir(caminho_f):
            continue

        total_pdf_forn = 0

        for arq in os.listdir(caminho_f):

            if arq.startswith("~$"):
                continue

            if arq.endswith(".pdf"):
                total_pdf_pauta += 1
                total_pdf_forn += 1

        fornecedores_tmp[f] = total_pdf_forn

    contagem_pautas[pauta] = total_pdf_pauta
    contagem_fornecedores[pauta] = fornecedores_tmp

# =========================================
# MENU SUPERIOR (RESTAURADO)
# =========================================

st.header("CAMPANHAS ATIVAS")

st.caption(f"{sum(contagem_pautas.values())} campanhas ativas (PDFs)")

for pauta, total in contagem_pautas.items():

    st.markdown(f"""
    <div style="
        background:#A8B9DC;
        padding:6px;
        border-radius:5px;
        text-align:center;
        color:white;
        font-weight:700;
        margin-bottom:6px;">
        📁 {pauta} | {total} campanhas
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================
# SIDEBAR FILTROS
# =========================================

pautas = sorted(os.listdir(PASTA_RAIZ))

pauta_sel = st.sidebar.selectbox("Pauta", ["Todas"] + pautas)

fornecedores = []

lista_pautas = pautas if pauta_sel == "Todas" else [pauta_sel]

for p in lista_pautas:
    for f in os.listdir(os.path.join(PASTA_RAIZ, p)):
        fornecedores.append(f)

fornecedores = sorted(set(fornecedores))

fornecedor_sel = st.sidebar.selectbox("Fornecedor", ["Todos"] + fornecedores)

pesquisa = st.sidebar.text_input("Pesquisar")

# =========================================
# ABAS
# =========================================

tab1, tab2 = st.tabs(["📄 Mecânicas", "🖼 Imagens & Excel"])

contador = 0

# =========================================
# TAB 1 - PDF (SEM DUPLICAÇÃO)
# =========================================

with tab1:

    for p in lista_pautas:

        for f in os.listdir(os.path.join(PASTA_RAIZ, p)):

            if fornecedor_sel != "Todos" and f != fornecedor_sel:
                continue

            pasta = os.path.join(PASTA_RAIZ, p, f)

            arquivos = os.listdir(pasta)

            for arq in arquivos:

                if arq.startswith("~$"):
                    continue

                if not arq.endswith(".pdf"):
                    continue

                if pesquisa and pesquisa.lower() not in arq.lower():
                    continue

                contador += 1

                caminho = os.path.join(pasta, arq)

                st.markdown(f"## {f}")
                st.caption(p)

                pdf_viewer(caminho, width="100%", height=800)

                with open(caminho, "rb") as file:
                    st.download_button("📥 Baixar PDF", file, file_name=arq)

                st.divider()

# =========================================
# TAB 2 - IMAGENS + EXCEL + PREVIEW
# =========================================

with tab2:

    for p in lista_pautas:

        for f in os.listdir(os.path.join(PASTA_RAIZ, p)):

            if fornecedor_sel != "Todos" and f != fornecedor_sel:
                continue

            pasta = os.path.join(PASTA_RAIZ, p, f)

            arquivos = os.listdir(pasta)

            imagens_exibidas = set()

            for arq in arquivos:

                if arq.startswith("~$"):
                    continue

                ext = os.path.splitext(arq)[1].lower()

                if ext not in EXT_IMAGEM:
                    continue

                if arq in imagens_exibidas:
                    continue

                imagens_exibidas.add(arq)

                caminho = os.path.join(pasta, arq)

                st.markdown(f"## {f}")
                st.caption(p)

                st.image(Image.open(caminho), use_container_width=True)

                # =================================
                # EXCEL RELACIONADO
                # =================================

                nome_base = os.path.splitext(arq)[0]

                excel = None

                for e in arquivos:
                    if e.startswith(nome_base) and e.endswith(tuple(EXT_EXCEL)):
                        excel = os.path.join(pasta, e)
                        break

                if excel:

                    st.markdown("### 📊 Excel")

                    df = ler_excel(excel)

                    if isinstance(df, pd.DataFrame):
                        st.dataframe(df, use_container_width=True)

                    with open(excel, "rb") as fexcel:
                        st.download_button(
                            "📥 Baixar Excel",
                            fexcel,
                            file_name=os.path.basename(excel)
                        )

                # =================================
                # PREVIEW WATCHDOG
                # =================================

                preview = None

                for img in arquivos:
                    if "preview" in img.lower() and nome_base in img:
                        preview = os.path.join(pasta, img)
                        break

                if preview:
                    st.markdown("### 🖼 Preview automático")
                    st.image(preview, use_container_width=True)

                st.divider()

# =========================================
# FOOTER
# =========================================

st.sidebar.write(f"CAMPANHAS (PDF): {contador}")