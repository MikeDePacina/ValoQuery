CREATE Table maps_dimension(
	map_id integer,
    match_id integer REFERENCES matches_dimension(match_id),
	map_name varchar(50),
	winner varchar(50),
	loser varchar(50),
	winner_score smallint,
	winner_attack_score smallint,
	winner_defense_score smallint,
	loser_score smallint,
	loser_attack_score smallint,
	loser_defense_score smallint,

	CONSTRAINT map_key PRIMARY KEY (map_id, match_id)
);

CREATE TABLE matches_dimension(
	match_id integer,
	match_date date,
	winner varchar(50),
	loser varchar(50),
	winner_score smallint,
	loser_score smallint,
	picks_and_bans text,

	CONSTRAINT matches_key PRIMARY KEY (match_id)
);

CREATE TABLE teams_dimension(
	team_id integer,
	team_name varchar(50),

	CONSTRAINT team_key PRIMARY KEY (team_id)
);

CREATE TABLE players_dimension(
	player_id integer,
	player_name varchar(50),
	
	CONSTRAINT player_key PRIMARY KEY (player_id)
);

CREATE TABLE agents_dimension(
	agent_id integer,
	agent_name varchar(50),
	
	CONSTRAINT agent_key PRIMARY KEY (agent_id)
);


CREATE TABLE facts(
	match_id integer REFERENCES matches_dimension(match_id),
	map_id integer REFERENCES maps_dimension(map_id),
	team_id integer REFERENCES teams_dimension(team_id),
	player_id integer REFERENCES players_dimension(player_id),
	agent_id integer REFERENCES agents_dimension(agent_id),
	rating numeric(3,2),
	average_combat_score smallint,
	kills smallint,
	deaths smallint,
	assists smallint,
	first_kills smallint,
	first_deaths smallint,	

    CONSTRAINT facts_key PRIMARY KEY (match_id, map_id, team_id, player_id, agent_id)
);

