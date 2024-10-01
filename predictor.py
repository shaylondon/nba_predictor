from nba_api.stats.endpoints import leaguedashteamstats
import pandas as pd

def main():
    team_advanced_stats_last_10 = leaguedashteamstats.LeagueDashTeamStats(last_n_games=10,measure_type_detailed_defense='Advanced',season="2022-23")
    
    team_advanced_stats_last_10_df = team_advanced_stats_last_10.get_data_frames()[0]
    
    pace_last_10 = team_advanced_stats_last_10_df[["TEAM_NAME","PACE_RANK"]].sort_values(by='PACE_RANK')[0:10]

    efg_last_10 = team_advanced_stats_last_10_df[["TEAM_NAME","EFG_PCT_RANK"]].sort_values(by='EFG_PCT_RANK')[0:10]

    print(pace_last_10.set_index("TEAM_NAME").join(efg_last_10.set_index("TEAM_NAME")))
    
    for team in efg_last_10["TEAM_NAME"]:
        if any(pace_last_10["TEAM_NAME"] == team):
            print(team)
    
if __name__ == "__main__": main()
