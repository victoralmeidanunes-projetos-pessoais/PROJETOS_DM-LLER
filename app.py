# =========================================
# RESUMO
# =========================================

st.markdown("### Resumo Geral")

# =========================================
# MAPEAR FORNECEDORES POR PAUTA
# =========================================

fornecedores_por_pauta = {}

if os.path.exists(PASTA_RAIZ):

    for pauta_nome in os.listdir(PASTA_RAIZ):

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
# EXIBIR EM COLUNAS
# =========================================

quantidade_pautas = len(
    fornecedores_por_pauta
)

if quantidade_pautas > 0:

    colunas_pautas = st.columns(
        quantidade_pautas
    )

    for i, (
        pauta_nome,
        lista_fornecedores
    ) in enumerate(
        fornecedores_por_pauta.items()
    ):

        with colunas_pautas[i]:

            total_pauta = contagem_pautas.get(
                pauta_nome,
                0
            )

            st.markdown(
                f"""
                <div style="
                    background-color:#0d4caa;
                    padding:12px;
                    border-radius:12px;
                    text-align:center;
                    color:white;
                    font-weight:700;
                    margin-bottom:10px;
                ">
                    📁 {pauta_nome}<br>
                    {total_pauta} campanhas
                </div>
                """,
                unsafe_allow_html=True
            )

            for fornecedor_nome, total in lista_fornecedores:

                st.info(
                    f"{fornecedor_nome}: {total}"
                )

st.divider()