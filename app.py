import streamlit as st
from PIL import Image
import os

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
        width=350
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

pautas = []

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

st.subheader("Feed de Mecânicas")

contador = 0

# =========================================
# LER ARQUIVOS
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

            # =====================================
            # FILTRAR EXTENSÕES
            # =====================================

            if (
                extensao not in EXTENSOES_IMAGEM
                and extensao not in EXTENSOES_PDF
            ):
                continue

            # =====================================
            # PESQUISA
            # =====================================

            if pesquisa:

                if pesquisa.lower() not in arquivo.lower():

                    continue

            contador += 1

            # =====================================
            # CARD
            # =====================================

            with st.container():

                st.markdown(f"### {f}")

                st.caption(p)

                # =================================
                # IMAGEM
                # =================================

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
                            f"Erro ao abrir imagem"
                        )

                        st.write(erro)

                # =================================
                # PDF
                # =================================

                elif extensao in EXTENSOES_PDF:

                    st.info(
                        f"📄 PDF disponível: {arquivo}"
                    )

                    try:

                        with open(
                            caminho_arquivo,
                            "rb"
                        ) as pdf_file:

                            st.download_button(
                                label="📥 Abrir / Baixar PDF",
                                data=pdf_file,
                                file_name=arquivo,
                                mime="application/pdf"
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