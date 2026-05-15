import streamlit as st
from PIL import Image
import os
import base64

# =========================================
# CONFIG PÁGINA
# =========================================

st.set_page_config(
    page_title="Campanhas",
    layout="wide"
)

# =========================================
# CABEÇALHO
# =========================================

logo = Image.open("imagens/logo.png")

col1, col2, col3 = st.columns([1,2,1])

with col2:

    st.image(
        logo,
        use_container_width=True,
        width=100
    )

    st.markdown(
        """
        <h1 style='text-align: center;'>
        CAMPANHAS DE INCENTIVOS ATIVOS
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='text-align: center;
        font-size:18px;
        color:gray;'>
        DMULLER DISTRIBUIDORA
        </p>
        """,
        unsafe_allow_html=True
    )

st.divider()

# =========================================
# MENU LATERAL
# =========================================

st.sidebar.title("📁 CAMPANHAS")

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
# LISTAR PAUTAS
# =========================================

pautas = os.listdir(PASTA_RAIZ)

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

    for f in os.listdir(caminho_pauta):

        fornecedores.append(f)

fornecedor = st.sidebar.selectbox(
    "Fornecedor",
    ["Todos"] + sorted(set(fornecedores))
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

st.subheader("MECÂNICAS ATIVAS")

contador = 0

# =========================================
# LER ARQUIVOS
# =========================================

for p in pastas_para_ler:

    caminho_pauta = os.path.join(
        PASTA_RAIZ,
        p
    )

    for f in os.listdir(caminho_pauta):

        if fornecedor != "Todos" and f != fornecedor:
            continue

        caminho_fornecedor = os.path.join(
            caminho_pauta,
            f
        )

        for arquivo in os.listdir(caminho_fornecedor):

            if pesquisa:

                if pesquisa.lower() not in arquivo.lower():
                    continue

            caminho_arquivo = os.path.join(
                caminho_fornecedor,
                arquivo
            )

            extensao = os.path.splitext(
                arquivo
            )[1].lower()

            contador += 1

            with st.container():

                st.markdown(f"### {f}")

                st.caption(p)

                # =====================
                # IMAGEM
                # =====================

                if extensao in EXTENSOES_IMAGEM:

                    imagem = Image.open(
                        caminho_arquivo
                    )

                    st.image(
                        imagem,
                        use_container_width=True
                    )

                # =====================
                # PDF
                # =====================

                elif extensao in EXTENSOES_PDF:

                    with open(
                        caminho_arquivo,
                        "rb"
                    ) as pdf_file:

                        base64_pdf = base64.b64encode(
                            pdf_file.read()
                        ).decode("utf-8")

                    pdf_display = f"""
                    <iframe
                        src="data:application/pdf;base64,{base64_pdf}"
                        width="100%"
                        height="700">
                    </iframe>
                    """

                    st.markdown(
                        pdf_display,
                        unsafe_allow_html=True
                    )

                st.write(arquivo)

                st.divider()

# =========================================
# TOTAL
# =========================================

st.sidebar.divider()

st.sidebar.write(
    f"Arquivos encontrados: {contador}"
)