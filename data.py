import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from config import STATISTICS

class BrasileiraoData:
    def __init__(self):
        self.current_data = {
            'Time': ['Botafogo', 'Palmeiras', 'Fortaleza', 'Flamengo', 'Internacional', 
                    'São Paulo', 'Bahia', 'Cruzeiro', 'Vasco da Gama', 'Atlético-MG',
                    'Grêmio', 'Criciúma', 'Fluminense', 'Corinthians', 'Vitória',
                    'Athletico PR', 'Bragantino', 'Juventude', 'Cuiabá-MT', 'Atlético-GO'],
            'Pontos': [64, 61, 57, 54, 52, 51, 46, 44, 43, 41, 38, 37, 36, 35, 35, 34, 34, 34, 27, 22],
            'Jogos': [31, 31, 31, 30, 30, 31, 31, 31, 31, 30, 31, 31, 31, 31, 31, 30, 31, 31, 31, 31],
            'V': [19, 18, 16, 16, 14, 15, 13, 12, 12, 10, 11, 9, 10, 8, 10, 9, 8, 8, 6, 5],
            'E': [7, 7, 9, 6, 10, 6, 7, 8, 7, 11, 5, 10, 6, 11, 5, 7, 10, 10, 9, 7],
            'D': [5, 6, 6, 8, 6, 10, 11, 11, 12, 9, 15, 12, 15, 12, 16, 14, 13, 13, 16, 19],
            'GM': [49, 53, 41, 49, 41, 42, 42, 36, 36, 42, 36, 38, 26, 35, 35, 32, 34, 38, 25, 23],
            'GS': [26, 25, 32, 36, 27, 33, 37, 33, 43, 45, 39, 44, 32, 40, 45, 37, 40, 48, 41, 50],
            'DG': [23, 28, 9, 13, 14, 9, 5, 3, -7, -3, -3, -6, -6, -5, -10, -5, -6, -10, -16, -27]
        }
        
        self.df = pd.DataFrame(self.current_data)
        self.team_historical = self._generate_team_historical()
    
    def _generate_team_historical(self) -> Dict[str, Dict[str, float]]:
        """
        Gera estatísticas históricas para cada time
        """
        historical = {}
        for team in self.current_data['Time']:
            historical[team] = {
                'home_win_rate': np.random.normal(0.45, 0.05),
                'draw_rate': np.random.normal(0.28, 0.03),
                'away_win_rate': np.random.normal(0.27, 0.05),
                'avg_goals_scored_home': np.random.normal(1.48, 0.2),
                'avg_goals_conceded_home': np.random.normal(1.12, 0.2),
                'avg_goals_scored_away': np.random.normal(1.12, 0.2),
                'avg_goals_conceded_away': np.random.normal(1.48, 0.2)
            }
        return historical
    
    def get_team_stats(self, team: str) -> Dict[str, float]:
        """
        Retorna estatísticas completas de um time
        """
        team_data = self.df[self.df['Time'] == team].iloc[0]
        total_games = team_data['Jogos']
        
        return {
            'current_points': team_data['Pontos'],
            'games_played': total_games,
            'wins': team_data['V'],
            'draws': team_data['E'],
            'losses': team_data['D'],
            'goals_scored': team_data['GM'],
            'goals_conceded': team_data['GS'],
            'goal_difference': team_data['DG'],
            'points_per_game': team_data['Pontos'] / total_games,
            'win_rate': team_data['V'] / total_games,
            'draw_rate': team_data['E'] / total_games,
            'loss_rate': team_data['D'] / total_games,
            'goals_scored_per_game': team_data['GM'] / total_games,
            'goals_conceded_per_game': team_data['GS'] / total_games
        }
    
    def get_match_history(self, team1: str, team2: str) -> Dict[str, float]:
        """
        Simula histórico de confrontos entre dois times
        """
        matches = 10
        team1_wins = np.random.binomial(matches//2, 0.45)
        team2_wins = np.random.binomial(matches//2, 0.45)
        draws = matches - team1_wins - team2_wins
        
        return {
            'total_matches': matches,
            'team1_wins': team1_wins,
            'team2_wins': team2_wins,
            'draws': draws,
            'team1_win_rate': team1_wins / matches,
            'team2_win_rate': team2_wins / matches,
            'draw_rate': draws / matches
        }
    
    def get_recent_form(self, team: str, games: int = 5) -> Dict[str, float]:
        """
        Calcula forma recente do time
        """
        team_data = self.df[self.df['Time'] == team].iloc[0]
        total_points = team_data['Pontos']
        games_played = team_data['Jogos']
        
        points_per_game = total_points / games_played
        recent_points = np.random.binomial(games * 3, points_per_game / 3)
        
        return {
            'recent_points': recent_points,
            'max_possible_points': games * 3,
            'form_rate': recent_points / (games * 3)
        }
