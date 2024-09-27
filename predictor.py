from nba_api.stats.endpoints import leaguedashteamstats

def main():
    team_advanced_stats = leaguedashteamstats.LeagueDashTeamStats(measure_type_detailed_defense='Advanced')
    
    team_advanced_stats_df = team_advanced_stats.get_data_frames()[0]
    
    pace_efg = team_advanced_stats_df[["TEAM_NAME", "EFG_PCT","PACE"]].sort_values(by='TEAM_NAME')
    
    print(pace_efg)
    
if __name__ == "__main__": main()
