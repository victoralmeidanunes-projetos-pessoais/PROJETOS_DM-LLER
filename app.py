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

html, body, [class*="css"]  {
    background-color: #f5f5f5;
    color: #131203;
}

/* =====================================
CONTAINER PRINCIPAL
===================================== */

.block-container {
    padding-top: 1.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* =====================================
SIDEBAR
===================================== */

[data-testid="stSidebar"] {
    background-color: #0d4caa;
}

[data-testid="stSidebar"] * {
    color: white;
}

/* =====================================
CAMPOS
===================================== */

.stTextInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 10px;
}

/* =====================================
TÍTULOS
===================================== */

.titulo-principal{
    font-size: 42px;
    font-weight: 700;
    color: #0b459b;
    margin-bottom: 0;
}

.subtitulo{
    font-size: 16px;
    color: #555;
    margin-top: -10px;
}

/* =====================================
CARDS RESUMO
===================================== */

.card-resumo{
    background: white;
    border-radius: 14px;
    padding: 18px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.card-titulo{
    font-size: 18px;
    font-weight: 700;
    color: #0b459b;
    margin-bottom: 10px;
}

/* =====================================
FEED
===================================== */

[data-testid="stVerticalBlock"]{
    gap: 0.7rem;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# LOGO
# =========================================

logo = Image.open("imagens/logo.png")

# =========================================
# MENU LATERAL
# =========================================

st.sidebar.image(
    logo,
    use_container_width=True
)

st.sidebar.title("📁 CAMPANHAS")

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
# CABEÇALHO
# =========================================

st.markdown(
    """
    <p class='titulo-principal'>
    CAMPANHAS ATIVAS
    </p>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p class='subtitulo'>
    Painel de campanhas e mecânicas vigentes
    </p>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# =========================================
# RESUMO PAUTAS
# =========================================

with col1:

    html_pautas = """
    <div class='card-resumo'>
    <div class='card-titulo'>
    Campanhas por Pauta
    </div>
    """

    for pauta, total in contagem_pautas.items():

        html_pautas += f"""
        <p>
        <b>{pauta}</b>: {total}
        </p>
        """

    html_pautas += "</div>"

    st.markdown(
        html_pautas,
        unsafe_allow_html=True
    )

# =========================================
# RESUMO FORNECEDORES
# =========================================

with col2:

    html_fornecedor = """
    <div class='card-resumo'>
    <div class='card-titulo'>
    Campanhas por Fornecedor
    </div>
    """

    for fornecedor_nome, total in sorted(
        contagem_fornecedores.items()
    ):

        html_fornecedor += f"""
        <p>
        <b>{fornecedor_nome}</b>: {total}
        </p>
        """

    html_fornecedor += "</div>"

    st.markdown(
        html_fornecedor,
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

st.subheader("Feed de Mecânicas")

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
                            width="100%",
                            height=500
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
    f"Arquivos encontrados: {contador}"
)