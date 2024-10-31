import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Tuple
from config import VIS_CONFIG

class MatchVisualizer:
    def __init__(self):
        self.colors = VIS_CONFIG['COLORS']
    
    def create_probability_chart(self, home_team: str, away_team: str, 
                               probabilities: Tuple[float, float, float]) -> go.Figure:
        prob_home, prob_draw, prob_away = probabilities
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=['Vitória Mandante', 'Empate', 'Vitória Visitante'],
            y=[prob_home * 100, prob_draw * 100, prob_away * 100],
            marker=dict(
                color=[self.colors['win'], 
                      self.colors['draw'],
                      self.colors['loss']],
                line=dict(width=1, color='white')
            ),
            text=[f'{v:.1f}%' for v in [prob_home * 100, prob_draw * 100, prob_away * 100]],
            textposition='auto',
        ))
        
        fig.update_layout(
            title=dict(
                text=f'Probabilidades - {home_team} vs {away_team}',
                x=0.5,
                xanchor='center'
            ),
            yaxis_title='Probabilidade (%)',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False,
            template='plotly_white'
        )
        
        return fig

    def create_form_comparison(self, home_form: Dict, away_form: Dict,
                             home_team: str, away_team: str) -> go.Figure:
        fig = go.Figure()
        
        # Indicador para o time da casa
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=home_form['form_rate'] * 100,
            title={'text': f"Forma - {home_team}"},
            domain={'row': 0, 'column': 0, 'x': [0, 0.45]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': self.colors['win']},
                'steps': [
                    {'range': [0, 33], 'color': self.colors['loss']},
                    {'range': [33, 66], 'color': self.colors['draw']},
                    {'range': [66, 100], 'color': self.colors['win']}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.75,
                    'value': home_form['form_rate'] * 100
                }
            }
        ))
        
        # Indicador para o time visitante
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=away_form['form_rate'] * 100,
            title={'text': f"Forma - {away_team}"},
            domain={'row': 0, 'column': 1, 'x': [0.55, 1]},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': self.colors['win']},
                'steps': [
                    {'range': [0, 33], 'color': self.colors['loss']},
                    {'range': [33, 66], 'color': self.colors['draw']},
                    {'range': [66, 100], 'color': self.colors['win']}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 2},
                    'thickness': 0.75,
                    'value': away_form['form_rate'] * 100
                }
            }
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(t=50, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            template='plotly_white'
        )
        
        return fig
    
    def create_comparison_chart(self, home_stats: Dict, away_stats: Dict,
                              metric: str, title: str) -> go.Figure:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Comparação',
            x=['Mandante', 'Visitante'],
            y=[home_stats[metric], away_stats[metric]],
            marker_color=[self.colors['win'], self.colors['loss']],
            text=[f'{v:.2f}' for v in [home_stats[metric], away_stats[metric]]],
            textposition='auto',
        ))
        
        fig.update_layout(
            title=dict(
                text=title,
                x=0.5,
                xanchor='center'
            ),
            height=300,
            showlegend=False,
            template='plotly_white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, b=0, l=0, r=0)
        )
        
        return fig

    def analyze_confidence(self, home_team: str, away_team: str, 
                         home_form: Dict, away_form: Dict,
                         home_stats: Dict, away_stats: Dict,
                         probabilities: Tuple[float, float, float]) -> Dict:
        prob_home, prob_draw, prob_away = probabilities
        points_diff = home_stats['points_per_game'] - away_stats['points_per_game']
        
        home_confidence = {
            'rating': 0,
            'factors': [],
            'description': ''
        }
        
        # Critérios de alta confiança
        high_confidence_factors = []
        if home_form['form_rate'] > 0.66:
            high_confidence_factors.append("Time em boa forma")
        if points_diff > 0.5:
            high_confidence_factors.append("Vantagem significativa em pontos")
        if prob_home > 0.60:
            high_confidence_factors.append("Alta probabilidade de vitória")
        
        # Critérios de média confiança
        medium_confidence_factors = []
        if 0.33 <= home_form['form_rate'] <= 0.66:
            medium_confidence_factors.append("Time em forma regular")
        if -0.5 <= points_diff <= 0.5:
            medium_confidence_factors.append("Times equilibrados em pontos")
        if 0.45 <= prob_home <= 0.60:
            medium_confidence_factors.append("Probabilidade moderada")
        
        # Critérios de baixa confiança
        low_confidence_factors = []
        if home_form['form_rate'] < 0.33:
            low_confidence_factors.append("Time em má forma")
        if prob_home < 0.45:
            low_confidence_factors.append("Baixa probabilidade")
        if abs(prob_home - prob_away) < 0.1:
            low_confidence_factors.append("Probabilidades muito equilibradas")
        
        # Determinar classificação
        if len(high_confidence_factors) >= 2:
            home_confidence['rating'] = 5
            home_confidence['description'] = "Alta confiança ★★★★★"
            home_confidence['factors'] = high_confidence_factors
        elif len(medium_confidence_factors) >= 2:
            home_confidence['rating'] = 3
            home_confidence['description'] = "Média confiança ★★★"
            home_confidence['factors'] = medium_confidence_factors
        else:
            home_confidence['rating'] = 1
            home_confidence['description'] = "Baixa confiança ★"
            home_confidence['factors'] = low_confidence_factors
        
        return {
            'home_confidence': home_confidence,
            'points_diff': points_diff,
            'form_diff': home_form['form_rate'] - away_form['form_rate'],
            'prob_diff': prob_home - prob_away
        }

    def create_confidence_chart(self, analysis: Dict) -> go.Figure:
        fig = go.Figure()
        
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=analysis['home_confidence']['rating'],
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 5], 'tickwidth': 1},
                'bar': {'color': self.colors['win']},
                'steps': [
                    {'range': [0, 2], 'color': self.colors['loss']},
                    {'range': [2, 4], 'color': self.colors['draw']},
                    {'range': [4, 5], 'color': self.colors['win']}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': analysis['home_confidence']['rating']
                }
            },
            title={
                'text': f"Nível de Confiança<br>{analysis['home_confidence']['description']}",
                'font': {'size': 20}
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(t=100, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            template='plotly_white'
        )
        
        return fig
