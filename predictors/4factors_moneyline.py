from datetime import datetime

import pandas as pd
import requests
from nba_api.live.nba.endpoints import scoreboard
from nba_api.stats.endpoints import leaguedashteamstats
from pandas import DataFrame
from tabulate import tabulate

from config import *
from over_under import *

def get_total_lines() -> list:
    json_data = get_betting_info()
    lines = []
    for i in range(len(json_data['events'])):
        team1 = json_data['events'][i]['teams'][0]['name'].split(' ')[-1]
        team2 = json_data['events'][i]['teams'][1]['name'].split(' ')[-1]
        dk_total = json_data['events'][i]['lines']['19']['total']['total_over']
        fd_total = json_data['events'][i]['lines']['23']['total']['total_over']
        lines.append([team1, team2, dk_total, fd_total])
    return lines

def overs_last_n_games(top_n_teams: int, last_n_games=None) -> list:
    top_10_efg_last_n_games = efg_last_n_games(last_n_games)[:top_n_teams]
    top_10_pace_last_n_games = pace_last_n_games(last_n_games)[:top_n_teams]
    matchups = get_matchups()
    teams_playing = get_teams_playing()

    last_10_efg_matchups = [entry.split(' ')[-1] for entry in top_10_efg_last_n_games['TEAM_NAME'] if entry.split(' ')[-1] in teams_playing]
    last_10_pace_matchups = [entry.split(' ')[-1] for entry in top_10_pace_last_n_games['TEAM_NAME'] if entry.split(' ')[-1] in teams_playing]

    return [matchup for matchup in matchups if (matchup[0] in last_10_efg_matchups and matchup[1] in last_10_pace_matchups) or (matchup[0] in last_10_pace_matchups and matchup[1] in last_10_efg_matchups)]

def efg_last_n_games(games: int) -> DataFrame:
    team_advanced_stats = get_team_advanced_stats_last_n_games(games)
    efg = team_advanced_stats[['TEAM_NAME','EFG_PCT_RANK', 'EFG_PCT']].sort_values(by='EFG_PCT_RANK')
    print(efg[:10])

    return efg

def pace_last_n_games(games: int) -> DataFrame:
    team_advanced_stats = get_team_advanced_stats_last_n_games(games)
    pace = team_advanced_stats[['TEAM_NAME','PACE_RANK', 'PACE']].sort_values(by='PACE_RANK')
    print(pace[:10])

    return pace

def team_ppg_last_n_games(team_names: list, games=None) -> list:
    teams_ppg: list = []
    team_stats_df = get_team_stats_last_n_games(games)
    team_stats_df['TEAM_PPG']= team_stats_df.apply(lambda row: round(row.PTS / row.GP, 1), axis=1)
    team_stats_df['TEAM_NAME'] = team_stats_df.apply(lambda row: row.TEAM_NAME.split(' ')[-1], axis=1)
    team_ppg_df = team_stats_df[['TEAM_NAME','TEAM_PPG']]
    teams_ppg.append([team_ppg_df.loc[team_ppg_df['TEAM_NAME'] == team_names[0]].iat[0,0], team_ppg_df.loc[team_ppg_df['TEAM_NAME'] == team_names[0]].iat[0,1]])
    teams_ppg.append([team_ppg_df.loc[team_ppg_df['TEAM_NAME'] == team_names[1]].iat[0,0], team_ppg_df.loc[team_ppg_df['TEAM_NAME'] == team_names[1]].iat[0,1]])
    return teams_ppg

def main():
    last_n_games: int = int(input('Last _ Games: '))
    top_n_teams: int = int(input('Top _ Teams: '))
    matchups = overs_last_n_games(top_n_teams,last_n_games)
    if not matchups:
        print('No matchups fit criteria on this date.')
        return
    matchups_with_pts = [avg_total_pts_last_n_games(matchup, last_n_games) for matchup in matchups]
    for over_game in matchups_with_pts:
        for game in get_total_lines():
            if over_game[0] == game[0]:
                over_game.append(game[2])
                over_game.append(game[3])

    # overs = [game for game in matchups_with_pts if game[2] + 10 >= game[3]]

    df = pd.DataFrame(matchups_with_pts,columns=['Away Team','Home Team',f'Last {last_n_games} Games Avg Total Points', 'DraftKings Total Points Line', 'FanDuel Total Points Line'])

    print(tabulate(df, headers='keys', tablefmt='psql', showindex=False))
    
if __name__ == "__main__": main()
