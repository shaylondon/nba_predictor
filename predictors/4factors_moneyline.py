from datetime import datetime

import pandas as pd
import requests
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leaguedashteamstats
from pandas import DataFrame
from tabulate import tabulate

from config import *
from over_under import *

def get_moneylines() -> list:
    json_data = get_betting_info()
    lines = []
    for i in range(len(json_data['events'])):
        team1 = json_data['events'][i]['teams'][0]['name'].split(' ')[-1]
        team2 = json_data['events'][i]['teams'][1]['name'].split(' ')[-1]
        dk_spread = json_data['events'][i]['lines']['19']['spread']['point_spread_away']
        dk_ml1 = json_data['events'][i]['lines']['19']['moneyline']['moneyline_away']
        dk_ml2 = json_data['events'][i]['lines']['19']['moneyline']['moneyline_home']
        fd_ml1 = json_data['events'][i]['lines']['23']['moneyline']['moneyline_away']
        fd_ml2 = json_data['events'][i]['lines']['23']['moneyline']['moneyline_home']
        lines.append([team1, team2, dk_spread, dk_ml1, dk_ml2, fd_ml1, fd_ml2])
    return lines

def get_team_4factors_stats_last_n_games(games: int) -> DataFrame:
    if games is None:
        team_4factors_stats = leaguedashteamstats.LeagueDashTeamStats()
    else:
        team_4factors_stats = leaguedashteamstats.LeagueDashTeamStats(last_n_games=games,
                                                                      measure_type_detailed_defense='Four Factors')

    return team_4factors_stats.get_data_frames()[0]

def calculate_4factor_score(team: str, games=None) -> float:
    factors_df = get_team_4factors_stats_last_n_games(games)
    factors_df['TEAM_NAME'] = factors_df.apply(lambda row: row.TEAM_NAME.split(' ')[-1], axis=1)
    factors_df.set_index('TEAM_NAME',inplace=True)

    efg_pct: float = factors_df['EFG_PCT'].get(team)
    to_pct: float = factors_df['TM_TOV_PCT'].get(team)
    off_reb_pct: float = factors_df['OREB_PCT'].get(team)
    fta_rate: float = factors_df['FTA_RATE'].get(team)
    pro_score: float = 0.44599*efg_pct - 0.341605*to_pct + 0.155112*off_reb_pct + 0.057293*fta_rate

    op_efg_pct: float = factors_df['OPP_EFG_PCT'].get(team)
    op_to_pct: float = factors_df['OPP_TOV_PCT'].get(team)
    def_reb_pct: float = 1 - factors_df['OPP_OREB_PCT'].get(team)
    op_fta_rate: float = factors_df['OPP_FTA_RATE'].get(team)
    anti_score: float = -0.44599*op_efg_pct + 0.341605*op_to_pct + 0.155112*def_reb_pct - 0.057293*op_fta_rate

    score: float = pro_score + anti_score
    return score


def main():
    last_n_games: int = int(input('Last _ Games: '))
    matchups = get_moneylines()
    for matchup in matchups:
        matchup.insert(2, calculate_4factor_score(matchup[1], last_n_games))
        matchup.insert(2, calculate_4factor_score(matchup[0], last_n_games))

    df = pd.DataFrame(matchups,columns=['Away Team','Home Team',
                                        f'Away Last {last_n_games} Games 4 Factor Rating',
                                        f'Home Last {last_n_games} Games 4 Factor Rating',
                                        'DK Away Spread',
                                        'DK Away ML', 'DK Home ML','FD Away ML', 'FD Home ML'])

    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    
if __name__ == "__main__": main()
