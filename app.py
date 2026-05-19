import streamlit as st
from PIL import Image
from streamlit_pdf_viewer import pdf_viewer
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

# =========================================
# CSS
# =========================================

st.markdown("""
<style>

/* =====================================
FUNDO GERAL
===================================== */

html, body, [class*="css"] {

    background-color: #f5f5f5;
    color: #131203;
}

/* =====================================
CONTAINER PRINCIPAL
===================================== */

.block-container {

    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* =====================================
SIDEBAR
===================================== */

[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #0d4caa 0%,
        #0a3d86 100%
    );

    border-right: 1px solid rgba(255,255,255,0.08);
}

/* =====================================
LOGO
===================================== */

.logo-container {

    background: rgba(255,255,255,0.08);

    border-radius: 0px;

    padding: 0px;

    margin-bottom: 1px;

    backdrop-filter: blur(6px);
}

/* =====================================
TEXTOS MENU
===================================== */

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span {

    color: #ffffff !important;

    font-weight: 500;
}

/* =====================================
TÍTULO MENU
===================================== */

[data-testid="stSidebar"] h1 {

    color: white !important;

    font-size: 26px !important;

    font-weight: 700 !important;
}

/* =====================================
SELECTBOX
===================================== */

.stSelectbox div[data-baseweb="select"] {

    background-color: rgba(255,255,255,0.96);

    border-radius: 12px;

    border: none;
}

.stSelectbox div[data-baseweb="select"] > div {

    color: #131203 !important;

    font-weight: 500;
}

/* =====================================
INPUT TEXTO
===================================== */

.stTextInput input {

    background-color: rgba(255,255,255,0.96) !important;

    color: #131203 !important;

    border-radius: 12px !important;

    border: none !important;
}

/* =====================================
RESUMO
===================================== */

[data-testid="stAlert"] {

    border-radius: 12px;
}

/* =====================================
FEED
===================================== */

[data-testid="stVerticalBlock"] {

    gap: 0.25rem;
}

</style>
""", unsafe_allow_html=True)

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

                if os.path.splitext(arq)[1].lower()
                in EXTENSOES_IMAGEM + EXTENSOES_PDF
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

st.subheader("    ")

st.header(
    "CAMPANHAS ATIVAS"
)

st.caption(
    f"{total_campanhas} campanhas ativas cadastradas"
)

# =========================================
# RESUMO
# =========================================


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

            arquivos_validos = [

                arq for arq in os.listdir(
                    caminho_fornecedor
                )

                if os.path.splitext(arq)[1].lower()
                in EXTENSOES_IMAGEM + EXTENSOES_PDF
            ]

            quantidade = len(arquivos_validos)

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

    quantidade_colunas = 7

    colunas = st.columns(
        quantidade_colunas
    )

    for i, (
        fornecedor_nome,
        total
    ) in enumerate(lista_fornecedores):

        coluna = colunas[
            i % quantidade_colunas
        ]

        with coluna:

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

st.subheader("MECÂNICAS📃")

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

            caminho_arquivo = os.path.join(
                caminho_fornecedor,
                arquivo
            )

            extensao = os.path.splitext(
                arquivo
            )[1].lower()

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

                st.markdown(f"### {f}")

                st.caption(p)

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

                elif extensao in EXTENSOES_PDF:

                    try:

                        pdf_viewer(
                            caminho_arquivo,
                            width="70%",
                            height=900
                        )

                        with open(
                            caminho_arquivo,
                            "rb"
                        ) as pdf_file:

                            st.download_button(
                                label="📥 Baixar PDF",
                                data=pdf_file,
                                file_name=arquivo,
                                mime="application/pdf",
                                use_container_width=True
                            )

                    except Exception as erro:

                        st.error(
                            "Erro ao abrir PDF"
                        )

                        st.write(erro)

                st.divider()

# =========================================
# TOTAL
# =========================================

st.sidebar.divider()

st.sidebar.write(
    f"CAMPANHAS ATIVAS: {contador}"
)