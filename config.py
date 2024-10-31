from datetime import datetime

# Configurações do Modelo
MODEL_CONFIG = {
    'HISTORIC_WEIGHT': 0.3,        # Peso para dados históricos
    'RECENT_FORM_WEIGHT': 0.3,     # Peso para forma recente
    'CURRENT_STATS_WEIGHT': 0.4,   # Peso para estatísticas atuais
    'HOME_ADVANTAGE_FACTOR': 1.15,  # Fator médio de vantagem em casa
    'MIN_PROBABILITY': 0.10,       # Probabilidade mínima para qualquer resultado
    'MAX_PROBABILITY': 0.70,       # Probabilidade máxima para qualquer resultado
    'DEFAULT_DRAW_RATE': 0.28,     # Taxa média histórica de empates no Brasileirão
}

# Configurações de Visualização
VIS_CONFIG = {
    'COLORS': {
        'primary': '#00b09b',
        'secondary': '#96c93d',
        'tertiary': '#2a5298',
        'background': '#ffffff',
        'text': '#333333'
    },
    'CHART_HEIGHT': 400,
    'CHART_WIDTH': 800
}

# Métricas de Avaliação
EVALUATION_METRICS = {
    'accuracy_threshold': 0.65,
    'confidence_threshold': 0.75,
    'min_samples': 10
}

# Constantes Estatísticas
STATISTICS = {
    'avg_home_goals': 1.48,
    'avg_away_goals': 1.12,
    'avg_home_wins': 0.45,
    'avg_draws': 0.28,
    'avg_away_wins': 0.27,
    'goals_importance': 0.35,
    'defense_importance': 0.30,
    'form_importance': 0.35
}

# Configurações da Aplicação
APP_CONFIG = {
    'title': "Previsor do Brasileirão",
    'version': '2.0.0',
    'last_update': datetime.now().strftime('%Y-%m-%d'),
    'debug': False
}
