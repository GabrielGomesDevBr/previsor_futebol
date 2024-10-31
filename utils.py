def analyze_confidence(self, home_team: str, away_team: str, 
                      home_form: Dict, away_form: Dict,
                      home_stats: Dict, away_stats: Dict,
                      probabilities: Tuple[float, float, float]) -> Dict:
    """
    Analisa o nível de confiança da previsão baseado nos critérios estabelecidos
    """
    prob_home, prob_draw, prob_away = probabilities
    
    # Calcular diferença de pontos por jogo
    points_diff = home_stats['points_per_game'] - away_stats['points_per_game']
    
    # Análise para time da casa
    home_confidence = {
        'rating': 0,  # 1 a 5 estrelas
        'factors': [],
        'description': ''
    }
    
    # Verificar critérios de alta confiança (5 estrelas)
    high_confidence_factors = []
    if home_form['form_rate'] > 0.66:
        high_confidence_factors.append("Time em boa forma")
    if points_diff > 0.5:
        high_confidence_factors.append("Vantagem significativa em pontos")
    if prob_home > 0.60:
        high_confidence_factors.append("Alta probabilidade de vitória")
    high_confidence_factors.append("Fator casa")  # Já está jogando em casa
    
    # Verificar critérios de média confiança (3 estrelas)
    medium_confidence_factors = []
    if 0.33 <= home_form['form_rate'] <= 0.66:
        medium_confidence_factors.append("Time em forma regular")
    if -0.5 <= points_diff <= 0.5:
        medium_confidence_factors.append("Times equilibrados em pontos")
    if 0.45 <= prob_home <= 0.60:
        medium_confidence_factors.append("Probabilidade moderada")
    
    # Verificar critérios de baixa confiança (1 estrela)
    low_confidence_factors = []
    if home_form['form_rate'] < 0.33:
        low_confidence_factors.append("Time em má forma")
    if prob_home < 0.45:
        low_confidence_factors.append("Baixa probabilidade")
    if abs(prob_home - prob_away) < 0.1:
        low_confidence_factors.append("Probabilidades muito equilibradas")
    
    # Determinar classificação final
    if len(high_confidence_factors) >= 3:
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
    """
    Cria uma visualização do nível de confiança
    """
    # Criar figura com subplot para gauge de confiança
    fig = go.Figure()
    
    # Adicionar indicador de confiança
    fig.add_trace(go.Indicator(
        mode="gauge+number+delta",
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
