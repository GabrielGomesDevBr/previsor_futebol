import plotly.graph_objects as go
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
                color=[self.colors['primary'], 
                      self.colors['secondary'],
                      self.colors['primary']],
                line=dict(width=1, color='white')
            ),
            text=[f'{v:.1f}%' for v in [prob_home * 100, prob_draw * 100, prob_away * 100]],
            textposition='auto',
        ))
        
        fig.update_layout(
            title=f'{home_team} vs {away_team}',
            yaxis_title='Probabilidade (%)',
            height=VIS_CONFIG['CHART_HEIGHT'],
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        return fig
    
    def create_comparison_chart(self, home_stats: Dict, away_stats: Dict, 
                              metric: str, title: str) -> go.Figure:
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=['Mandante', 'Visitante'],
            y=[home_stats[metric], away_stats[metric]],
            marker_color=[self.colors['primary'], self.colors['secondary']],
            text=[f'{v:.2f}' for v in [home_stats[metric], away_stats[metric]]],
            textposition='auto',
        ))
        
        fig.update_layout(
            title=title,
            height=300,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_form_chart(self, recent_forms: List[Dict], team_names: List[str]) -> go.Figure:
        fig = go.Figure()
        
        for team, form in zip(team_names, recent_forms):
            value = form['form_rate'] * 100
            fig.add_trace(go.Indicator(
                mode="gauge+number",
                value=value,
                title={'text': f"Forma - {team}"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': self.colors['primary']},
                    'steps': [
                        {'range': [0, 33], 'color': "lightgray"},
                        {'range': [33, 66], 'color': "gray"},
                        {'range': [66, 100], 'color': "darkgray"}
                    ]
                }
            ))
        
        fig.update_layout(
            grid={'rows': 1, 'columns': 2},
            height=250
        )
        
        return fig
    
    def create_history_chart(self, match_history: Dict, team1: str, team2: str) -> go.Figure:
        labels = ['Vitórias ' + team1, 'Empates', 'Vitórias ' + team2]
        values = [match_history['team1_wins'], match_history['draws'], match_history['team2_wins']]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            marker=dict(colors=[
                self.colors['primary'],
                self.colors['secondary'],
                self.colors['primary']
            ])
        )])
        
        fig.update_layout(
            title="Histórico de Confrontos",
            height=300
        )
        
        return fig
