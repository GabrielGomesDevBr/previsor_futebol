import streamlit as st
from data import BrasileiraoData
from models import MatchPredictor
from utils import MatchVisualizer
from ui import UI
from config import APP_CONFIG

class BrasileiraoPredictor:
    def __init__(self):
        self.data = BrasileiraoData()
        self.predictor = MatchPredictor()
        self.visualizer = MatchVisualizer()
        self.ui = UI()
        
        # Configuração da página
        st.set_page_config(
            page_title=APP_CONFIG['title'],
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def run(self):
        # Renderizar cabeçalho
        self.ui.render_header()
        
        # Seleção dos times
        home_team, away_team = self.ui.render_team_selector(self.data.df['Time'].tolist())
        
        if home_team == away_team:
            st.warning("⚠️ Por favor, selecione times diferentes para a análise.")
            return
        
        # Coletar dados dos times
        home_stats = self.data.get_team_stats(home_team)
        away_stats = self.data.get_team_stats(away_team)
        
        # Mostrar estatísticas
        col1, col2 = st.columns(2)
        with col1:
            self.ui.render_team_stats(home_stats, home_team)
        with col2:
            self.ui.render_team_stats(away_stats, away_team)
        
        # Botão de previsão
        if st.button("🎯 Realizar Previsão", use_container_width=True):
            with st.spinner("Analisando dados..."):
                # Coletar dados adicionais
                home_form = self.data.get_recent_form(home_team)
                away_form = self.data.get_recent_form(away_team)
                match_history = self.data.get_match_history(home_team, away_team)
                
                # Realizar previsão
                probabilities = self.predictor.predict_match(
                    home_stats=home_stats,
                    away_stats=away_stats,
                    home_form=home_form,
                    away_form=away_form,
                    home_historical=self.data.team_historical[home_team],
                    away_historical=self.data.team_historical[away_team]
                )
                
                # Mostrar resultados
                self.ui.render_prediction(home_team, away_team, probabilities)
                
                # Gráficos
                col3, col4 = st.columns(2)
                with col3:
                    prob_chart = self.visualizer.create_probability_chart(
                        home_team, away_team, probabilities)
                    st.plotly_chart(prob_chart, use_container_width=True)
                    
                    form_chart = self.visualizer.create_form_chart(
                        [home_form, away_form],
                        [home_team, away_team]
                    )
                    st.plotly_chart(form_chart, use_container_width=True)
                
                with col4:
                    history_chart = self.visualizer.create_history_chart(
                        match_history, home_team, away_team)
                    st.plotly_chart(history_chart, use_container_width=True)
                    
                    comparison_chart = self.visualizer.create_comparison_chart(
                        home_stats, away_stats, 
                        'points_per_game', 
                        'Pontos por Jogo'
                    )
                    st.plotly_chart(comparison_chart, use_container_width=True)
                
                # Análise
                self.ui.render_analysis(home_team, away_team, home_form, away_form)

if __name__ == "__main__":
    app = BrasileiraoPredictor()
    app.run()
