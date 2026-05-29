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

EXTENSOES_IMAGEM = [
    ".png",
    ".jpg",
    ".jpeg",
    ".webp"
]

EXTENSOES_PDF = [
    ".pdf"
]

EXTENSOES_EXCEL = [
    ".xlsx",
    ".xlsb",
    ".xlsm"
]

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
# FUNÇÃO LEITURA EXCEL
# =========================================

def ler_excel(caminho_excel):

    try:

        # ================================
        # XLSB
        # ================================

        if caminho_excel.endswith(".xlsb"):

            abas = pd.ExcelFile(
                caminho_excel,
                engine="pyxlsb"
            ).sheet_names

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

        # ================================
        # XLSX / XLSM
        # ================================

        else:

            abas = pd.ExcelFile(
                caminho_excel
            ).sheet_names

            aba_escolhida = abas[0]

            for aba in abas:

                if "geral" in aba.lower():

                    aba_escolhida = aba
                    break

            df = pd.read_excel(
                caminho_excel,
                sheet_name=aba_escolhida
            )

        # ================================
        # LIMPEZA
        # ================================

        df = df.dropna(
            how="all"
        )

        df = df.dropna(
            axis=1,
            how="all"
        )

        # REMOVE COLUNAS "UNNAMED"

        df = df.loc[
            :,
            ~df.columns.astype(str)
            .str.contains("^Unnamed")
        ]

        # LIMITA LINHAS

        df = df.head(25)

        return df

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

            arquivos_validos = [

                arq for arq in os.listdir(caminho_fornecedor)

                if (
                    os.path.splitext(arq)[1].lower()
                    in EXTENSOES_IMAGEM + EXTENSOES_PDF
                )

                and not arq.startswith("~$")
            ]

            quantidade = len(arquivos_validos)

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
# RESUMO PAUTAS
# =========================================

for pauta_nome in sorted(contagem_pautas.keys()):

    total_pauta = contagem_pautas[pauta_nome]

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
# FILTRO PAUTA
# =========================================

pauta = st.sidebar.selectbox(
    "Pauta",
    ["Todas"] + pautas
)

# =========================================
# LISTAR FORNECEDORES
# =========================================

fornecedores = []

pastas_para_ler = pautas

if pauta != "Todas":

    pastas_para_ler = [pauta]

for p in pastas_para_ler:

    caminho_pauta = os.path.join(
        PASTA_RAIZ,
        p
    )

    if os.path.isdir(caminho_pauta):

        for f in os.listdir(caminho_pauta):

            caminho_fornecedor = os.path.join(
                caminho_pauta,
                f
            )

            if os.path.isdir(caminho_fornecedor):

                fornecedores.append(f)

fornecedores = sorted(
    list(set(fornecedores))
)

# =========================================
# FILTRO FORNECEDOR
# =========================================

fornecedor = st.sidebar.selectbox(
    "Fornecedor",
    ["Todos"] + fornecedores
)

# =========================================
# PESQUISA
# =========================================

pesquisa = st.sidebar.text_input(
    "Pesquisar"
)

# =========================================
# FEED
# =========================================

st.subheader("MECÂNICAS 📃")

st.divider()

contador = 0

# =========================================
# LOOP PRINCIPAL
# =========================================

for p in pastas_para_ler:

    caminho_pauta = os.path.join(
        PASTA_RAIZ,
        p
    )

    if not os.path.isdir(caminho_pauta):
        continue

    for f in os.listdir(caminho_pauta):

        if fornecedor != "Todos" and f != fornecedor:
            continue

        caminho_fornecedor = os.path.join(
            caminho_pauta,
            f
        )

        if not os.path.isdir(caminho_fornecedor):
            continue

        arquivos = os.listdir(caminho_fornecedor)

        arquivos.sort(reverse=True)

        for arquivo in arquivos:

            if arquivo.startswith("~$"):
                continue

            caminho_arquivo = os.path.join(
                caminho_fornecedor,
                arquivo
            )

            extensao = os.path.splitext(
                arquivo
            )[1].lower()

            nome_sem_extensao = os.path.splitext(
                arquivo
            )[0]

            if (
                extensao not in EXTENSOES_IMAGEM
                and extensao not in EXTENSOES_PDF
            ):
                continue

            if pesquisa:

                if pesquisa.lower() not in arquivo.lower():

                    continue

            contador += 1

            with st.container():

                st.markdown(f"## {f}")

                st.caption(p)

                # =====================================
                # IMAGEM
                # =====================================

                if extensao in EXTENSOES_IMAGEM:

                    try:

                        imagem = Image.open(
                            caminho_arquivo
                        )

                        st.image(
                            imagem,
                            use_container_width=True
                        )

                    except Exception as erro:

                        st.error(
                            "Erro ao abrir imagem"
                        )

                        st.write(erro)

                # =====================================
                # PDF
                # =====================================

                elif extensao in EXTENSOES_PDF:

                    try:

                        pdf_viewer(
                            caminho_arquivo,
                            width="100%",
                            height=850
                        )

                        with open(
                            caminho_arquivo,
                            "rb"
                        ) as pdf_file:

                            st.download_button(
                                label="📥 Baixar PDF",
                                data=pdf_file,
                                file_name=arquivo,
                                mime="application/pdf"
                            )

                    except Exception as erro:

                        st.error(
                            "Erro ao abrir PDF"
                        )

                        st.write(erro)

                # =====================================
                # BUSCAR EXCEL RELACIONADO
                # =====================================

                excel_encontrado = None

                for arq_excel in os.listdir(caminho_fornecedor):

                    if arq_excel.startswith("~$"):
                        continue

                    nome_excel = os.path.splitext(
                        arq_excel
                    )[0]

                    extensao_excel = os.path.splitext(
                        arq_excel
                    )[1].lower()

                    if extensao_excel not in EXTENSOES_EXCEL:
                        continue

                    if nome_excel == nome_sem_extensao:

                        excel_encontrado = os.path.join(
                            caminho_fornecedor,
                            arq_excel
                        )

                        break

                # =====================================
                # EXIBIR EXCEL
                # =====================================

                if excel_encontrado:

                    st.markdown("""
                    <div class="excel-box">
                    """, unsafe_allow_html=True)

                    st.markdown("### 📊 Acompanhamento")

                    resultado = ler_excel(
                        excel_encontrado
                    )

                    if isinstance(resultado, pd.DataFrame):

                        st.dataframe(
                            resultado,
                            use_container_width=True,
                            height=350
                        )

                        st.caption(
                            f"{len(resultado)} linhas exibidas"
                        )

                    else:

                        st.warning(
                            "Não foi possível carregar o Excel."
                        )

                        st.write(resultado)

                    with open(
                        excel_encontrado,
                        "rb"
                    ) as excel_file:

                        st.download_button(
                            label="📥 Baixar Excel",
                            data=excel_file,
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
# TOTAL
# =========================================

st.sidebar.divider()

st.sidebar.write(
    f"CAMPANHAS ATIVAS: {contador}"
)