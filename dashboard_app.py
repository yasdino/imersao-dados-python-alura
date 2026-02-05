import streamlit as st
import pandas as pd
import plotly.express as px

# Identidade visual
cor_areia = "#A68A64"
cor_verde = "#72B296"
cor_neutra = "#E8DED1"
cor_azul = "#86C0CA"
cor_fundo = "#101D20"
cor_sidebar = "#1A2F34"

#  <style> ... </style> é uma “caixinha” de HTML onde o navegador lê CSS.

st.markdown(
    """
    <style>

    /* tipografia global */
    /* aplicar fonte e cor base no documento inteiro e no app; tenta usar uma sequencia de fontes, usa a que funcionar; !important pois ha conflito com o default do st */
   
    html, body, .stApp { 
    font-family: Avantgarde, "TeX Gyre Adventor", "URW Gothic L", sans-serif !important;
    color: #DAD6CE !important; /* cor base */
    }

    /* texto comum */
    /* div eh um bloco generico de html (uma caixa); p significa paragrafo (faz uma nova linha); label eh um rótulo (ex: “Ano”, “Senioridade”) */
    /* div[data-testid="stAppViewContainer"] quer dizer "só aplique isso dentro do container principal do app”

    div[data-testid="stAppViewContainer"] p,
    div[data-testid="stAppViewContainer"] label {
        color: #F4F1EC !important;
        font-weight: 400;
    }

    /* st.subheader (h3) */
    /* span é um “pedaço de texto” inline (não quebra linha); “Dentro do app view container, pegue qualquer h3, e dentro dele pegue o span do texto, e pinte ele.” */

    div[data-testid="stAppViewContainer"] h3 span {
        color: #F7F3EE !important;
        font-weight: 600 !important;
    }

    /* subtitulo (st.markdown) */
    /* pinta os parágrafos do conteúdo principal */ 

        div[data-testid="stAppViewContainer"] p {
        color: #D8D3CB !important;
    }
    
    /* titulo "filtros" */
    /* isso é uma classe (ponto = classe): “pegue todo elemento que tem class sidebar-title e aplique isso” */
    /* 1 rem = 16px. margin = margem externa, a ordem é: topo, direita, baixo, esquerda */
    /* opacity = 1 (totalmente visivel); opacity = 0 (invisivel) */
    
    .sidebar-title{ 
        color: #F4F1EC !important;
        font-size: 1.45rem !important;
        font-weight: 650 !important;
        margin: 0.2rem 0 1rem 0 !important;
        opacity: 1 !important;
    }

    /* div[data-testid="metric-container"] é o container que o Streamlit usa para uma métrica */

    div[data-testid="metric-container"] div {
        color: #F4F1EC !important;
        font-weight: 600;
    }

    /* rótulo “Salário médio”, “Salário máximo” etc. */

    div[data-testid="metric-container"] label {
        color: #F4F1EC !important;
        font-size: 0.85rem;
    }

    /* Plotly (eixos, legendas) */
    /* .js-plotly-plot - classe usada pelo Plotly (biblioteca dos gráficos); nos gráficos (SVG), eixo e legenda sao text; em SVG a cor do texto eh fill, nao color */

    .js-plotly-plot text {
        fill: #F4F1EC !important;
        font-family: Avantgarde, "TeX Gyre Adventor", sans-serif !important;
    }

    /* fundo geral e da sidebar */

    .stApp { 
        background-color: #101D20 !important; 
    }
     
    /* section eh como div, mas usado para partes especificas da pagina */ 

    section[data-testid="stSidebar"] { 
        background-color: #1A2F34 !important; 
    }

    /* tags do multiselect na sidebar */
    /* [data-baseweb="tag"] significa, basicamente, "qualquer elemento que tenha esse atributo" ou seja, que seja uma tag */
    /* > div "filho direto", pega so a div imediatamente dentro de algo */

    section[data-testid="stSidebar"] [data-baseweb="tag"],
    section[data-testid="stSidebar"] [data-baseweb="tag"] > div {
        background-color: #72B296 !important;
        color: #2B2B2B !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        border: 0 !important;
    }

    /* texto das tags; pinta o texto externo */

    section[data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #2B2B2B !important;
    }

    /* botão X das tags; svg é um formato de desenho vetorial (ícones) */

    section[data-testid="stSidebar"] [data-baseweb="tag"] svg {
        color: #2B2B2B !important;
    }

    /* hover do X (círculo/efeito); isso muda a cor quando o mouse passa por cima (:hover) */

    section[data-testid="stSidebar"] [data-baseweb="tag"] svg:hover {
        color: #000000 !important;
    }

    /* divisória do Markdown ("---"); hr eh uma linha horizontal (horizontal rule); border = 0 remove a borda padrao */
    /* rgba: red, green, blue, alpha (opacidade)

    div[data-testid="stMarkdownContainer"] hr,
    .stApp hr {
        border: 0 !important;
        height: 1px !important;
        background: rgba(244, 241, 236, 0.28) !important; /* linha clara */
        margin: 1.6rem 0 !important;
        opacity: 1 !important;
    }

    </style>
    """,
    unsafe_allow_html=True #permite que o Streamlit aceite HTML/CSS no Markdown (senão ele bloqueia)
)

