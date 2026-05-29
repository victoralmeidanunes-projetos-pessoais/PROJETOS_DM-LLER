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
    background: linear-gradient(
        180deg,
        #0d4caa 0%,
        #0a3d86 100%
    );
}

.logo-container {
    background: rgba(255,255,255,0.08);
    padding: 0px;
    margin-bottom: 1px;
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
    background: white;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #E5E5E5;
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# FUNÇÃO LEITURA EXCEL
# =========================================

def ler_excel(caminho):

    try:

        if caminho.endswith(".xlsb"):

            abas = pd.ExcelFile(
                caminho,
                engine="pyxlsb"
            ).sheet_names

            aba = abas[0]

            for a in abas:

                if "geral" in a.lower():

                    aba = a
                    break

            df = pd.read_excel(
                caminho,
                sheet_name=aba,
                engine="pyxlsb"
            )

        else:

            abas = pd.ExcelFile(
                caminho
            ).sheet_names

            aba = abas[0]

            for a in abas:

                if "geral" in a.lower():

                    aba = a
                    break

            df = pd.read_excel(
                caminho,
                sheet_name=aba
            )

        df = df.dropna(how="all")
        df = df.dropna(axis=1, how="all")

        df = df.loc[
            :,
            ~df.columns.astype(str)
            .str.contains("^Unnamed")
        ]

        return df.head(20)

    except Exception as erro:

        return erro

# =========================================
# LOGO
# =========================================

logo = Image.open("imagens/logo.png")

# =========================================
# SIDEBAR
# =========================================

with st.sidebar:

    st.markdown(
        "<div class='logo-container'>",
        unsafe_allow_html=True
    )

    st.image(
        logo,
        use_container_width=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

    st.title("FILTROS")

# =========================================
# CONTADORES
# =========================================

contagem_pautas = {}
contagem_fornecedores = {}

if os.path.exists(PASTA_RAIZ):

    for pauta_nome in os.listdir(PASTA_RAIZ):

        caminho_pauta = os.path.join(
            PASTA_RAIZ,
            pauta_nome
        )

        if not os.path.isdir(caminho_pauta):
            continue

        total_pauta = 0

        for fornecedor_nome in os.listdir(caminho_pauta):

            caminho_fornecedor = os.path.join(
                caminho_pauta,
                fornecedor_nome
            )

            if not os.path.isdir(caminho_fornecedor):
                continue

            quantidade = 0

            for arq in os.listdir(caminho_fornecedor):

                if arq.lower().endswith(".pdf"):

                    quantidade += 1

            total_pauta += quantidade

            if fornecedor_nome not in contagem_fornecedores:

                contagem_fornecedores[
                    fornecedor_nome
                ] = 0

            contagem_fornecedores[
                fornecedor_nome
            ] += quantidade

        contagem_pautas[
            pauta_nome
        ] = total_pauta

# =========================================
# TOTAL GERAL
# =========================================

total_campanhas = sum(
    contagem_pautas.values()
)

# =========================================
# CABEÇALHO
# =========================================

st.subheader(" ")

st.header(
    "CAMPANHAS ATIVAS"
)

st.caption(
    f"{total_campanhas} campanhas ativas cadastradas"
)

# =========================================
# FORNECEDORES POR PAUTA
# =========================================

fornecedores_por_pauta = {}

if os.path.exists(PASTA_RAIZ):

    for pauta_nome in sorted(os.listdir(PASTA_RAIZ)):

        caminho_pauta = os.path.join(
            PASTA_RAIZ,
            pauta_nome
        )

        if not os.path.isdir(caminho_pauta):
            continue

        lista_fornecedores = []

        for fornecedor_nome in sorted(
            os.listdir(caminho_pauta)
        ):

            caminho_fornecedor = os.path.join(
                caminho_pauta,
                fornecedor_nome
            )

            if not os.path.isdir(caminho_fornecedor):
                continue

            quantidade = 0

            for arq in os.listdir(caminho_fornecedor):

                if arq.lower().endswith(".pdf"):

                    quantidade += 1

            lista_fornecedores.append(
                (
                    fornecedor_nome,
                    quantidade
                )
            )

        fornecedores_por_pauta[
            pauta_nome
        ] = lista_fornecedores

# =========================================
# EXIBIR RESUMO
# =========================================

for pauta_nome, lista_fornecedores in fornecedores_por_pauta.items():

    total_pauta = contagem_pautas.get(
        pauta_nome,
        0
    )

    st.markdown(
        f"""
        <div style="
            background-color:#A8B9DC;
            padding:6px;
            border-radius:5px;
            text-align:center;
            color:white;
            font-weight:700;
            margin-bottom:8px;
        ">
            📁 {pauta_nome} | {total_pauta} campanhas
        </div>
        """,
        unsafe_allow_html=True
    )

    colunas = st.columns(7)

    for i, (
        fornecedor_nome,
        total
    ) in enumerate(lista_fornecedores):

        with colunas[i % 7]:

            st.info(
                f"{fornecedor_nome}: {total}"
            )

    st.markdown("<br>", unsafe_allow_html=True)

st.divider()

# =========================================
# LISTAR PAUTAS
# =========================================

pautas = []

if os.path.exists(PASTA_RAIZ):

    for item in os.listdir(PASTA_RAIZ):

        caminho = os.path.join(
            PASTA_RAIZ,
            item
        )

        if os.path.isdir(caminho):

            pautas.append(item)

pautas.sort()

# =========================================
# FILTROS
# =========================================

pauta_sel = st.sidebar.selectbox(
    "Pauta",
    ["Todas"] + pautas
)

lista_pautas = (
    pautas
    if pauta_sel == "Todas"
    else [pauta_sel]
)

fornecedores = []

for p in lista_pautas:

    caminho_pauta = os.path.join(
        PASTA_RAIZ,
        p
    )

    if os.path.isdir(caminho_pauta):

        for f in os.listdir(caminho_pauta):

            fornecedores.append(f)

fornecedores = sorted(
    list(set(fornecedores))
)

fornecedor_sel = st.sidebar.selectbox(
    "Fornecedor",
    ["Todos"] + fornecedores
)

pesquisa = st.sidebar.text_input(
    "Pesquisar"
)

# =========================================
# ABAS
# =========================================

tab1, tab2 = st.tabs([
    "📄 Mecânicas",
    "🖼 Imagens & Excel"
])

contador = 0

# =========================================
# TAB PDF
# =========================================

with tab1:

    for p in lista_pautas:

        caminho_pauta = os.path.join(
            PASTA_RAIZ,
            p
        )

        if not os.path.isdir(caminho_pauta):
            continue

        for f in os.listdir(caminho_pauta):

            if fornecedor_sel != "Todos" and f != fornecedor_sel:
                continue

            pasta = os.path.join(
                caminho_pauta,
                f
            )

            if not os.path.isdir(pasta):
                continue

            arquivos = os.listdir(pasta)

            for arq in arquivos:

                if arq.startswith("~$"):
                    continue

                if not arq.lower().endswith(".pdf"):
                    continue

                if pesquisa:

                    if pesquisa.lower() not in arq.lower():
                        continue

                contador += 1

                caminho = os.path.join(
                    pasta,
                    arq
                )

                st.markdown(f"## {f}")

                st.caption(p)

                pdf_viewer(
                    caminho,
                    width="100%",
                    height=850
                )

                with open(
                    caminho,
                    "rb"
                ) as file:

                    st.download_button(
                        "📥 Baixar PDF",
                        file,
                        file_name=arq
                    )

                st.divider()

# =========================================
# TAB IMAGENS
# =========================================

with tab2:

    previews_exibidos = set()

    for p in lista_pautas:

        caminho_pauta = os.path.join(
            PASTA_RAIZ,
            p
        )

        if not os.path.isdir(caminho_pauta):
            continue

        for f in os.listdir(caminho_pauta):

            if fornecedor_sel != "Todos" and f != fornecedor_sel:
                continue

            pasta = os.path.join(
                caminho_pauta,
                f
            )

            if not os.path.isdir(pasta):
                continue

            arquivos = os.listdir(pasta)

            for arq in arquivos:

                if arq.startswith("~$"):
                    continue

                # MOSTRA SOMENTE PREVIEW
                if "_preview" not in arq.lower():
                    continue

                ext = os.path.splitext(
                    arq
                )[1].lower()

                if ext not in EXT_IMAGEM:
                    continue

                # REMOVE DUPLICIDADE
                if arq.lower() in previews_exibidos:
                    continue

                previews_exibidos.add(
                    arq.lower()
                )

                if pesquisa:

                    if pesquisa.lower() not in arq.lower():
                        continue

                caminho = os.path.join(
                    pasta,
                    arq
                )

                st.markdown(f"## {f}")

                st.caption(p)

                st.image(
                    caminho,
                    use_container_width=True
                )

                # =====================================
                # BUSCAR EXCEL RELACIONADO
                # =====================================

                nome_base = arq.lower()

                nome_base = nome_base.replace(
                    "_preview.png",
                    ""
                )

                nome_base = nome_base.replace(
                    "_preview.jpg",
                    ""
                )

                nome_base = nome_base.replace(
                    "_preview.jpeg",
                    ""
                )

                nome_base = nome_base.replace(
                    "_preview.webp",
                    ""
                )

                excel_encontrado = None

                for arq_excel in arquivos:

                    if arq_excel.startswith("~$"):
                        continue

                    ext_excel = os.path.splitext(
                        arq_excel
                    )[1].lower()

                    if ext_excel not in EXT_EXCEL:
                        continue

                    nome_excel = os.path.splitext(
                        arq_excel
                    )[0].lower()

                    if nome_excel == nome_base:

                        excel_encontrado = os.path.join(
                            pasta,
                            arq_excel
                        )

                        break

                # =====================================
                # EXCEL
                # =====================================

                if excel_encontrado:

                    st.markdown("""
                    <div class="excel-box">
                    """, unsafe_allow_html=True)

                    st.markdown("### 📊 Excel")

                    resultado = ler_excel(
                        excel_encontrado
                    )

                    if isinstance(
                        resultado,
                        pd.DataFrame
                    ):

                        st.dataframe(
                            resultado,
                            use_container_width=True,
                            height=350
                        )

                    else:

                        st.warning(
                            "Não foi possível carregar o Excel."
                        )

                        st.write(resultado)

                    # DOWNLOAD EXCEL
                    with open(
                        excel_encontrado,
                        "rb"
                    ) as fexcel:

                        st.download_button(
                            label="📥 Baixar Excel",
                            data=fexcel,
                            file_name=os.path.basename(
                                excel_encontrado
                            ),
                            mime="application/vnd.ms-excel"
                        )

                    st.markdown("""
                    </div>
                    """, unsafe_allow_html=True)

                st.divider()

# =========================================
# FOOTER
# =========================================

st.sidebar.divider()

st.sidebar.write(
    f"CAMPANHAS (PDF): {contador}"
)