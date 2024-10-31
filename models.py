from typing import Dict, Tuple
import numpy as np
from config import MODEL_CONFIG, STATISTICS

class MatchPredictor:
    def __init__(self):
        self.home_advantage = MODEL_CONFIG['HOME_ADVANTAGE_FACTOR']
        self.min_prob = MODEL_CONFIG['MIN_PROBABILITY']
        self.max_prob = MODEL_CONFIG['MAX_PROBABILITY']
        self.default_draw = MODEL_CONFIG['DEFAULT_DRAW_RATE']
    
    def predict_match(self, home_stats: Dict, away_stats: Dict,
                     home_form: Dict, away_form: Dict,
                     home_historical: Dict, away_historical: Dict) -> Tuple[float, float, float]:
        """
        Prediz o resultado de uma partida
        """
        # Calcular força base dos times
        home_strength = self._calculate_team_strength(home_stats, home_form, True)
        away_strength = self._calculate_team_strength(away_stats, away_form, False)
        
        # Calcular probabilidades iniciais
        prob_home = home_strength * self.home_advantage
        prob_away = away_strength
        
        # Ajustar baseado na forma recente
        form_diff = home_form['form_rate'] - away_form['form_rate']
        prob_home *= (1 + form_diff * 0.2)
        prob_away *= (1 - form_diff * 0.2)
        
        # Calcular probabilidade de empate
        prob_draw = self._calculate_draw_probability(home_strength, away_strength)
        
        # Normalizar probabilidades
        return self._normalize_probabilities(prob_home, prob_draw, prob_away)
    
    def _calculate_team_strength(self, stats: Dict, form: Dict, is_home: bool) -> float:
        """
        Calcula a força de um time baseado em suas estatísticas
        """
        ppg_strength = stats['points_per_game'] / 3
        goal_strength = (stats['goals_scored_per_game'] / 
                        (STATISTICS['avg_home_goals'] if is_home else STATISTICS['avg_away_goals']))
        form_strength = form['form_rate']
        
        return (ppg_strength * 0.4 + goal_strength * 0.3 + form_strength * 0.3)
    
    def _calculate_draw_probability(self, home_strength: float, away_strength: float) -> float:
        """
        Calcula a probabilidade de empate baseado na proximidade das forças dos times
        """
        strength_diff = abs(home_strength - away_strength)
        base_draw = self.default_draw
        
        # Quanto mais próximos os times, maior a chance de empate
        if strength_diff < 0.1:
            return base_draw * 1.2
        elif strength_diff < 0.2:
            return base_draw
        else:
            return base_draw * 0.8
    
    def _normalize_probabilities(self, home: float, draw: float, away: float) -> Tuple[float, float, float]:
        """
        Normaliza as probabilidades para somarem 1 e respeita limites mínimos e máximos
        """
        # Aplicar limites
        home = np.clip(home, self.min_prob, self.max_prob)
        away = np.clip(away, self.min_prob, self.max_prob)
        draw = np.clip(draw, self.min_prob, self.max_prob)
        
        # Normalizar
        total = home + draw + away
        return home/total, draw/total, away/total
