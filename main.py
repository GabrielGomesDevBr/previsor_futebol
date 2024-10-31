import streamlit as st
from data import BrasileiraoData
from models import MatchPredictor
from utils import MatchVisualizer
from ui import UI
from config import APP_CONFIG

# Configuração da página deve ser a primeira chamada Streamlit
st.set_page_config(
    page_title=APP_CONFIG['title'],
    layout="wide",
    initial_sidebar_state="expanded"
)

class BrasileiraoPredictor:
    def __init__(self):
        self.data = BrasileiraoData()
        self.predictor = MatchPredictor()
        self.visualizer = MatchVisualizer()
        self.ui = UI()

    def show_guide(self):
        """Mostra o guia de uso da aplicação"""
        st.markdown("""
            <div style='background: white; padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h2>📖 Como usar o Previsor</h2>
                <p>1. Selecione os times que irão se enfrentar</p>
                <p>2. Analise as estatísticas básicas de cada time</p>
                <p>3. Clique em "Realizar Previsão" para ver a análise completa</p>
                <p>4. Observe o nível de confiança e os fatores considerados</p>
                <br>
                <h3>🎯 Níveis de Confiança:</h3>
                <p>★★★★★ Alta Confiança: Maioria dos indicadores favoráveis</p>
                <p>★★★ Média Confiança: Alguns indicadores favoráveis</p>
                <p>★ Baixa Confiança: Poucos indicadores favoráveis</p>
            </div>
        """, unsafe_allow_html=True)
    
    def run(self):
        # Renderizar cabeçalho
        self.ui.render_header()
        
        # Adicionar menu na sidebar
        menu = st.sidebar.selectbox(
            "Menu",
            ["Previsão de Jogos", "Como Usar"]
        )
        
        if menu == "Como Usar":
            self.show_guide()
            return
        
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
            with st.spinner("Analisando dados e calculando probabilidades..."):
                # Coletar dados adicionais
                home_form = self.data.get_recent_form(home_team)
                away_form = self.data.get_recent_form(away_team)
                
                # Realizar previsão
                probabilities = self.predictor.predict_match(
                    home_stats=home_stats,
                    away_stats=away_stats,
                    home_form=home_form,
                    away_form=away_form,
                    home_historical=self.data.team_historical[home_team],
                    away_historical=self.data.team_historical[away_team]
                )
                
                # Mostrar resultados em tabs
                tab1, tab2, tab3 = st.tabs(["📊 Probabilidades", 
                                          "📈 Análise Detalhada",
                                          "🎯 Nível de Confiança"])
                
                with tab1:
                    # Mostrar resultados
                    self.ui.render_prediction(home_team, away_team, probabilities)
                    
                    # Gráfico de probabilidades
                    prob_chart = self.visualizer.create_probability_chart(
                        home_team, away_team, probabilities)
                    st.plotly_chart(prob_chart, use_container_width=True)
                
                with tab2:
                    col3, col4 = st.columns(2)
                    with col3:
                        # Gráfico de forma
                        form_chart = self.visualizer.create_form_comparison(
                            home_form=home_form,
                            away_form=away_form,
                            home_team=home_team,
                            away_team=away_team
                        )
                        st.plotly_chart(form_chart, use_container_width=True)
                    
                    with col4:
                        # Comparação de métricas
                        points_chart = self.visualizer.create_comparison_chart(
                            home_stats,
                            away_stats,
                            'points_per_game',
                            'Pontos por Jogo'
                        )
                        st.plotly_chart(points_chart, use_container_width=True)
                
                with tab3:
                    # Análise de confiança
                    confidence_analysis = self.visualizer.analyze_confidence(
                        home_team=home_team,
                        away_team=away_team,
                        home_form=home_form,
                        away_form=away_form,
                        home_stats=home_stats,
                        away_stats=away_stats,
                        probabilities=probabilities
                    )
                    
                    # Gráfico de confiança
                    confidence_chart = self.visualizer.create_confidence_chart(
                        confidence_analysis)
                    st.plotly_chart(confidence_chart, use_container_width=True)
                    
                    # Detalhes da análise
                    st.markdown(f"""
                        <div style='background: white; padding: 20px; border-radius: 10px; margin-top: 20px;'>
                            <h3>📊 Fatores Analisados:</h3>
                            <ul>
                                {"".join(f"<li>{factor}</li>" for factor in confidence_analysis['home_confidence']['factors'])}
                            </ul>
                            
                            <h3>📈 Análise Detalhada:</h3>
                            <p><b>Diferença de pontos por jogo:</b> {confidence_analysis['points_diff']:.2f}</p>
                            <p><b>Diferença na forma:</b> {confidence_analysis['form_diff']*100:.1f}%</p>
                            <p><b>Diferença nas probabilidades:</b> {confidence_analysis['prob_diff']*100:.1f}%</p>
                            
                            <div style='background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 15px;'>
                                <h4 style='color: #2C3E50;'>🎯 Recomendação Final:</h4>
                                <p style='font-size: 1.2em; font-weight: bold; color: #2C3E50;'>
                                    {confidence_analysis['home_confidence']['description']}
                                </p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Aviso de responsabilidade
                st.markdown("""
                    <div style='background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; text-align: center;'>
                        <p style='color: #666; font-size: 0.9em;'>
                            ⚠️ Esta análise é baseada em dados estatísticos e deve ser usada apenas como referência.
                            O futebol é imprevisível e outros fatores podem influenciar o resultado.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    app = BrasileiraoPredictor()
    app.run()
