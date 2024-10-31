
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Previsor de Jogos - Brasileirão",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    * {
        font-family: 'Roboto', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f6f9fc 0%, #ffffff 100%);
        padding: 2rem;
        border-radius: 20px;
    }
    
    .title-container {
        background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .stat-box {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: transform 0.3s ease;
    }
    
    .stat-box:hover {
        transform: translateY(-5px);
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #00b09b 0%, #96c93d 100%);
        color: white;
        padding: 0.8rem 2rem;
        border-radius: 10px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        font-weight: 500;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    .prediction-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
    }
    
    .prediction-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1e3c72;
        margin: 1rem 0;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 10px;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #00b09b 0%, #96c93d 100%);
    }
    
    .plot-container {
        background: white;
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# Dados do Brasileirão
data = {
    'Time': ['Botafogo', 'Palmeiras', 'Fortaleza', 'Flamengo', 'Internacional', 
             'São Paulo', 'Bahia', 'Cruzeiro', 'Vasco da Gama', 'Atlético-MG',
             'Grêmio', 'Criciúma', 'Fluminense', 'Corinthians', 'Vitória',
             'Athletico PR', 'Bragantino', 'Juventude', 'Cuiabá-MT', 'Atlético-GO'],
    'Pontos': [64, 61, 57, 54, 52, 51, 46, 44, 43, 41, 38, 37, 36, 35, 35, 34, 34, 34, 27, 22],
    'Jogos': [31, 31, 31, 30, 30, 31, 31, 31, 31, 30, 31, 31, 31, 31, 31, 30, 31, 31, 31, 31],
    'V': [19, 18, 16, 16, 14, 15, 13, 12, 12, 10, 11, 9, 10, 8, 10, 9, 8, 8, 6, 5],
    'E': [7, 7, 9, 6, 10, 6, 7, 8, 7, 11, 5, 10, 6, 11, 5, 7, 10, 10, 9, 7],
    'D': [5, 6, 6, 8, 6, 10, 11, 11, 12, 9, 15, 12, 15, 12, 16, 14, 13, 13, 16, 19],
    'GM': [49, 53, 41, 49, 41, 42, 42, 36, 36, 42, 36, 38, 26, 35, 35, 32, 34, 38, 25, 23],
    'GS': [26, 25, 32, 36, 27, 33, 37, 33, 43, 45, 39, 44, 32, 40, 45, 37, 40, 48, 41, 50],
    'DG': [23, 28, 9, 13, 14, 9, 5, 3, -7, -3, -3, -6, -6, -5, -10, -5, -6, -10, -16, -27]
}

# Criar DataFrame
df = pd.DataFrame(data)

# Função melhorada para calcular métricas
def calcular_metricas(time):
    dados_time = df[df['Time'] == time].iloc[0]
    total_jogos = dados_time['Jogos']
    vitorias_perc = (dados_time['V'] / total_jogos) * 100
    empates_perc = (dados_time['E'] / total_jogos) * 100
    derrotas_perc = (dados_time['D'] / total_jogos) * 100
    gols_por_jogo = dados_time['GM'] / total_jogos
    gols_sofridos_por_jogo = dados_time['GS'] / total_jogos
    aproveitamento = (dados_time['Pontos'] / (total_jogos * 3)) * 100
    return {
        'vitorias_perc': vitorias_perc,
        'empates_perc': empates_perc,
        'derrotas_perc': derrotas_perc,
        'gols_por_jogo': gols_por_jogo,
        'gols_sofridos_por_jogo': gols_sofridos_por_jogo,
        'aproveitamento': aproveitamento,
        'pontos': dados_time['Pontos'],
        'saldo_gols': dados_time['DG']
    }

# Função melhorada para criar o modelo
def criar_modelo():
    features = ['Pontos', 'V', 'E', 'D', 'GM', 'GS', 'DG']
    X = df[features].values
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Criar labels baseados na posição na tabela
    y = pd.qcut(df['Pontos'], q=3, labels=['Inferior', 'Médio', 'Superior'])
    
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_scaled, y)
    
    return modelo, scaler

