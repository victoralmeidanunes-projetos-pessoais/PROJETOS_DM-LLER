import streamlit as st
import pandas as pd

# =========================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================

st.set_page_config(
    page_title="Sistema de Exemplo",
    page_icon="📊",
    layout="wide"
)

# =========================================
# MENU LATERAL
# =========================================

with st.sidebar:

    st.title("MENU")

    pagina = st.selectbox(
        "Escolha a página",
        [
            "Dashboard",
            "Clientes",
            "Financeiro"
        ]
    )

    st.divider()

    st.subheader("Filtros")

    filtro_estado = st.selectbox(
        "Estado",
        ["SC", "SP", "RJ"]
    )

    filtro_status = st.multiselect(
        "Status",
        ["Ativo", "Inativo", "Pendente"]
    )

    atualizar = st.button("Atualizar Dados")

# =========================================
# TOPO DA PÁGINA
# =========================================

st.title("Sistema de Gestão")

st.write("Exemplo completo para aprendizado do Streamlit.")

# =========================================
# MÉTRICAS
# =========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Clientes",
        "150"
    )

with col2:
    st.metric(
        "Vendas",
        "R$ 25.000"
    )

with col3:
    st.metric(
        "Pedidos",
        "320"
    )

with col4:
    st.metric(
        "Lucro",
        "R$ 8.500"
    )

# =========================================
# LINHA DIVISÓRIA
# =========================================

st.divider()

# =========================================
# ABAS
# =========================================

aba1, aba2, aba3 = st.tabs(
    [
        "Cadastro",
        "Tabela",
        "Configurações"
    ]
)

# =========================================
# ABA 1
# =========================================

with aba1:

    st.subheader("Cadastro de Cliente")

    # COLUNAS
    col1, col2, col3 = st.columns(3)

    with col1:

        nome = st.text_input(
            "Nome"
        )

        idade = st.number_input(
            "Idade",
            min_value=0,
            max_value=120
        )

        cidade = st.selectbox(
            "Cidade",
            [
                "Itajaí",
                "Balneário Camboriú",
                "Florianópolis"
            ]
        )

    with col2:

        email = st.text_input(
            "E-mail"
        )

        telefone = st.text_input(
            "Telefone"
        )

        ativo = st.checkbox(
            "Cliente Ativo"
        )

    st.divider()

    observacao = st.text_area(
        "Observações"
    )

    salvar = st.button(
        "Salvar Cadastro"
    )

    # AÇÃO DO BOTÃO
    if salvar:

        st.success("Cadastro realizado com sucesso!")

        st.write("Nome:", nome)
        st.write("Idade:", idade)
        st.write("Cidade:", cidade)
        st.write("E-mail:", email)

with col3:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=200
    )

# =========================================
# ABA 2
# =========================================

with aba2:

    st.subheader("Tabela de Clientes")

    # DADOS EXEMPLO
    dados = {
        "Nome": [
            "João",
            "Maria",
            "Carlos",
            "Ana"
        ],

        "Cidade": [
            "Itajaí",
            "Florianópolis",
            "Blumenau",
            "Joinville"
        ],

        "Valor": [
            1500,
            2300,
            1800,
            3200
        ]
    }

    df = pd.DataFrame(dados)

    st.dataframe(
        df,
        use_container_width=True
    )

# =========================================
# ABA 3
# =========================================

with aba3:

    st.subheader("Configurações")

    tema_escuro = st.toggle(
        "Tema Escuro"
    )

    notificacao = st.checkbox(
        "Receber notificações"
    )

    volume = st.slider(
        "Volume",
        0,100,0
    )

    st.write("Tema escuro:", tema_escuro)
    st.write("Notificações:", notificacao)
    st.write("Volume:", volume)

# =========================================
# RODAPÉ
# =========================================

st.divider()

st.caption("Sistema criado para aprendizado Streamlit.")