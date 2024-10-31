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
        # Criar figura única com os dois indicadores lado a lado
        fig = go.Figure()
        
        # Adicionar indicador para o time da casa
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=home_form['form_rate'] * 100,
            title={'text': f"Forma - {home_team}"},
            domain={'row': 0, 'column': 0},
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
        
        # Adicionar indicador para o time visitante
        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=away_form['form_rate'] * 100,
            title={'text': f"Forma - {away_team}"},
            domain={'row': 0, 'column': 1},
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
        
        # Atualizar layout
        fig.update_layout(
            grid={'rows': 1, 'columns': 2},
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
