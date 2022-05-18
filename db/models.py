from collections import namedtuple

Team = namedtuple('Team', ['team_id', 'full_name', 'abbreviation', 'nickname', 'city', 'state', 'year_founded', 'alias'])
Player = namedtuple('Player', ['player_id', 'full_name', 'first_name', 'last_name', 'is_active'])
# PlayerStats = namedtuple('PlayerStats', ['player_id', 'season_id', 'is_postseason', 'team_id', 'team_abbreviation', 'player_age', 'gp', 'gs', 'min', 'fgm', 'fga', 'fg_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts'])
PlayerStats = namedtuple('PlayerStats', ['player_id', 'season_id', 'is_postseason', 'team_id', 'team_abbreviation', 'player_age', 'gp', 'gs', 'min', 'fgm', 'fga', 'fg_pct', 'fg2m', 'fg2a', 'fg2_pct', 'fg3m', 'fg3a', 'fg3_pct', 'ftm', 'fta', 'ft_pct', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts'])
Game = namedtuple('Game', ['season_id', 'game_id', 'game_date', 'home_team', 'away_team', 'home_score', 'away_score'])

ShotAttempt = namedtuple('ShotAttempt', ['game_id', 'game_event_id', 'player_id', 'team_id', 'period', 'minutes_remaining', 'seconds_remaining', 'event_type', 'action_type', 'shot_type', 'shot_zone_basic', 'shot_zone_area', 'shot_zone_range', 'shot_distance', 'loc_x', 'loc_y', 'shot_attempted_flag', 'shot_made_flag', 'game_date', 'htm_id', 'vtm_id'])