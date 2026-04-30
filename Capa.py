import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Saúde",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== ESTILO PERSONALIZADO ====================
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        text-align: center;
    }
    .stExpander {
        background: #f8f9fa;
        border-radius: 10px;
        border: none;
    }
    hr {
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==================== CARREGAMENTO DE DADOS ====================
@st.cache_data
def carregar_dados():
    # Carregar CSV com os separadores corretos
    dados_avc = pd.read_csv("dados_avc.csv", sep=";", encoding='latin-1', on_bad_lines='skip')
    estilo_sono = pd.read_csv("estilo_sono.csv", sep=";", encoding='latin-1', on_bad_lines='skip')
    impacto_midia = pd.read_csv("impacto_midia_saude.csv", sep=";", encoding='latin-1', on_bad_lines='skip')
    
    # Renomear colunas do AVC
    colunas_avc = ['ID', 'Gênero', 'Idade', 'Hipertensão', 'Doença Cardíaca', 'Já se casou', 
                   'Trabalho', 'Residência', 'Nível médio de glicose', 'IMC', 'Tabagismo', 'Histórico Familiar']
    if len(dados_avc.columns) == len(colunas_avc):
        dados_avc.columns = colunas_avc
    
    # Renomear colunas do Estilo Sono
    colunas_sono = ['ID', 'Gênero', 'Idade', 'Ocupação', 'Duração do Sono', 'Qualidade do Sono', 
                    'Nível de Atividade Física', 'Nível de Stress', 'IMC', 'Pressão arterial', 
                    'Frequência Cardíaca', 'Passos Diários', 'Transtorno do Sono']
    if len(estilo_sono.columns) == len(colunas_sono):
        estilo_sono.columns = colunas_sono
    
    # Mapeamento de colunas do impacto_midia
    colunas_midia = {
        'Horas de uso': ['Horas Médias de uso diário', 'Horas Mídias de uso diário', 'Horas de uso', 'Uso diário'],
        'Horas de sono': ['Horas de sono', 'Horas Sono', 'Sleep Hours'],
        'Impacto': ['Impacto geral', 'Impacto', 'Impacto Geral'],
        'Plataforma': ['Plataforma mais EUAda', 'Plataforma mais Usada', 'Plataforma', 'Platform'],
        'Saúde mental': ['Pontuação de saúde mental', 'Saúde mental', 'Mental Health Score']
    }
    
    for novo_nome, possiveis_nomes in colunas_midia.items():
        for nome in possiveis_nomes:
            if nome in impacto_midia.columns:
                if nome != novo_nome:
                    impacto_midia = impacto_midia.rename(columns={nome: novo_nome})
                break
    
    # Converter colunas numéricas
    colunas_numericas_sono = ['Duração do Sono', 'Qualidade do Sono', 'Nível de Stress', 
                              'Nível de Atividade Física', 'Frequência Cardíaca', 'Passos Diários']
    for col in colunas_numericas_sono:
        if col in estilo_sono.columns:
            estilo_sono[col] = pd.to_numeric(estilo_sono[col], errors='coerce')
    
    # Converter colunas numéricas do impacto_midia
    if 'Horas de uso' in impacto_midia.columns:
        impacto_midia['Horas de uso'] = pd.to_numeric(impacto_midia['Horas de uso'], errors='coerce')
    if 'Horas de sono' in impacto_midia.columns:
        impacto_midia['Horas de sono'] = pd.to_numeric(impacto_midia['Horas de sono'], errors='coerce')
    if 'Saúde mental' in impacto_midia.columns:
        impacto_midia['Saúde mental'] = pd.to_numeric(impacto_midia['Saúde mental'], errors='coerce')
    
    # Converter colunas numéricas do AVC
    dados_avc['Idade'] = pd.to_numeric(dados_avc['Idade'], errors='coerce')
    dados_avc['Nível médio de glicose'] = pd.to_numeric(dados_avc['Nível médio de glicose'], errors='coerce')
    dados_avc['IMC'] = pd.to_numeric(dados_avc['IMC'], errors='coerce')
    dados_avc['Hipertensão'] = pd.to_numeric(dados_avc['Hipertensão'], errors='coerce')
    dados_avc['Doença Cardíaca'] = pd.to_numeric(dados_avc['Doença Cardíaca'], errors='coerce')
    dados_avc['Histórico Familiar'] = pd.to_numeric(dados_avc['Histórico Familiar'], errors='coerce')
    
    return dados_avc, estilo_sono, impacto_midia

dados_avc, estilo_sono, impacto_midia = carregar_dados()

# ==================== SESSION STATE ====================
if "pagina" not in st.session_state:
    st.session_state.pagina = "Visão Geral"

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("## Saúde Analytics")
    st.markdown("### Dashboard Integrado")
    st.markdown("---")
    
    pagina = st.radio(
        "Navegação",
        ["Visão Geral", "Análise de AVC", "Qualidade do Sono", "Impacto Digital"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("Dashboard desenvolvido com Streamlit")
    
    page_map = {
        "Visão Geral": "Visão Geral",
        "Análise de AVC": "Dados AVC",
        "Qualidade do Sono": "Estilo de Sono",
        "Impacto Digital": "Impacto de Mídia"
    }
    st.session_state.pagina = page_map[pagina]

# ==================== PÁGINA: VISÃO GERAL ====================
if st.session_state.pagina == "Visão Geral":
    st.markdown('<div class="main-header"><h1 style="margin:0">Saúde em Análise: AVC, Sono e Impacto Digital</h1><p style="margin:0; opacity:0.9">Compreendendo a relação entre fatores de risco cardiovascular, qualidade do sono e hábitos digitais</p></div>', unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📋 Total de Registros AVC", f"{len(dados_avc):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("😴 Registros de Sono", f"{len(estilo_sono):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("📱 Registros de Mídia", f"{len(impacto_midia):,}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        avc_count = len(dados_avc[dados_avc['Histórico Familiar'] == 1])
        pct = avc_count/len(dados_avc)*100 if len(dados_avc) > 0 else 0
        st.metric("⚠️ Histórico de AVC", f"{avc_count:,}", delta=f"{pct:.1f}%", delta_color="inverse")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição por Gênero")
        genero_count = dados_avc['Gênero'].value_counts()
        
        genero_colors = {
            'Masculino': '#3498db',
            'Feminino': '#1a5276',
            'Other': '#5dade2'
        }
        
        colors_list = [genero_colors.get(g, '#3498db') for g in genero_count.index]
        
        fig = px.pie(
            values=genero_count.values, 
            names=genero_count.index,
            title="Proporção por Gênero",
            color_discrete_sequence=colors_list,
            hole=0.4
        )
        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            marker=dict(line=dict(color='white', width=2))
        )
        fig.update_layout(showlegend=True, legend_title="Gênero", height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Distribuição Etária")
        idade_limpa = dados_avc[dados_avc['Idade'] <= 100].copy()
        
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 101]
        labels = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']
        
        idade_limpa['Faixa Etária'] = pd.cut(idade_limpa['Idade'], bins=bins, labels=labels, right=False)
        faixa_counts = idade_limpa['Faixa Etária'].value_counts().sort_index().reset_index()
        faixa_counts.columns = ['Faixa Etária', 'Quantidade']
        
        cores_verdes = ['#a8e6cf', '#7fcdbb', '#55b49f', '#2e9c83', '#1a7a64', '#0a5c4a', '#063d2e', '#002214', '#001a0f', '#000d08']
        cores_verdes = cores_verdes[:len(faixa_counts)]
        
        fig = px.bar(
            faixa_counts,
            x='Faixa Etária',
            y='Quantidade',
            title="Distribuição de Idade por Faixas Etárias",
            labels={'Faixa Etária': 'Faixa Etária (anos)', 'Quantidade': 'Número de Pacientes'},
            color='Faixa Etária',
            color_discrete_sequence=cores_verdes,
            text='Quantidade'
        )
        fig.update_traces(textposition='outside', texttemplate='%{y}')
        fig.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Faixa Etária",
            yaxis_title="Quantidade de Pacientes",
            bargap=0.15
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    st.markdown("---")
    st.subheader("Principais Insights")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**🧬 Fatores de Risco**\n\n• Hipertensão aumenta risco cardíaco\n• Idade avançada é fator principal para AVC")
    with col2:
        st.success("**😴 Qualidade do Sono**\n\n• Maioria tem boa qualidade de sono\n• Transtornos afetam ~30% da amostra")
    with col3:
        st.warning("**📱 Impacto Digital**\n\n• Alto uso correlaciona com menor sono\n• Impacto negativo em ~45% dos casos")

# ==================== PÁGINA: DADOS AVC ====================
elif st.session_state.pagina == "Dados AVC":
    st.title("Análise de Fatores de Risco para AVC")
    st.markdown("---")
    
    # Filtros
    with st.expander("Filtros", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            genero_filter = st.multiselect("Gênero", options=dados_avc['Gênero'].unique(), default=dados_avc['Gênero'].unique())
        with col2:
            idade_max = st.slider("Idade máxima", 0, 100, 100)
    
    dados_filtrados = dados_avc[
        (dados_avc['Gênero'].isin(genero_filter)) &
        (dados_avc['Idade'] <= idade_max)
    ]
    
    st.caption(f"Mostrando {len(dados_filtrados)} registros")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Histórico Familiar de AVC")
        hist_data = dados_filtrados['Histórico Familiar'].value_counts().reset_index()
        hist_data.columns = ['Histórico', 'Quantidade']
        hist_data['Histórico'] = hist_data['Histórico'].map({1: "Com Histórico", 0: "Sem Histórico"})
        
        fig = px.pie(
            hist_data, values='Quantidade', names='Histórico',
            color_discrete_sequence=['#ff6b6b', '#4ecdc4'], hole=0.35
        )
        fig.update_traces(textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Idade vs Nível de Glicose")
        scatter_data = dados_filtrados[['Idade', 'Nível médio de glicose', 'Histórico Familiar', 'Gênero', 'Tabagismo']].copy()
        scatter_data = scatter_data.dropna(subset=['Idade', 'Nível médio de glicose'])
        
        scatter_data['AVC na Família'] = scatter_data['Histórico Familiar'].map({1: "Com Histórico de AVC", 0: "Sem Histórico de AVC"})
        scatter_data['AVC na Família'] = scatter_data['AVC na Família'].fillna("Sem Histórico de AVC")
        
        fig = px.scatter(
            scatter_data,
            x='Idade',
            y='Nível médio de glicose',
            color='AVC na Família',
            size='Idade',
            size_max=10,
            hover_data=['Gênero', 'Tabagismo'],
            title="Relação: Idade x Nível de Glicose",
            labels={'Idade': 'Idade (anos)', 'Nível médio de glicose': 'Nível de Glicose (mg/dL)'},
            color_discrete_sequence=['#4ecdc4', '#ff6b6b'],
            opacity=0.7
        )
        
        z = np.polyfit(scatter_data['Idade'], scatter_data['Nível médio de glicose'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(scatter_data['Idade'].min(), scatter_data['Idade'].max(), 100)
        y_trend = p(x_trend)
        
        fig.add_trace(
            go.Scatter(
                x=x_trend,
                y=y_trend,
                mode='lines',
                name=f'Tendência (coef = {z[0]:.2f})',
                line=dict(color='gray', width=2, dash='dash')
            )
        )
        
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        col_est1, col_est2, col_est3 = st.columns(3)
        with col_est1:
            corr_geral = scatter_data['Idade'].corr(scatter_data['Nível médio de glicose'])
            st.metric("Correlação", f"{corr_geral:.2f}")
        with col_est2:
            st.metric("Glicose Média", f"{scatter_data['Nível médio de glicose'].mean():.1f} mg/dL")
        with col_est3:
            st.metric("Idade Média", f"{scatter_data['Idade'].mean():.1f} anos")
    
    # Resumo dos Indicadores de Risco Cardiovascular
    st.markdown("---")
    st.subheader("Resumo dos Indicadores de Risco Cardiovascular")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pct_hipertensao = (dados_filtrados['Hipertensão'] == 1).mean() * 100
        st.metric("❤️ Hipertensão", f"{pct_hipertensao:.1f}%")
    
    with col2:
        pct_cardiaco = (dados_filtrados['Doença Cardíaca'] == 1).mean() * 100
        st.metric("💔 Doença Cardíaca", f"{pct_cardiaco:.1f}%")
    
    with col3:
        pct_historico = (dados_filtrados['Histórico Familiar'] == 1).mean() * 100
        st.metric("👨‍👩‍👧‍👦 Histórico Familiar", f"{pct_historico:.1f}%")
    
    with col4:
        imc_limpo = dados_filtrados[dados_filtrados['IMC'].notna() & (dados_filtrados['IMC'] < 60)]
        imc_medio = imc_limpo['IMC'].mean() if len(imc_limpo) > 0 else 0
        st.metric("⚖️ IMC Médio", f"{imc_medio:.1f}")
    
    # Distribuição de Tabagismo
    st.markdown("---")
    st.subheader("Distribuição de Tabagismo")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tabagismo_count = dados_filtrados['Tabagismo'].value_counts()
        fig_tab = px.pie(
            values=tabagismo_count.values,
            names=tabagismo_count.index,
            title="Proporção por Tipo de Tabagismo",
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.3
        )
        fig_tab.update_traces(textposition='inside', textinfo='percent+label')
        fig_tab.update_layout(height=350)
        st.plotly_chart(fig_tab, use_container_width=True)
    
    with col2:
        tabagismo_gen = pd.crosstab(dados_filtrados['Gênero'], dados_filtrados['Tabagismo'])
        tabagismo_gen_long = tabagismo_gen.reset_index().melt(id_vars='Gênero', var_name='Tabagismo', value_name='Quantidade')
        
        fig_tab_gen = px.bar(
            tabagismo_gen_long,
            x='Gênero',
            y='Quantidade',
            color='Tabagismo',
            title="Tabagismo por Gênero",
            barmode='group',
            color_discrete_sequence=['#95e1d3', '#f38181', '#f4a261', '#e9c46a']
        )
        fig_tab_gen.update_layout(height=350, legend_title="Tipo de Tabagismo")
        st.plotly_chart(fig_tab_gen, use_container_width=True)
    
    with st.expander("Ver dados completos"):
        st.dataframe(dados_filtrados, use_container_width=True)

# ==================== PÁGINA: ESTILO DO SONO ====================
elif st.session_state.pagina == "Estilo de Sono":
    st.title("Análise de Padrões de Sono")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Transtornos do Sono")
        transtorno_count = estilo_sono['Transtorno do Sono'].value_counts().reset_index()
        transtorno_count.columns = ['Transtorno', 'Quantidade']
        
        colors = {'Nenhum': '#2ecc71', 'Insônia': '#e74c3c', 'Apnéia do Sono': '#f39c12'}
        colors_list = [colors.get(t, '#95a5a6') for t in transtorno_count['Transtorno']]
        
        fig = px.bar(
            transtorno_count, x='Transtorno', y='Quantidade',
            title="Prevalência de Transtornos",
            color='Transtorno', text='Quantidade',
            color_discrete_sequence=colors_list
        )
        fig.update_traces(textposition='outside')
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Qualidade do Sono vs Nível de Estresse")
        
        dados_sono = estilo_sono[['Qualidade do Sono', 'Nível de Stress', 'Transtorno do Sono', 'Duração do Sono', 'Gênero']].copy()
        dados_sono = dados_sono.dropna(subset=['Qualidade do Sono', 'Nível de Stress'])
        
        fig = px.scatter(
            dados_sono,
            x='Qualidade do Sono',
            y='Nível de Stress',
            color='Transtorno do Sono',
            size='Duração do Sono',
            size_max=15,
            hover_data=['Gênero'],
            title="Relação: Qualidade do Sono vs Nível de Estresse",
            labels={
                'Qualidade do Sono': 'Qualidade do Sono (1-10)',
                'Nível de Stress': 'Nível de Estresse (1-10)',
                'Transtorno do Sono': 'Transtorno',
                'Duração do Sono': 'Horas de Sono'
            },
            color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12'],
            opacity=0.7
        )
        
        z = np.polyfit(dados_sono['Qualidade do Sono'], dados_sono['Nível de Stress'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(dados_sono['Qualidade do Sono'].min(), dados_sono['Qualidade do Sono'].max(), 100)
        y_trend = p(x_trend)
        
        fig.add_trace(
            go.Scatter(
                x=x_trend,
                y=y_trend,
                mode='lines',
                name=f'Tendência (coef = {z[0]:.2f})',
                line=dict(color='red', width=3, dash='dash')
            )
        )
        
        fig.update_layout(
            height=500,
            xaxis_title="Qualidade do Sono (1-10)",
            yaxis_title="Nível de Estresse (1-10)",
            legend_title="Transtorno do Sono",
            hovermode='closest',
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray')
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        col_est1, col_est2, col_est3, col_est4 = st.columns(4)
        with col_est1:
            correlacao = dados_sono['Qualidade do Sono'].corr(dados_sono['Nível de Stress'])
            st.metric("Correlação", f"{correlacao:.2f}")
        with col_est2:
            qualidade_media = dados_sono['Qualidade do Sono'].mean()
            st.metric("Qualidade Média", f"{qualidade_media:.1f}/10")
        with col_est3:
            stress_medio = dados_sono['Nível de Stress'].mean()
            st.metric("Estresse Médio", f"{stress_medio:.1f}/10")
        with col_est4:
            sono_medio = dados_sono['Duração do Sono'].mean()
            st.metric("Sono Médio", f"{sono_medio:.1f} horas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição da Qualidade do Sono")
        
        fig_violin = px.violin(
            estilo_sono,
            x='Transtorno do Sono',
            y='Qualidade do Sono',
            color='Transtorno do Sono',
            box=True,
            points='all',
            title="Distribuição da Qualidade do Sono por Transtorno",
            labels={'Transtorno do Sono': 'Transtorno', 'Qualidade do Sono': 'Qualidade do Sono (1-10)'},
            color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12']
        )
        fig_violin.update_traces(
            meanline_visible=True,
            points='all',
            jitter=0.3,
            pointpos=-1.5
        )
        fig_violin.update_layout(
            height=450,
            showlegend=False,
            xaxis_title="Transtorno do Sono",
            yaxis_title="Qualidade do Sono (1-10)"
        )
        st.plotly_chart(fig_violin, use_container_width=True)
        
        st.caption("O gráfico mostra a densidade dos dados: áreas mais largas indicam maior concentração de pessoas")
    
    with col2:
        st.subheader("Análise Multidimensional do Sono")
        
        colunas_interesse = ['Qualidade do Sono', 'Duração do Sono', 'Nível de Stress', 'Nível de Atividade Física']
        colunas_existentes = [col for col in colunas_interesse if col in estilo_sono.columns]
        
        if len(colunas_existentes) >= 3:
            bubble_data = estilo_sono.groupby('Transtorno do Sono').agg({
                'Qualidade do Sono': 'mean',
                'Duração do Sono': 'mean',
                'Nível de Stress': 'mean',
                'Nível de Atividade Física': 'mean',
                'ID': 'count'
            }).reset_index()
            bubble_data.columns = ['Transtorno', 'Qualidade Média', 'Duração Média', 'Stress Médio', 'Atividade Média', 'Quantidade']
            
            fig_bubble = px.scatter(
                bubble_data,
                x='Qualidade Média',
                y='Stress Médio',
                size='Quantidade',
                color='Transtorno',
                hover_name='Transtorno',
                size_max=40,
                title="Qualidade do Sono vs Estresse por Transtorno",
                labels={
                    'Qualidade Média': 'Qualidade do Sono (média)',
                    'Stress Médio': 'Nível de Estresse (média)'
                },
                color_discrete_sequence=['#2ecc71', '#e74c3c', '#f39c12'],
                text='Quantidade'
            )
            fig_bubble.update_traces(textposition='top center')
            fig_bubble.update_layout(height=450)
            st.plotly_chart(fig_bubble, use_container_width=True)
            
            st.caption("Tamanho da bolha = Número de pessoas com o transtorno")
        else:
            st.info("Dados insuficientes para análise multidimensional")
    
    # Métricas rápidas
    st.markdown("---")
    st.subheader("Resumo dos Indicadores de Sono")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pct_sono_ruim = (estilo_sono['Qualidade do Sono'] <= 5).mean() * 100
        st.metric("⚠️ Qualidade Ruim (≤5)", f"{pct_sono_ruim:.1f}%")
    
    with col2:
        pct_stress_alto = (estilo_sono['Nível de Stress'] >= 7).mean() * 100
        st.metric("😰 Estresse Alto (≥7)", f"{pct_stress_alto:.1f}%")
    
    with col3:
        pct_sono_adequado = (estilo_sono['Duração do Sono'] >= 7).mean() * 100
        st.metric("✅ Sono Adequado (≥7h)", f"{pct_sono_adequado:.1f}%")
    
    with col4:
        pct_insonia = (estilo_sono['Transtorno do Sono'] == 'Insônia').mean() * 100
        st.metric("🌙 Taxa de Insônia", f"{pct_insonia:.1f}%")
    
    with st.expander("Ver dados completos"):
        st.dataframe(estilo_sono, use_container_width=True)

# ==================== PÁGINA: IMPACTO DIGITAL ====================
else:
    st.title("Impacto da Mídia Social na Saúde")
    st.markdown("---")
    
    if len(impacto_midia) == 0:
        st.error("Não foi possível carregar os dados de impacto da mídia")
        st.stop()
    
    # Identificar as colunas corretas
    coluna_plataforma = None
    for col in impacto_midia.columns:
        if 'plataforma' in col.lower() or 'Plataforma' in col:
            coluna_plataforma = col
            break
    
    coluna_impacto = None
    for col in impacto_midia.columns:
        if 'impacto' in col.lower() or 'Impacto' in col:
            coluna_impacto = col
            break
    
    coluna_uso = None
    for col in impacto_midia.columns:
        if 'uso' in col.lower() and 'horas' in col.lower():
            coluna_uso = col
            break
    if coluna_uso is None:
        for col in impacto_midia.columns:
            if 'horas' in col.lower():
                coluna_uso = col
                break
    
    coluna_sono_midia = None
    for col in impacto_midia.columns:
        if 'sono' in col.lower():
            coluna_sono_midia = col
            break
    
    coluna_saude_mental = None
    for col in impacto_midia.columns:
        if 'saúde' in col.lower() or 'mental' in col.lower():
            coluna_saude_mental = col
            break
    
    # Gráfico 1: Top Plataformas
    if coluna_plataforma:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Top 10 Plataformas Mais Usadas")
            plat_count = impacto_midia[coluna_plataforma].value_counts().head(10).reset_index()
            plat_count.columns = ['Plataforma', 'Quantidade']
            plat_count = plat_count.sort_values('Quantidade', ascending=True)
            
            fig = px.bar(
                plat_count, 
                x='Quantidade', 
                y='Plataforma', 
                orientation='h',
                title="Plataformas Mais Usadas", 
                color='Quantidade',
                color_continuous_scale='Viridis', 
                text='Quantidade'
            )
            fig.update_traces(textposition='outside')
            fig.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if coluna_impacto:
                st.subheader("Impacto na Saúde por Plataforma")
                impacto_plat = pd.crosstab(impacto_midia[coluna_plataforma], impacto_midia[coluna_impacto]).head(8)
                impacto_long = impacto_plat.reset_index().melt(id_vars=coluna_plataforma, var_name='Impacto', value_name='Quantidade')
                
                fig = px.bar(
                    impacto_long, 
                    x=coluna_plataforma, 
                    y='Quantidade', 
                    color='Impacto',
                    title="Impacto Geral por Plataforma", 
                    barmode='stack',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig.update_layout(xaxis_tickangle=-45, height=500)
                st.plotly_chart(fig, use_container_width=True)
    
    # Gráfico 2: Uso vs Sono
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Horas de Uso vs Horas de Sono")
        
        if coluna_uso and coluna_sono_midia:
            df_scatter = impacto_midia[[coluna_uso, coluna_sono_midia]].copy()
            if coluna_impacto:
                df_scatter['Impacto'] = impacto_midia[coluna_impacto]
            if coluna_saude_mental:
                df_scatter['Saúde Mental'] = impacto_midia[coluna_saude_mental]
            
            df_scatter = df_scatter.dropna(subset=[coluna_uso, coluna_sono_midia])
            
            if len(df_scatter) > 0:
                fig = px.scatter(
                    df_scatter,
                    x=coluna_uso,
                    y=coluna_sono_midia,
                    color='Impacto' if coluna_impacto in df_scatter.columns else None,
                    size='Saúde Mental' if coluna_saude_mental in df_scatter.columns else None,
                    size_max=15,
                    title="Relação: Uso de Mídia Social x Horas de Sono",
                    labels={
                        coluna_uso: 'Horas de Uso por Dia',
                        coluna_sono_midia: 'Horas de Sono por Noite'
                    },
                    opacity=0.7,
                    color_discrete_sequence=px.colors.qualitative.Set1
                )
                
                if len(df_scatter) > 1:
                    z = np.polyfit(df_scatter[coluna_uso], df_scatter[coluna_sono_midia], 1)
                    p = np.poly1d(z)
                    x_trend = np.linspace(df_scatter[coluna_uso].min(), df_scatter[coluna_uso].max(), 100)
                    y_trend = p(x_trend)
                    
                    fig.add_trace(
                        go.Scatter(
                            x=x_trend,
                            y=y_trend,
                            mode='lines',
                            name=f'Tendência (coef = {z[0]:.2f})',
                            line=dict(color='red', width=3, dash='dash')
                        )
                    )
                
                fig.update_layout(height=450)
                st.plotly_chart(fig, use_container_width=True)
                
                correlacao = df_scatter[coluna_uso].corr(df_scatter[coluna_sono_midia])
                st.caption(f"Correlação entre uso de mídia e horas de sono: {correlacao:.2f}")
            else:
                st.warning("Dados insuficientes para exibir o gráfico")
        else:
            st.warning(f"Colunas não encontradas. Uso: {coluna_uso}, Sono: {coluna_sono_midia}")
    
    with col2:
        st.subheader("Estresse do Sono vs Riscos Cardiovasculares")
        
        risco_data = dados_avc[['Hipertensão', 'Doença Cardíaca', 'Histórico Familiar']].copy()
        risco_data['Risco Cardiovascular'] = (risco_data['Hipertensão'] + risco_data['Doença Cardíaca'] + risco_data['Histórico Familiar']) / 3
        risco_medio = risco_data['Risco Cardiovascular'].mean()
        
        stress_sono = estilo_sono['Nível de Stress'].dropna()
        stress_medio = stress_sono.mean()
        
        comparativo = pd.DataFrame({
            'Indicador': ['Estresse do Sono', 'Risco Cardiovascular'],
            'Valor Médio': [stress_medio, risco_medio * 10],
            'Cor': ['#f39c12', '#e74c3c']
        })
        
        fig = px.bar(
            comparativo,
            x='Indicador',
            y='Valor Médio',
            color='Indicador',
            title="Comparação: Estresse do Sono vs Risco Cardiovascular",
            labels={'Valor Médio': 'Nível Médio (0-10)', 'Indicador': ''},
            text='Valor Médio',
            color_discrete_sequence=['#f39c12', '#e74c3c']
        )
        fig.update_traces(textposition='outside', texttemplate='%{y:.1f}')
        fig.update_layout(height=450, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        col_est1, col_est2 = st.columns(2)
        with col_est1:
            pct_stress_alto = (estilo_sono['Nível de Stress'] >= 7).mean() * 100
            st.metric("Pessoas com Estresse Alto (≥7)", f"{pct_stress_alto:.1f}%")
        
        with col_est2:
            pct_hipertensao = (dados_avc['Hipertensão'] == 1).mean() * 100
            st.metric("Taxa de Hipertensão", f"{pct_hipertensao:.1f}%")
        
        st.caption("O estresse crônico do sono pode aumentar significativamente os riscos cardiovasculares")
        
        stress_dist = estilo_sono['Nível de Stress'].value_counts().sort_index().reset_index()
        stress_dist.columns = ['Nível de Stress', 'Quantidade']
        
        fig4 = px.bar(
            stress_dist,
            x='Nível de Stress',
            y='Quantidade',
            title="Distribuição Geral do Nível de Estresse",
            color='Nível de Stress',
            color_continuous_scale='Oranges',
            labels={'Nível de Stress': 'Nível de Estresse (1-10)', 'Quantidade': 'Número de Pessoas'}
        )
        fig4.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Métricas rápidas
    st.markdown("---")
    st.subheader("Resumo do Impacto Digital")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if coluna_uso:
            st.metric("📱 Média de Uso Diário", f"{impacto_midia[coluna_uso].mean():.1f} horas")
        else:
            st.metric("📱 Média de Uso Diário", "N/A")
    
    with col2:
        if coluna_impacto:
            pct_pos = (impacto_midia[coluna_impacto] == 'Positivo').mean() * 100
            st.metric("😊 Impacto Positivo", f"{pct_pos:.1f}%")
        else:
            st.metric("😊 Impacto Positivo", "N/A")
    
    with col3:
        if coluna_impacto:
            pct_neg = (impacto_midia[coluna_impacto] == 'Negativo').mean() * 100
            st.metric("😞 Impacto Negativo", f"{pct_neg:.1f}%")
        else:
            st.metric("😞 Impacto Negativo", "N/A")
    
    with st.expander("Ver dados completos"):
        st.dataframe(impacto_midia, use_container_width=True)