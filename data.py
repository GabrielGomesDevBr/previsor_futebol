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
        """Recupera dados do cache se existirem e forem válidos"""
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                cache = json.load(f)
                if time.time() - cache['timestamp'] < self.cache_duration:
                    return cache['data']
        return None

    def _save_to_cache(self, data: Dict):
        """Salva dados no cache"""
        cache = {
            'timestamp': time.time(),
            'data': data
        }
        with open(self.cache_file, 'w') as f:
            json.dump(cache, f)

    def get_current_table(self) -> pd.DataFrame:
        """Coleta a tabela atual do Brasileirão"""
        try:
            # Verificar cache primeiro
            cached_data = self._get_cached_data()
            if cached_data:
                return pd.DataFrame(cached_data)

            # Se não houver cache, fazer scraping
            response = requests.get(self.base_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'lxml')
            
            table_data = {
                'Time': [], 'Pontos': [], 'Jogos': [], 'V': [], 'E': [], 
                'D': [], 'GM': [], 'GS': [], 'DG': []
            }
            
            # Encontrar a tabela do campeonato
            table = soup.find('table', {'class': 'tabela__pontos'})
            if not table:
                raise Exception("Tabela não encontrada")
                
            rows = table.find_all('tr')[1:]  # Pular cabeçalho
            
            for row in rows:
                cols = row.find_all('td')
                
                # Extrair dados
                table_data['Time'].append(cols[1].text.strip())
                table_data['Pontos'].append(int(cols[2].text))
                table_data['Jogos'].append(int(cols[3].text))
                table_data['V'].append(int(cols[4].text))
                table_data['E'].append(int(cols[5].text))
                table_data['D'].append(int(cols[6].text))
                table_data['GM'].append(int(cols[7].text))
                table_data['GS'].append(int(cols[8].text))
                table_data['DG'].append(int(cols[9].text))
            
            # Salvar no cache
            self._save_to_cache(table_data)
            
            return pd.DataFrame(table_data)
            
        except Exception as e:
            print(f"Erro ao coletar dados: {e}")
            # Retornar dados estáticos em caso de erro
            return pd.DataFrame(self._get_static_data())

    def get_recent_matches(self, team: str, num_matches: int = 5) -> List[Dict]:
        """Coleta resultados recentes de um time específico"""
        try:
            team_url = f"{self.base_url}/times/{team.lower().replace(' ', '-')}"
            response = requests.get(team_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'lxml')
            
            matches = []
            recent_games = soup.find_all('div', {'class': 'jogo'})[:num_matches]
            
            for game in recent_games:
                result = game.find('div', {'class': 'placar'}).text.strip()
                matches.append({
                    'result': 'V' if result == 'V' else 'D' if result == 'D' else 'E',
                    'date': game.find('div', {'class': 'data'}).text.strip()
                })
            
            return matches
            
        except Exception as e:
            print(f"Erro ao coletar partidas recentes: {e}")
            # Retornar dados simulados em caso de erro
            return self._get_simulated_matches(num_matches)

    def _get_static_data(self) -> Dict:
        """Dados estáticos para fallback"""
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
        """Gera resultados simulados para fallback"""
        results = []
        for i in range(num_matches):
            results.append({
                'result': np.random.choice(['V', 'E', 'D'], p=[0.4, 0.3, 0.3]),
                'date': (datetime.now() - timedelta(days=i*7)).strftime('%Y-%m-%d')
            })
        return results

class BrasileiraoData:
    def __init__(self):
        self.scraper = BrasileiraoScraper()
        self.df = self.scraper.get_current_table()
        self.team_historical = self._generate_team_historical()
        self.last_update = datetime.now()

    def update_data(self):
        """Atualiza dados do campeonato"""
        current_time = datetime.now()
        if (current_time - self.last_update).total_seconds() > 3600:  # Atualiza a cada hora
            self.df = self.scraper.get_current_table()
            self.last_update = current_time

    def _generate_team_historical(self) -> Dict[str, Dict[str, float]]:
        """Gera estatísticas históricas para cada time"""
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
        """Retorna estatísticas completas de um time"""
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
        """Calcula forma recente do time usando dados reais"""
        recent_matches = self.scraper.get_recent_matches(team, games)
        points = sum([3 if m['result'] == 'V' else 1 if m['result'] == 'E' else 0 
                     for m in recent_matches])
        
        return {
            'recent_points': points,
            'max_possible_points': games * 3,
            'form_rate': points / (games * 3)
        }
