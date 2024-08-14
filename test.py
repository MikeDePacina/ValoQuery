from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
import pandas as pd

load_dotenv()

conn = create_engine(os.getenv('POSTGRES_CONNECTION'))

MATCH_DIMENSION = 'matches_dimension'
MAP_DIMENSION = 'maps_dimension'
PLAYER_DIMENSION = 'players_dimension'
AGENT_DIMENSION = 'agents_dimension'
TEAM_DIMENSION = 'teams_dimension'
FACTS = 'facts'


def load_match_dimension(df_match_details, conn):
    df_match_details.columns = ['match_id', 'match_date', 'winner', 'loser', 'winner_score', 'loser_score', 'picks_and_bans']
    try:
        df_match_details.to_sql(MATCH_DIMENSION, conn, if_exists='append', index=False)
    except Exception as e:
        print(e)

def load_map_dimension(df_map_details, conn):
    df_map_details = df_map_details[['MatchID', 'MapID', 'Map Name', 'Winner', 'Loser', 'Winner Score', 'Winner Attack Score', 'Winner Defense Score', 'Loser Score', 'Loser Attack Score', 'Loser Defense Score']]  
    df_map_details.columns = ['match_id', 'map_id', 'map_name', 'winner', 'loser', 'winner_score', 'winner_attack_score', 'winner_defense_score', 'loser_score', 'loser_attack_score', 'loser_defense_score']

    try:
        df_map_details.to_sql(MAP_DIMENSION, conn, if_exists='append', index=False)
    except Exception as e:
        print(e)

def load_stats_fact(df_stats, conn):
    df_stats.drop(columns=['Player Name', 'Map Name', 'Team Name', 'Agent'], inplace=True)
    df_stats.columns = ['match_id', 'map_id','player_id', 'team_id', 'agent_id', 'rating', 'average_combat_score', 'kills', 'deaths', 'assists', 'first_kills', 'first_deaths']
    df_stats = df_stats[['match_id', 'map_id', 'team_id', 'player_id', 'agent_id', 'rating', 'average_combat_score', 'kills', 'deaths', 'assists', 'first_kills', 'first_deaths']]

    try:
        df_stats.to_sql(FACTS, conn, if_exists='append', index=False)
    except Exception as e:
        print(e)

def load_data_to_database(conn, match_csvs, map_csvs, stats_csvs, N):
    #count of csvs should be equal or N
    for i in range(N):
        df_match_details = pd.read_csv(match_csvs[i])
        df_map_details = pd.read_csv(map_csvs[i])
        df_stats = pd.read_csv(stats_csvs[i])

        #this order of loading data into tables is needed due to foreign key constraints
        load_match_dimension(df_match_details, conn)
        load_map_dimension(df_map_details, conn)
        load_stats_fact(df_stats, conn)


# df_matches = pd.read_csv('./csvs/vct_emea_season2_stage2_playoffs_match_details.csv')
# df_matches.columns = ['match_id', 'match_date', 'winner', 'loser', 'winner_score', 'loser_score', 'picks_and_bans']
# df_matches.to_sql('matches_dimension', conn, if_exists='append', index=False)

# df_maps = pd.read_csv('./csvs/vct_emea_season2_stage2_playoffs_map_details.csv')

# df_maps = df_maps[['MatchID', 'MapID', 'Map Name', 'Winner', 'Loser', 'Winner Score', 'Winner Attack Score', 'Winner Defense Score', 'Loser Score', 'Loser Attack Score', 'Loser Defense Score']]  

# df_maps.columns = ['match_id', 'map_id', 'map_name', 'winner', 'loser', 'winner_score', 'winner_attack_score', 'winner_defense_score', 'loser_score', 'loser_attack_score', 'loser_defense_score']
# df_maps.to_sql('maps_dimension', conn, if_exists='append', index=False)

# df_players = pd.read_csv('./csvs/players.csv')
# df_agents = pd.read_csv('./csvs/agents.csv')
# df_teams = pd.read_csv('./csvs/teams.csv')

# df_players.columns = ['player_id', 'player_name']
# df_agents.columns = ['agent_id', 'agent_name']
# df_teams.columns = ['team_id', 'team_name']

# df_players.to_sql('players_dimension', conn, if_exists='append', index=False)
# df_agents.to_sql('agents_dimension', conn, if_exists='append', index=False)
# df_teams.to_sql('teams_dimension', conn, if_exists='append', index=False)

# df_player_stats = pd.read_csv('./csvs/vct_emea_season2_stage2_playoffs_player_stats.csv')
# df_player_stats.drop(columns=['Player Name', 'Map Name', 'Team Name', 'Agent'], inplace=True)
# df_player_stats.columns = ['match_id', 'map_id','player_id', 'team_id', 'agent_id', 'rating', 'average_combat_score', 'kills', 'deaths', 'assists', 'first_kills', 'first_deaths']
# df_player_stats = df_player_stats[['match_id', 'map_id', 'team_id', 'player_id', 'agent_id', 'rating', 'average_combat_score', 'kills', 'deaths', 'assists', 'first_kills', 'first_deaths']]

# df_player_stats.to_sql(FACTS, conn, if_exists='append', index=False)