import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA (DESIGN RESPONSIVO E CORES CLARAS)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Sistema de Doceria",
    page_icon="🧁",
    layout="wide"
)

# Estilização CSS personalizada para um design limpo e cores claras
st.markdown("""
    <style>
    .stApp {
        background-color: #FAFAFA;
        color: #4A4A4A;
    }
    section[data-testid="stSidebar"] {
        background-color: #FFF5F7;
        border-right: 1px solid #FFE4E8;
    }
    div[data-testid="stMetricValue"] {
        color: #D81B60 !important;
        font-weight: bold;
    }
    .stButton>button {
        background-color: #F8BBD0;
        color: #880E4F;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #F48FB1;
        color: #FFFFFF;
    }
    h1, h2, h3 {
        color: #880E4F;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# INICIALIZAÇÃO DO BANCO DE DADOS EM MEMÓRIA (SESSION STATE)
# -----------------------------------------------------------------------------
if 'produtos' not in st.session_state:
    st.session_state.produtos = pd.DataFrame([
        {"id": 1, "nome": "Creme de Leite", "marca": "Nestlé", "preco": 10.00, "qtd_embalagem": 395.0, "unidade": "Gramas (g)"},
        {"id": 2, "nome": "Leite Condensado", "marca": "Moça", "preco": 8.50, "qtd_embalagem": 395.0, "unidade": "Gramas (g)"}
    ])

if 'fichas' not in st.session_state:
    st.session_state.fichas = []

if 'proximo_id_prod' not in st.session_state:
    st.session_state.proximo_id_prod = 3

if 'proximo_id_ficha' not in st.session_state:
    st.session_state.proximo_id_ficha = 1

# -----------------------------------------------------------------------------
# MENU LATERAL PRINCIPAL (NAVEGAÇÃO SEPARADA)
# -----------------------------------------------------------------------------
st.sidebar.title("🧁 Doceria App")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Navegue pelas Opções:",
    ["📦 Gestão de Produtos", "📋 Fichas Técnicas"]
)

# =============================================================================
# PÁGINA 1: GESTÃO DE PRODUTOS (CADASTRAR, EDITAR, EXCLUIR)
# =============================================================================
if pagina == "📦 Gestão de Produtos":
    st.title("📦 Gestão de Produtos / Insumos")
    st.markdown("Cadastre, edite ou exclua os produtos e matérias-primas comprados para a doceria.")

    tab_cad, tab_ger = st.tabs(["➕ Cadastrar Novo", "✏️ Editar / Excluir"])

    # ABA 1: Cadastrar
    with tab_cad:
        st.subheader("Adicionar Novo Produto")
        with st.form("form_novo_prod", clear_on_submit=True):
            nome = st.text_input("Nome do Produto (ex: Leite Condensado)")
            marca = st.text_input("Marca (ex: Moça)")
            
            col_a, col_b = st.columns(2)
            with col_a:
                preco = st.number_input("Preço de Compra da Embalagem (R$)", min_value=0.01, step=0.50, format="%.2f")
            with col_b:
                qtd_embalagem = st.number_input("Quantidade na Embalagem", min_value=0.1, step=10.0)
            
            unidade = st.selectbox("Unidade de Medida", ["Gramas (g)", "Litros/Mililitros (ml/L)"])
            
            salvar = st.form_submit_button("Salvar Produto")
            if salvar:
                if nome.strip() == "":
                    st.error("Informe o nome do produto.")
                else:
                    novo = {
                        "id": st.session_state.proximo_id_prod,
                        "nome": nome,
                        "marca": marca,
                        "preco": preco,
                        "qtd_embalagem": qtd_embalagem,
                        "unidade": unidade
                    }
                    st.session_state.produtos = pd.concat([st.session_state.produtos, pd.DataFrame([novo])], ignore_index=True)
                    st.session_state.proximo_id_prod += 1
                    st.success(f"Produto '{nome}' cadastrado com sucesso!")

    # ABA 2: Editar ou Excluir
    with tab_ger:
        st.subheader("Produtos Cadastrados")
        if st.session_state.produtos.empty:
            st.info("Nenhum produto cadastrado.")
        else:
            st.dataframe(st.session_state.produtos, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Editar ou Excluir Produto Específico")
            
            opcoes_p = {r['id']: f"{r['nome']} - {r['marca']}" for _, r in st.session_state.produtos.iterrows()}
            prod_escolhido = st.selectbox("Selecione o produto", options=list(opcoes_p.keys()), format_func=lambda x: opcoes_p[x])
            
            p_dados = st.session_state.produtos[st.session_state.produtos['id'] == prod_escolhido].iloc[0]
            
            with st.form("form_edicao_prod"):
                e_nome = st.text_input("Nome", value=p_dados['nome'])
                e_marca = st.text_input("Marca", value=p_dados['marca'])
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    e_preco = st.number_input("Preço (R$)", value=float(p_dados['preco']), min_value=0.01)
                with col_e2:
                    e_qtd = st.number_input("Qtd Embalagem", value=float(p_dados['qtd_embalagem']), min_value=0.1)
                
                e_unid = st.selectbox("Unidade", ["Gramas (g)", "Litros/Mililitros (ml/L)"], index=0 if p_dados['unidade']=="Gramas (g)" else 1)
                
                col_btn_ed1, col_btn_ed2 = st.columns(2)
                with col_btn_ed1:
                    btn_atualizar = st.form_submit_button("💾 Salvar Alterações")
                with col_btn_ed2:
                    btn_excluir = st.form_submit_button("🗑️ Excluir Produto")
                
                if btn_atualizar:
                    idx = st.session_state.produtos.index[st.session_state.produtos['id'] == prod_escolhido].tolist()[0]
                    st.session_state.produtos.loc[idx] = [prod_escolhido, e_nome, e_marca, e_preco, e_qtd, e_unid]
                    st.success("Produto atualizado com sucesso!")
                    st.rerun()
                
                if btn_excluir:
                    st.session_state.produtos = st.session_state.produtos[st.session_state.produtos['id'] != prod_escolhido]
                    st.warning("Produto excluído!")
                    st.rerun()

# =============================================================================
# PÁGINA 2: FICHAS TÉCNICAS (CRIAR, EDITAR, EXCLUIR E CALCULAR)
# =============================================================================
elif pagina == "📋 Fichas Técnicas":
    st.title("📋 Fichas Técnicas e Receitas")
    st.markdown("Monte
