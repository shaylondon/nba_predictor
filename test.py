from nba_api.stats.endpoints import leaguedashplayerstats

def main():
    career = leaguedashplayerstats.LeagueDashPlayerStats(season='2009-10')

    df = career.get_data_frames()[0]
    df['PTS/G'] = df.apply(lambda row: round(row.PTS / row.GP, 1), axis=1)
    df['AST/G'] = df.apply(lambda row: round(row.AST / row.GP, 1), axis=1)
    df['REB/G'] = df.apply(lambda row: round(row.REB / row.GP, 1), axis=1)
    df = df.sort_values(by='PTS/G',ascending=False)
    season_leaders = df[['PTS_RANK','TEAM_ABBREVIATION','PLAYER_NAME','GP','PTS/G','AST/G','REB/G','FG_PCT','FG3_PCT']][0:10]

    print(season_leaders)
    
if __name__ == "__main__": main()
