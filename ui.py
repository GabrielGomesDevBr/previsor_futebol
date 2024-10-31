import streamlit as st
from typing import Dict, List, Tuple
from config import VIS_CONFIG

class UI:
    def __init__(self):
        self.colors = VIS_CONFIG['COLORS']
        self._apply_style()
    
    def _apply_style(self):
        """
        Aplica estilo CSS personalizado
        """
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
            
            * {
                font-family: 'Roboto', sans-serif;
            }
            
            .title-container {
                background: linear-gradient(90deg, #2E86C1 0%, #3498DB 100%);
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
                background: linear-gradient(90deg, #2E86C1 0%, #3498DB 100%);
                color: white;
                padding: 0.8rem 2rem;
                border-radius: 10px;
                border: none;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s ease;
                width: 100%;
            }
            
            .stButton>button:hover {
                transform: translateY(-2px);
            }
            
            .metric-value {
                font-size: 2rem;
                font-weight: bold;
                color: #2E86C1;
            }
            
            .prediction-container {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                margin-top: 2rem;
                text-align: center;
            }
            </style>
        """, unsafe_allow_html=True)
    
    def render_header(self):
        """
        Renderiza o cabeçalho da aplicação
        """
        st.markdown("""
            <div class="title-container">
                <h1>⚽ Previsor do Brasileirão</h1>
                <p>Análise avançada com Machine Learning e Estatísticas</p>
            </div>
        """, unsafe_allow_html=True)
    
    def render_team_selector(self, teams: List[str]) -> Tuple[str, str]:
        """
        Renderiza os seletores de times
        """
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="stat-box"><h3>🏠 Time Mandante</h3></div>', 
                      unsafe_allow_html=True)
            home_team = st.selectbox('Selecione o time da casa:', teams, key='home')
        
        with col2:
            st.markdown('<div class="stat-box"><h3>✈️ Time Visitante</h3></div>', 
                      unsafe_allow_html=True)
            away_team = st.selectbox('Selecione o time visitante:', teams, key='away')
        
        return home_team, away_team
    
    def render_team_stats(self, stats: Dict, title: str):
        """
        Renderiza estatísticas do time
        """
        st.markdown(f"""
            <div class="stat-box">
                <h4>📊 Estatísticas - {title}</h4>
                <div style="display: flex; justify-content: space-between; margin-top: 1rem;">
                    <div>
                        <p>Aproveitamento</p>
                        <div class="metric-value">{stats['points_per_game']*100/3:.1f}%</div>
                    </div>
                    <div>
                        <p>Gols/Jogo</p>
                        <div class="metric-value">{stats['goals_scored_per_game']:.2f}</div>
                    </div>
                    <div>
                        <p>Saldo de Gols</p>
                        <div class="metric-value">{stats['goal_difference']:+d}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    def render_prediction(self, home_team: str, away_team: str, 
                        probabilities: Tuple[float, float, float]):
        """
        Renderiza previsão do jogo
        """
        prob_home, prob_draw, prob_away = probabilities
        
        st.markdown("""
            <div class="prediction-container">
                <h2>🎯 Probabilidades</h2>
            </div>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        with cols[0]:
            self._render_probability(f"Vitória {home_team}", prob_home)
        with cols[1]:
            self._render_probability("Empate", prob_draw)
        with cols[2]:
            self._render_probability(f"Vitória {away_team}", prob_away)
    
    def _render_probability(self, label: str, value: float):
        """
        Renderiza uma probabilidade individual
        """
        st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <p>{label}</p>
                <div class="metric-value">{value*100:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    def render_analysis(self, home_team: str, away_team: str, 
                       home_form: Dict, away_form: Dict):
        """
        Renderiza análise comparativa
        """
        st.markdown(f"""
            <div class="stat-box">
                <h4>📈 Análise da Forma</h4>
                <p>{home_team}: {home_form['form_rate']*100:.1f}% de aproveitamento recente</p>
                <p>{away_team}: {away_form['form_rate']*100:.1f}% de aproveitamento recente</p>
            </div>
        """, unsafe_allow_html=True)
