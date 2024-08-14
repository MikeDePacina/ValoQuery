def isInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


player_stats_columns = [
    "MatchID",
    "MapID",
    "Map Name",
    "PlayerID",
    "Player Name",
    "TeamID",
    "Team Name",
    "AgentID",
    "Agent", 
    "Rating", 
    "Average Combat Score",
    "Kills",
    "Deaths",
    "Assists",
    "First Kills",
    "First Deaths",
]

match_columns = [
    "MatchID",
    "Match Date",
    "Winner",
    "Loser",
    "Winner Score",
    "Loser Score",
    "Picks and Bans",
]

map_columns = [
    "MatchID",
    "MapID",
    "Map Name",
    "Winner",
    "Loser",
    "Winner Score",
    "Winner Attack Score",
    "Winner Defense Score",
    "Loser Score",
    "Loser Attack Score",
    "Loser Defense Score",    
]