st.set_page_config(
    page_title="Dashboard de Salários na Área de Dados",
    page_icon="🎲", #pode ser logo.png 
    layout="wide", #define a largura, pode ser "centered" (centralizado, estreito) ou "wide", usando quase toda a largura da tela
)
df = pd.read_csv("https://raw.githubusercontent.com/vqrca/dashboard_salarios_dados/refs/heads/main/dados-imersao-final.csv") #pandas para ler link

st.sidebar.markdown('<div class="sidebar-title">Filtros</div>', unsafe_allow_html=True) #barra lateral

# Filtro de Ano
anos_disponiveis = sorted(df['ano'].unique()) #df['ano'] seleciona a coluna ano do df; .unique() pega todos os valores distintos, sem repetir; sorted, ordem crescente
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis) #cria um campo de seleção multípla entre os anos, com o título "Ano"

# Filtro de Senioridade
senioridades_disponiveis = sorted(df['senioridade'].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df['contrato'].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df['tamanho_empresa'].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# --- Filtragem do DataFrame ---
# O dataframe principal é filtrado com base nas seleções do usuario feitas na barra lateral.
df_filtrado = df[
    (df['ano'].isin(anos_selecionados)) & #"O ano dessa linha está entre os anos selecionados pelo usuário?”, se sim - True, se nao - False
    (df['senioridade'].isin(senioridades_selecionadas)) & # & exige que todas as condicoes sejam verdadeiras. ex.: se o user seleciona somente junior, as outras linhas
    (df['contrato'].isin(contratos_selecionados)) & # contendo as outras senioridades sao False, logo, sao executadas, avaliadas e *descartadas*
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# --- Conteúdo Principal ---
st.title("Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.") #subtitulo

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas gerais (Salário anual em USD)")

if not df_filtrado.empty: #.empty verifica se o df tem 0 linhas, se True - vazio, se False - tem pelo menos 1 linha. logo, if not quer dizer: se o df nao estiver vazio
    salario_medio = df_filtrado['usd'].mean()
    salario_maximo = df_filtrado['usd'].max()
    total_registros = df_filtrado.shape[0] #quantidade de linhas
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0] #.mode “Qual(is) valor(es) aparece(m) mais vezes?”; [0] pega o primeiro, se houver empate
else: #executa se o df nao tiver dados, esta aqui para nao quebrar o codigo - atribui valores vazios para as variaveis
    salario_medio = 0
    salario_maximo = 0
    total_registros = 0 
    cargo_mais_frequente = "" #vazio, texto com comprimento de 0

col1, col2, col3, col4 = st.columns(4) #colunas horizontais apresentadas no dashboard, lado a lado
col1.metric("Salário médio", f"${salario_medio:,.0f}") #:,.0f - , separador de milhar/ .0f zero casas decimais. ex.: 75000 → $75,000
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.markdown("---") #cria uma linha horizontal no dashboard

# --- Análises Visuais com Plotly ---

col_graf1, col_graf2 = st.columns(2) #primeira linha

with col_graf1: #possui formato de bloco. significa “Tudo que vier abaixo será renderizado dentro dessa coluna do layout”
    if not df_filtrado.empty:
        top_cargos = df_filtrado.groupby('cargo')['usd'].mean().nlargest(10).sort_values(ascending=True).reset_index() #nlargest(10)=top10
        #agrupa por cargo, calcula o salario medio, faz top 10, ordena do menor para o maior. depois de .groupby, cargo vira indice, entao .reset volta p colunas normais
        grafico_cargos = px.bar( #criando o grafico com plotly (interativo)
            top_cargos,
            x='usd',
            y='cargo',
            orientation='h', #barras horizontais
            title="Top 10 cargos por salário médio",
            labels={'usd': 'Média salarial anual (USD)', 'cargo': ''},
            color_discrete_sequence=[cor_areia]
        )
        grafico_cargos.update_layout(title_x=0.3, 
            yaxis={'categoryorder':'total ascending'},
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)") #title_x=0.1 move o titulo p esquerda
        #categoryorder='total ascending' garante que as barras sigam a ordem correta dos valores
        st.plotly_chart(grafico_cargos, use_container_width=True) #“renderize esse gráfico Plotly ocupando toda a largura disponível da coluna”
    else:
        st.warning("Nenhum dado para exibir no gráfico de cargos.") #caso o grafico nao possa ser gerado

with col_graf2:
    if not df_filtrado.empty:
        grafico_hist = px.histogram(
            df_filtrado,
            x='usd',
            nbins=30, #barras do histograma
            title="Distribuição de salários anuais",
            labels={'usd': 'Faixa salarial (USD)', 'count': ' '},
            color_discrete_sequence=[cor_verde]
        )
        grafico_hist.update_layout(
            title_x=0.3,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)")
        grafico_hist.update_yaxes(title_text="Frequência")
        grafico_hist.update_traces(
            marker_line_color="black", #demarca uma separacao entre as barras (uma borda)
            marker_line_width=1
        )
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de distribuição.")

col_graf3, col_graf4 = st.columns(2) #segunda linha

with col_graf3:
    if not df_filtrado.empty: #caso df_filtrado nao esteja vazio...
        remoto_contagem = df_filtrado['remoto'].value_counts().reset_index() #conte a quantidade de opcoes presentes na coluna 'remoto' 
        #.value_counts() transforma em indice, entao .reset_index() transforma para colunas novamente
        remoto_contagem.columns = ['tipo_trabalho', 'quantidade'] #o que eh cada fatia / o tamanho de cada fatia
        grafico_remoto = px.pie(
            remoto_contagem,
            names='tipo_trabalho', #rótulos das fatias
            values='quantidade', #tamanho de cada fatia
            title='Proporção dos tipos de trabalho', #titulo do grafico
            hole=0.5, #transforma pie (pizza) em donut
            color_discrete_sequence=[
                cor_azul,
                cor_verde,
                cor_areia
            ]
        )
        grafico_remoto.update_traces(textinfo='percent+label') #mostra dentro do grafico o nome do tipo de trabalho e o percentual correspondente
        grafico_remoto.update_layout(
            title_x=0.3, #move levemente para a esquerda, padrao adotado nos outros graficos
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)") 
        st.plotly_chart(grafico_remoto, use_container_width=True) #preenche todo o espaco da coluna (col_graf3)
    else:
        st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

with col_graf4:
    if not df_filtrado.empty:
        df_ds = df_filtrado[df_filtrado['cargo'] == 'Data Scientist'] #cria um subconjunto do df_filtrado, com apenas as linhas cujo cargo eh DS
        #importante: df_filtrado já passou pelos filtros do usuário, df_ds é um recorte ainda mais específico
        media_ds_pais = df_ds.groupby('residencia_iso3')['usd'].mean().reset_index() #pycountry; def iso2_to_iso3(code) - muda US para USA (ex), p/ plotly ler
        #nao precisamos fazer iso2_to_iso3(code) pois isso ja estava pronto na base de dados que pegamos (link no inicio do codigo)
        grafico_paises = px.choropleth(media_ds_pais, #px.choropleth faz o grafico em mapa
            locations='residencia_iso3', #qual pais eh qual 
            color='usd', #a cor do pais representa o salario medio
            color_continuous_scale='Earth', #paleta terrosa
            title='Salário médio de Cientista de Dados por país',
            labels={'usd': 'Salário médio (USD)', 'residencia_iso3': 'País'})
        grafico_paises.update_layout(
            title_x=0.2,
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de países.")

st.markdown("---")

# --- Tabela de Dados Detalhados ---
st.subheader("Dados Detalhados")
st.dataframe(df_filtrado)