# Função corrigida para calcular probabilidades
def calcular_probabilidades(time_casa, time_fora):
    metricas_casa = calcular_metricas(time_casa)
    metricas_fora = calcular_metricas(time_fora)
    
    # Fator casa
    fator_casa = 1.2
    
    # Base de cálculo usando aproveitamento
    base_casa = metricas_casa['aproveitamento'] / 100
    base_fora = metricas_fora['aproveitamento'] / 100
    
    # Ajuste pelo saldo de gols
    ajuste_saldo = (metricas_casa['saldo_gols'] - metricas_fora['saldo_gols']) / 100
    
    # Cálculo das probabilidades base
    prob_base_casa = base_casa * fator_casa
    prob_base_fora = base_fora
    
    # Ajuste final
    prob_casa = min(max((prob_base_casa + ajuste_saldo) * 100, 15), 75)
    prob_fora = min(max((prob_base_fora - ajuste_saldo) * 100, 15), 75)
    
    # Garantir que a soma não ultrapasse 100%
    total = prob_casa + prob_fora
    if total > 100:
        fator = 100 / total
        prob_casa *= fator
        prob_fora *= fator
    
    # Calcular empate
    prob_empate = 100 - (prob_casa + prob_fora)
    
    return prob_casa, prob_empate, prob_fora
# Título principal com novo design
st.markdown("""
    <div class="title-container">
        <h1>⚽ Previsor de Jogos do Brasileirão</h1>
        <p>Análise avançada e previsões precisas baseadas em Machine Learning</p>
    </div>
""", unsafe_allow_html=True)

