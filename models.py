import numpy as np
from typing import Dict, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from config import MODEL_CONFIG, STATISTICS

class MatchPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.historic_weight = MODEL_CONFIG['HISTORIC_WEIGHT']
        self.recent_form_weight = MODEL_CONFIG['RECENT_FORM_WEIGHT']
        self.current_stats_weight = MODEL_CONFIG['CURRENT_STATS_WEIGHT']
        
    def process_team_data(self, current_stats: Dict, historical_stats: Dict, recent_form: Dict, is_home: bool) -> Dict:
        home_factor = MODEL_CONFIG['HOME_ADVANTAGE_FACTOR'] if is_home else 1/MODEL_CONFIG['HOME_ADVANTAGE_FACTOR']
        
        base_win_rate = (
            current_stats['win_rate'] * self.current_stats_weight +
            (historical_stats['home_win_rate'] if is_home else historical_stats['away_win_rate']) * self.historic_weight +
            recent_form['form_rate'] * self.recent_form_weight
        )
        
        attack_strength = (
            (current_stats['goals_scored_per_game'] / STATISTICS['avg_home_goals']) * STATISTICS['goals_importance'] +
            (1 - current_stats['goals_conceded_per_game'] / STATISTICS['avg_away_goals']) * STATISTICS['defense_importance']
        )
        
        return {
            'win_rate': base_win_rate * home_factor,
            'points_per_game': current_stats['points_per_game'],
            'attack_strength': attack_strength,
            'form': recent_form['form_rate']
        }

class MatchPredictor:
    def __init__(self):
        self.preprocessor = MatchPreprocessor()
        
    def predict_match(self, home_stats: Dict, away_stats: Dict, home_form: Dict, away_form: Dict,
                     home_historical: Dict, away_historical: Dict) -> Tuple[float, float, float]:
        
        # Processar dados dos times
        home_processed = self.preprocessor.process_team_data(home_stats, home_historical, home_form, True)
        away_processed = self.preprocessor.process_team_data(away_stats, away_historical, away_form, False)
        
        # Calcular probabilidade base de vitória
        base_prob_home = home_processed['win_rate'] * (home_processed['attack_strength'] / away_processed['attack_strength'])
        base_prob_away = away_processed['win_rate'] * (away_processed['attack_strength'] / home_processed['attack_strength'])
        
        # Ajustar com forma recente
        form_factor_home = 1 + (home_processed['form'] - 0.5) * 0.2
        form_factor_away = 1 + (away_processed['form'] - 0.5) * 0.2
        
        prob_home = base_prob_home * form_factor_home
        prob_away = base_prob_away * form_factor_away
        
        # Calcular probabilidade de empate baseada na proximidade dos times
        strength_diff = abs(home_processed['attack_strength'] - away_processed['attack_strength'])
        form_diff = abs(home_processed['form'] - away_processed['form'])
        
        base_draw = MODEL_CONFIG['DEFAULT_DRAW_RATE']
        draw_factor = 1 + (1 - (strength_diff + form_diff) / 2)
        prob_draw = base_draw * draw_factor
        
        # Normalizar probabilidades
        return self._normalize_probabilities(prob_home, prob_draw, prob_away)
    
    def _normalize_probabilities(self, home: float, draw: float, away: float) -> Tuple[float, float, float]:
        # Aplicar limites
        home = np.clip(home, MODEL_CONFIG['MIN_PROBABILITY'], MODEL_CONFIG['MAX_PROBABILITY'])
        away = np.clip(away, MODEL_CONFIG['MIN_PROBABILITY'], MODEL_CONFIG['MAX_PROBABILITY'])
        draw = np.clip(draw, MODEL_CONFIG['MIN_PROBABILITY'], MODEL_CONFIG['MAX_PROBABILITY'])
        
        # Normalizar para soma 1
        total = home + draw + away
        home /= total
        draw /= total
        away /= total
        
        # Garantir mínimo de empates
        min_draw = MODEL_CONFIG['DEFAULT_DRAW_RATE'] * 0.7
        if draw < min_draw:
            excess = min_draw - draw
            draw = min_draw
            home -= excess/2
            away -= excess/2
            
        return home, draw, away
