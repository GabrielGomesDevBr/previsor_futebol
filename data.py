import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
import json
import os
from config import STATISTICS

class BrasileiraoScraper:
    def __init__(self):
        self.base_url = "https://ge.globo.com/futebol/brasileirao-serie-a/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.cache_file = "brasileirao_cache.json"
        self.cache_duration = 3600  # 1 hora em segundos

    def _get_cached_data(self) -> Dict:
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
                if time.time() - cache['timestamp'] < self.cache_duration:
                    return cache['data']
        return None

    def _save_to_cache(self, data: Dict):
        cache = {
            'timestamp': time.time(),
            'data': data
        }
        with open(self.cache_file, 'w') as f:
            json.dump(cache, f)

    def get_current_table(self) -> pd.DataFrame:
        data = self._get_static_data()  # Começar com dados estáticos
        try:
            cached_data = self._get_cached_data()
            if cached_data:
                return pd.DataFrame(cached_data)

            # Se não houver cache válido, retornar dados estáticos
            return pd.DataFrame(data)
            
        except Exception as e:
            print(f"Erro ao coletar dados: {e}")
            return pd.DataFrame(data)

    def get_recent_matches(self, team: str, num_matches: int = 5) -> List[Dict]:
        try:
            # Encontrar dados do time na tabela atual
            data = self.get_current_table()
            team_data = data[data['Time'] == team].iloc[0]
            
            # Calcular probabilidades baseadas no desempenho atual
            games_played = team_data['Jogos']
            wins = team_data['V']
            draws = team_data['E']
            
            win_prob = wins / games_played
            draw_prob = draws / games_played
            loss_prob = 1 - (win_prob + draw_prob)
            
            # Ajustar probabilidades com base no aproveitamento
            points_per_game = team_data['Pontos'] / games_played
            if points_per_game > 2:  # Time em ótima fase
                win_prob = min(0.7, win_prob * 1.3)
                loss_prob = max(0.1, loss_prob * 0.7)
            elif points_per_game < 1:  # Time em má fase
                win_prob = max(0.1, win_prob * 0.7)
                loss_prob = min(0.7, loss_prob * 1.3)
            
            # Normalizar probabilidades
            total = win_prob + draw_prob + loss_prob
            win_prob /= total
            draw_prob /= total
            loss_prob /= total
            
            # Gerar resultados recentes
            matches = []
            for i in range(num_matches):
                result = np.random.choice(['V', 'E', 'D'], p=[win_prob, draw_prob, loss_prob])
                matches.append({
                    'result': result,
                    'date': (datetime.now() - timedelta(days=i*7)).strftime('%Y-%m-%d'),
                    'points': 3 if result == 'V' else 1 if result == 'E' else 0
                })
            
            return matches
        
        except Exception as e:
            print(f"Erro ao gerar resultados recentes: {e}")
            return self._get_simulated_matches(num_matches)

    def _get_static_data(self) -> Dict:
        return {
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

    def _get_simulated_matches(self, num_matches: int) -> List[Dict]:
        matches = []
        # Probabilidades médias do Brasileirão
        probs = [0.45, 0.28, 0.27]  # Vitória, Empate, Derrota
        
        for i in range(num_matches):
            result = np.random.choice(['V', 'E', 'D'], p=probs)
            matches.append({
                'result': result,
                'date': (datetime.now() - timedelta(days=i*7)).strftime('%Y-%m-%d'),
                'points': 3 if result == 'V' else 1 if result == 'E' else 0
            })
        return matches

class BrasileiraoData:
    def __init__(self):
        self.scraper = BrasileiraoScraper()
        self.df = self.scraper.get_current_table()
        self.team_historical = self._generate_team_historical()
        self.last_update = datetime.now()

    def update_data(self):
        current_time = datetime.now()
        if (current_time - self.last_update).total_seconds() > 3600:
            self.df = self.scraper.get_current_table()
            self.last_update = current_time

    def _generate_team_historical(self) -> Dict[str, Dict[str, float]]:
        historical = {}
        for team in self.df['Time']:
            team_data = self.df[self.df['Time'] == team].iloc[0]
            games_played = team_data['Jogos']
            wins = team_data['V']
            draws = team_data['E']
            
            win_rate = wins / games_played
            draw_rate = draws / games_played
            goals_scored_rate = team_data['GM'] / games_played
            goals_conceded_rate = team_data['GS'] / games_played
            
            historical[team] = {
                'home_win_rate': min(1.0, win_rate * 1.2 + np.random.normal(0, 0.05)),
                'draw_rate': min(1.0, draw_rate + np.random.normal(0, 0.03)),
                'away_win_rate': min(1.0, win_rate * 0.8 + np.random.normal(0, 0.05)),
                'avg_goals_scored_home': max(0, goals_scored_rate * 1.2 + np.random.normal(0, 0.2)),
                'avg_goals_conceded_home': max(0, goals_conceded_rate * 0.8 + np.random.normal(0, 0.2)),
                'avg_goals_scored_away': max(0, goals_scored_rate * 0.8 + np.random.normal(0, 0.2)),
                'avg_goals_conceded_away': max(0, goals_conceded_rate * 1.2 + np.random.normal(0, 0.2))
            }
        return historical

    def get_team_stats(self, team: str) -> Dict[str, float]:
        self.update_data()
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

    def get_recent_form(self, team: str, games: int = 5) -> Dict[str, float]:
        recent_matches = self.scraper.get_recent_matches(team, games)
        
        # Calcular pontos com pesos
        weighted_points = 0
        max_weighted_points = 0
        
        for i, match in enumerate(recent_matches):
            # Jogos mais recentes têm peso maior
            weight = 1 + (games - i) * 0.1
            weighted_points += match['points'] * weight
            max_weighted_points += 3 * weight
        
        # Calcular taxa de forma ponderada
        form_rate = weighted_points / max_weighted_points
        
        # Ajustar com base no aproveitamento geral do time
        team_data = self.df[self.df['Time'] == team].iloc[0]
        season_rate = team_data['Pontos'] / (team_data['Jogos'] * 3)
        
        # Combinar forma recente com aproveitamento geral
        final_form = (form_rate * 0.7) + (season_rate * 0.3)
        
        # Adicionar pequena variação aleatória (±5%)
        final_form = min(1.0, max(0.0, final_form + np.random.normal(0, 0.05)))
        
        points = sum(match['points'] for match in recent_matches)
        
        return {
            'recent_points': points,
            'max_possible_points': games * 3,
            'form_rate': final_form
        }
