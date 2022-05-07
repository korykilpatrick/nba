from collections import namedtuple

Team = namedtuple('Team', ['team_id', 'full_name', 'abbreviation', 'nickname', 'city', 'state', 'year_founded', 'alias'])
Player = namedtuple('Player', ['player_id', 'full_name', 'first_name', 'last_name', 'is_active'])
# PlayerStats = namedtuple('PlayerStats', ['player_id', 'season_id', 'is_postseason', 'team_id', 'team_abbreviation', 'player_age', 'gp', 'gs', 'min', 'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts'])
PlayerStats = namedtuple('PlayerStats', ['player_id', 'season_id', 'is_postseason', 'team_id', 'team_abbreviation', 'player_age', 'gp', 'gs', 'min', 'fgm', 'fga', 'fg_pct', 'fg2m', 'fg2a', 'fg2_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts'])
Game = namedtuple('Game', ['season_id', 'game_id', 'game_date', 'home_team', 'away_team', 'home_score', 'away_score'])