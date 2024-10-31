import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time

class BrasileiraoDataCollector:
    def __init__(self):
        self.base_url = "https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_current_standings(self):
        """
        Coleta dados atuais da tabela do Brasileirão
        """
        try:
            response = requests.get(f"{self.base_url}", headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            data = {
                'Time': [], 'Pontos': [], 'Jogos': [], 'V': [], 'E': [], 
                'D': [], 'GM': [], 'GS': [], 'DG': []
            }
            
            # Adaptar seletores conforme a estrutura do site
            table = soup.find('table', {'class': 'table-standings'})
            rows = table.find_all('tr')[1:]  # Pular cabeçalho
            
            for row in rows:
                cols = row.find_all('td')
                data['Time'].append(cols[1].text.strip())
                data['Pontos'].append(int(cols[2].text))
                data['Jogos'].append(int(cols[3].text))
                data['V'].append(int(cols[4].text))
                data['E'].append(int(cols[5].text))
                data['D'].append(int(cols[6].text))
                data['GM'].append(int(cols[7].text))
                data['GS'].append(int(cols[8].text))
                data['DG'].append(int(cols[9].text))
            
            return pd.DataFrame(data)
        
        except Exception as e:
            print(f"Erro ao coletar dados: {e}")
            return None

    def get_recent_matches(self, team, num_matches=5):
        """
        Coleta resultados recentes de um time específico
        """
        try:
            # URL específica para resultados do time
            team_url = f"{self.base_url}/clube/{team}/resultados"
            response = requests.get(team_url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            matches = []
            # Adaptar seletores conforme a estrutura do site
            recent_games = soup.find_all('div', {'class': 'match'})[:num_matches]
            
            for game in recent_games:
                match_data = {
                    'date': game.find('div', {'class': 'date'}).text,
                    'home_team': game.find('div', {'class': 'home'}).text,
                    'away_team': game.find('div', {'class': 'away'}).text,
                    'score': game.find('div', {'class': 'score'}).text,
                }
                matches.append(match_data)
            
            return matches
        
        except Exception as e:
            print(f"Erro ao coletar partidas recentes: {e}")
            return []

    def update_database(self):
        """
        Atualiza base de dados local com informações mais recentes
        """
        current_data = self.get_current_standings()
        if current_data is not None:
            current_data.to_csv('data/brasileirao_atual.csv', index=False)
            return True
        return False

# Exemplo de uso:
if __name__ == "__main__":
    collector = BrasileiraoDataCollector()
    collector.update_database()
