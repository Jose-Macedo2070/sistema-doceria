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

# Estilização CSS personalizada para um design limpo, tons claros e legibilidade
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
# MENU LATERAL PRINCIPAL COM TEXTOS CLAROS
# -----------------------------------------------------------------------------
st.sidebar.title("🧁 Sistema Doceria")
st.sidebar.markdown("---")

pagina = st.sidebar.radio(
    "Menu Principal:",
    ["📦 Produtos", "📋 Fichas Técnicas"]
)

# =============================================================================
# PÁGINA 1: GESTÃO DE PRODUTOS
# =============================================================================
if pagina == "📦 Produtos":
    st.title("📦 Cadastro e Gestão de Produtos")
    st.markdown("Cadastre, edite ou exclua os produtos e insumos utilizados na sua produção.")

    tab_cad, tab_ger = st.tabs(["➕ Cadastrar Novo Produto", "✏️ Editar ou Excluir Produtos"])

    # ABA 1: Cadastrar Novo Produto
    with tab_cad:
        st.subheader("Informações do Novo Produto")
        with st.form("form_novo_prod", clear_on_submit=True):
            nome = st.text_input("Nome do Produto (ex: Leite Condensado, Chocolate em Pó)")
            marca = st.text_input("Marca do Produto (ex: Moça, Nestlé, Melken)")
            
            col_a, col_b = st.columns(2)
            with col_a:
                preco = st.number_input("Valor pago na embalagem (R$)", min_value=0.01, step=0.50, format="%.2f")
            with col_b:
                qtd_embalagem = st.number_input("Quantidade na embalagem (ex: 395 para gramas ou 1000 para ml)", min_value=0.1, step=10.0)
            
            unidade = st.selectbox("Unidade de medida da embalagem", ["Gramas (g)", "Litros/Mililitros (ml/L)"])
            
            salvar = st.form_submit_button("Salvar Produto")
            if salvar:
                if nome.strip() == "":
                    st.error("O campo 'Nome do Produto' é obrigatório.")
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

    # ABA 2: Editar ou Excluir Produtos
    with tab_ger:
        st.subheader("Lista de Produtos Cadastrados")
        if st.session_state.produtos.empty:
            st.info("Nenhum produto cadastrado até o momento.")
        else:
            st.dataframe(st.session_state.produtos, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Alterar ou Remover Produto Específico")
            
            opcoes_p = {r['id']: f"{r['nome']} - {r['marca']}" for _, r in st.session_state.produtos.iterrows()}
            prod_escolhido = st.selectbox("Selecione o produto que deseja modificar", options=list(opcoes_p.keys()), format_func=lambda x: opcoes_p[x])
            
            p_dados = st.session_state.produtos[st.session_state.produtos['id'] == prod_escolhido].iloc[0]
            
            with st.form("form_edicao_prod"):
                e_nome = st.text_input("Nome do Produto", value=p_dados['nome'])
                e_marca = st.text_input("Marca", value=p_dados['marca'])
                
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    e_preco = st.number_input("Valor da Embalagem (R$)", value=float(p_dados['preco']), min_value=0.01)
                with col_e2:
                    e_qtd = st.number_input("Quantidade na Embalagem", value=float(p_dados['qtd_embalagem']), min_value=0.1)
                
                e_unid = st.selectbox("Unidade de Medida", ["Gramas (g)", "Litros/Mililitros (ml/L)"], index=0 if p_dados['unidade']=="Gramas (g)" else 1)
                
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
                    st.warning("Produto excluído com sucesso!")
                    st.rerun()

# =============================================================================
# PÁGINA 2: FICHAS TÉCNICAS
# =============================================================================
elif pagina == "📋 Fichas Técnicas":
    st.title("📋 Fichas Técnicas e Receitas")
    st.markdown("Monte suas receitas utilizando os produtos cadastrados, calcule automaticamente os custos com 10% de desperdício e defina sua margem de lucro.")

    tab_fich_nova, tab_fich_ger = st.tabs(["➕ Criar Nova Ficha Técnica", "📂 Ver / Excluir Fichas Salvas"])

    # ABA 1: Criar Nova Ficha Técnica
    with tab_fich_nova:
        if st.session_state.produtos.empty:
            st.warning("Cadastre produtos na aba 'Produtos' antes de montar uma ficha técnica.")
        else:
            nome_receita = st.text_input("Nome da Receita ou Doce (ex: Brigadeiro Gourmet, Bolo de Pote)")
            
            st.markdown("---")
            st.subheader("1. Adicionar Ingredientes à Receita")
            
            if 'temp_ingredientes' not in st.session_state:
                st.session_state.temp_ingredientes = []

            op_prod = {row['id']: f"{row['nome']} ({row['marca']}) - R$ {row['preco']:.2f} / {row['qtd_embalagem']}{'g' if row['unidade']=='Gramas (g)' else 'ml'}" 
                       for _, row in st.session_state.produtos.iterrows()}
            
            sel_prod_id = st.selectbox("Escolha o insumo da lista de produtos", options=list(op_prod.keys()), format_func=lambda x: op_prod[x])
            prod_info = st.session_state.produtos[st.session_state.produtos['id'] == sel_prod_id].iloc[0]
            
            unid_str = "g" if prod_info['unidade'] == "Gramas (g)" else "ml"
            qtd_receita = st.number_input(f"Quantidade usada efetivamente na receita ({unid_str})", min_value=0.1, value=100.0, step=10.0)
            
            if st.button("➕ Adicionar Ingrediente"):
                preco_com_desperdicio = prod_info['preco'] * 1.10
                custo_unit_base = preco_com_desperdicio / prod_info['qtd_embalagem']
                custo_item = custo_unit_base * qtd_receita
                
                st.session_state.temp_ingredientes.append({
                    "id_produto": prod_info['id'],
                    "nome": prod_info['nome'],
                    "marca": prod_info['marca'],
                    "qtd_usada": qtd_receita,
                    "unidade": unid_str,
                    "custo": custo_item
                })
                st.success("Ingrediente adicionado com cálculo de 10% de desperdício aplicado!")

            if st.session_state.temp_ingredientes:
                st.markdown("**Ingredientes na receita atual:**")
                df_temp = pd.DataFrame(st.session_state.temp_ingredientes)
                st.dataframe(df_temp[['nome', 'marca', 'qtd_usada', 'unidade', 'custo']].rename(columns={
                    'nome': 'Produto', 'marca': 'Marca', 'qtd_usada': 'Qtd Utilizada', 'unidade': 'Unid', 'custo': 'Custo + 10% Desperdício (R$)'
                }), use_container_width=True)
                
                if st.button("Limpar Lista de Ingredientes"):
                    st.session_state.temp_ingredientes = []
                    st.rerun()

            st.markdown("---")
            st.subheader("2. Custos de Embalagens e Insumos Extras")
            
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                custo_emb = st.number_input("Custo da Embalagem do Doce (R$)", min_value=0.0, value=0.0, step=0.50)
            with col_ex2:
                custo_out = st.number_input("Outros Insumos Externos - Fitas, Adesivos, etc. (R$)", min_value=0.0, value=0.0, step=0.50)
            
            soma_ing = sum(i['custo'] for i in st.session_state.temp_ingredientes) if st.session_state.temp_ingredientes else 0.0
            custo_total_receita = soma_ing + custo_emb + custo_out
            
            st.markdown("---")
            st.subheader("3. Precificação e Margem de Lucro")
            tipo_lucro = st.radio("Como deseja calcular o seu lucro?", ["Porcentagem (%) sobre o custo", "Valor Fixo em Reais (R$)"])
            
            if tipo_lucro == "Porcentagem (%) sobre o custo":
                margem_p = st.number_input("Margem de Lucro Desejada (%)", min_value=0.0,
