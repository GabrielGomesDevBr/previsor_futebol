from datetime import datetime

# Configurações do Modelo
MODEL_CONFIG = {
    'HISTORIC_WEIGHT': 0.3,
    'RECENT_FORM_WEIGHT': 0.3,
    'CURRENT_STATS_WEIGHT': 0.4,
    'HOME_ADVANTAGE_FACTOR': 1.15,
    'MIN_PROBABILITY': 0.10,
    'MAX_PROBABILITY': 0.70,
    'DEFAULT_DRAW_RATE': 0.28,
}

# Nova paleta de cores para análise estatística
VIS_CONFIG = {
    'COLORS': {
        'win': '#2E86C1',      # Azul forte para vitórias
        'draw': '#717D7E',     # Cinza para empates
        'loss': '#E74C3C',     # Vermelho para derrotas
        'primary': '#3498DB',  # Azul principal
        'secondary': '#95A5A6', # Cinza secundário
        'accent': '#2ECC71',   # Verde para destaque
        'background': '#F8F9F9',
        'text': '#2C3E50'
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