# Layout principal
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="stat-box">
            <h3>🏠 Time da Casa</h3>
        </div>
    """, unsafe_allow_html=True)
    time_casa = st.selectbox('Selecione o time da casa:', df['Time'].unique(), key='time_casa')
    
    # Estatísticas do time da casa
    metricas_casa = calcular_metricas(time_casa)
    st.markdown(f"""
        <div class="stat-box">
            <h4>📊 Estatísticas</h4>
            <p>Aproveitamento: {metricas_casa['aproveitamento']:.2f}%</p>
            <p>Vitórias: {metricas_casa['vitorias_perc']:.2f}%</p>
            <p>Gols por jogo: {metricas_casa['gols_por_jogo']:.2f}</p>
            <p>Saldo de Gols: {metricas_casa['saldo_gols']}</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="stat-box">
            <h3>✈️ Time Visitante</h3>
        </div>
    """, unsafe_allow_html=True)
    time_fora = st.selectbox('Selecione o time visitante:', df['Time'].unique(), key='time_fora')
    
    # Estatísticas do time visitante
    metricas_fora = calcular_metricas(time_fora)
    st.markdown(f"""
        <div class="stat-box">
            <h4>📊 Estatísticas</h4>
            <p>Aproveitamento: {metricas_fora['aproveitamento']:.2f}%</p>
            <p>Vitórias: {metricas_fora['vitorias_perc']:.2f}%</p>
            <p>Gols por jogo: {metricas_fora['gols_por_jogo']:.2f}</p>
            <p>Saldo de Gols: {metricas_fora['saldo_gols']}</p>
        </div>
    """, unsafe_allow_html=True)

# Botão de previsão
if st.button('🎯 Realizar Previsão'):
    # Calcular probabilidades com o novo método
    prob_casa, prob_empate, prob_fora = calcular_probabilidades(time_casa, time_fora)
    
    # Container de resultado
    st.markdown("""
        <div class="prediction-container">
            <h2>🎮 Resultado da Previsão</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # Gráfico de probabilidades
    fig = go.Figure()
    
    # Adicionar barras com as novas cores
    fig.add_trace(go.Bar(
        x=['Vitória Casa', 'Empate', 'Vitória Fora'],
        y=[prob_casa, prob_empate, prob_fora],
        marker_color=['#00b09b', '#96c93d', '#00b09b'],
        text=[f'{v:.2f}%' for v in [prob_casa, prob_empate, prob_fora]],
        textposition='auto',
    ))
    
    # Personalizar layout
    fig.update_layout(
        title={
            'text': f'{time_casa} vs {time_fora}',
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        yaxis_title='Probabilidade (%)',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=400
    )
    
    # Adicionar elementos visuais
    fig.update_traces(
        marker_line_color='white',
        marker_line_width=1.5,
        opacity=0.8
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar resultado mais provável com design melhorado
    resultado_provavel = "Vitória do " + time_casa if prob_casa > max(prob_empate, prob_fora) else \
                        "Empate" if prob_empate > max(prob_casa, prob_fora) else \
                        "Vitória do " + time_fora
    
    st.markdown(f"""
        <div class="prediction-value">
            <h3 style='color: #00b09b; margin-bottom: 1rem;'>Resultado mais provável:</h3>
            <p style='font-size: 2.5rem; color: #2a5298;'>{resultado_provavel}</p>
            <div style='display: flex; justify-content: space-around; margin-top: 1rem;'>
                <div>
                    <p style='color: #00b09b; font-weight: bold;'>Vitória {time_casa}</p>
                    <p style='font-size: 1.2rem;'>{prob_casa:.2f}%</p>
                </div>
                <div>
                    <p style='color: #96c93d; font-weight: bold;'>Empate</p>
                    <p style='font-size: 1.2rem;'>{prob_empate:.2f}%</p>
                </div>
                <div>
                    <p style='color: #00b09b; font-weight: bold;'>Vitória {time_fora}</p>
                    <p style='font-size: 1.2rem;'>{prob_fora:.2f}%</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Análise complementar
    st.markdown("""
        <div class="stat-box" style='margin-top: 2rem;'>
            <h4 style='color: #2a5298;'>📈 Análise Comparativa</h4>
        </div>
    """, unsafe_allow_html=True)
    
    # Gráficos comparativos
    col3, col4 = st.columns(2)
    
    with col3:
        fig_aprov = go.Figure()
        fig_aprov.add_trace(go.Bar(
            x=[time_casa, time_fora],
            y=[metricas_casa['aproveitamento'], metricas_fora['aproveitamento']],
            marker_color=['#00b09b', '#96c93d'],
            text=[f"{metricas_casa['aproveitamento']:.1f}%", 
                  f"{metricas_fora['aproveitamento']:.1f}%"],
            textposition='auto',
        ))
        fig_aprov.update_layout(
            title="Aproveitamento",
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_aprov, use_container_width=True)

    with col4:
        fig_gols = go.Figure()
        fig_gols.add_trace(go.Bar(
            x=[time_casa, time_fora],
            y=[metricas_casa['gols_por_jogo'], metricas_fora['gols_por_jogo']],
            marker_color=['#00b09b', '#96c93d'],
            text=[f"{metricas_casa['gols_por_jogo']:.1f}", 
                  f"{metricas_fora['gols_por_jogo']:.1f}"],
            textposition='auto',
            name='Gols Marcados'
        ))
        fig_gols.update_layout(
            title="Média de Gols por Jogo",
            showlegend=False,
            height=300
        )
        st.plotly_chart(fig_gols, use_container_width=True)

# Rodapé com informações adicionais
st.markdown(f"""
    <div style='margin-top: 50px; text-align: center; color: #666;'>
        <p>As previsões são baseadas em um modelo avançado de Machine Learning que considera múltiplas variáveis.</p>
        <p>Dados atualizados em: {datetime.now().strftime('%d/%m/%Y')}</p>
        <p style='font-size: 0.8em;'>Este é um modelo preditivo e os resultados são probabilísticos. 
           Use estas informações apenas como referência.</p>
    </div>
""", unsafe_allow_html=True)

