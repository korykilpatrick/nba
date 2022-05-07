from nba_api.live.nba.endpoints import boxscore
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import boxscoreadvancedv2
from termcolor import cprint
from collections import defaultdict
import re

from nba.utils import clean_shooting_figs
def get_live_boxscore(game_id):
	# https://github.com/swar/nba_api/blob/master/docs/examples/LiveData.ipynb
	return boxscore.BoxScore(game_id).game.get_dict()

def parse_live_boxscore(box):
	box_dict = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict()))) # box_dict['MEM']['players']['Ja Morant']['pts'] = 30
	for team_dict in [box['homeTeam'], box['awayTeam']]:
		team = team_dict['teamTricode']
		for player in team_dict['players']:
			name = player['name']
			stats = player['statistics']
			fgm, fga, fg_pct, fg2m, fg2a, fg2_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct = clean_shooting_figs(stats['fieldGoalsMade'], stats['fieldGoalsAttempted'], stats['twoPointersMade'], stats['twoPointersAttempted'], stats['threePointersMade'], stats['threePointersAttempted'], stats['freeThrowsMade'], stats['freeThrowsAttempted'])
			box_dict[team]['players'][name]['id'] = player['personId']
			box_dict[team]['players'][name]['pf'] = stats['foulsPersonal']
			box_dict[team]['players'][name]['min'] = stats['minutes']
			box_dict[team]['players'][name]['stl'] = stats['steals']
			box_dict[team]['players'][name]['pts'] = stats['points']
			box_dict[team]['players'][name]['plus_minus'] = stats['plusMinusPoints']
			box_dict[team]['players'][name]['paint_pts'] = stats['pointsInThePaint']
			box_dict[team]['players'][name]['reb'] = stats['pointsInThePaint']
			box_dict[team]['players'][name]['oreb'] = stats['reboundsTotal']
			box_dict[team]['players'][name]['dreb'] = stats['reboundsDefensive']
			box_dict[team]['players'][name]['to'] = stats['turnovers']
			box_dict[team]['players'][name]['fgm'] = fgm
			box_dict[team]['players'][name]['fga'] = fga
			box_dict[team]['players'][name]['fg_pct'] = fg_pct
			box_dict[team]['players'][name]['fg2m'] = fg2m
			box_dict[team]['players'][name]['fg2a'] = fg2a
			box_dict[team]['players'][name]['fg2_pct'] = fg2_pct
			box_dict[team]['players'][name]['fg3m'] = fg3m
			box_dict[team]['players'][name]['fg3a'] = fg3a
			box_dict[team]['players'][name]['fg3_pct'] = fg3_pct
			box_dict[team]['players'][name]['ftm'] = ftm
			box_dict[team]['players'][name]['fta'] = fta
			box_dict[team]['players'][name]['ft_pct'] = ft_pct

	return box_dict

def get_boxscore_traditional(game_id):
	# ['GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY', 'PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'START_POSITION', 'COMMENT', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TO', 'PF', 'PTS', 'PLUS_MINUS']
	return boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id).player_stats.get_dict()

def parse_boxscore_traditional(box):
	box_dict = defaultdict(lambda : defaultdict(lambda : defaultdict(lambda : defaultdict()))) # box_dict['MEM']['players']['Ja Morant']['pts'] = 30
	for player in box['data']:
		team = player[2]
		name = player[5]
		fgm, fga, fg_pct, fg2m, fg2a, fg2_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct = clean_shooting_figs(player[10], player[11], None, None, player[13], player[14], player[16], player[17] )
		box_dict[team]['players'][name]['id'] = player[4]
		box_dict[team]['players'][name]['min'] = player[9] or '0'
		box_dict[team]['players'][name]['fgm'] = fgm
		box_dict[team]['players'][name]['fga'] = fga
		box_dict[team]['players'][name]['fg_pct'] = fg_pct
		box_dict[team]['players'][name]['fg3m'] = fg3m
		box_dict[team]['players'][name]['fg3a'] = fg3a
		box_dict[team]['players'][name]['fg3_pct'] = fg3_pct
		box_dict[team]['players'][name]['fg2m'] = fg2m
		box_dict[team]['players'][name]['fg2a'] = fg2a
		box_dict[team]['players'][name]['fg2_pct'] = fg2_pct
		box_dict[team]['players'][name]['ftm'] = ftm
		box_dict[team]['players'][name]['fta'] = fta
		box_dict[team]['players'][name]['ft_pct'] = ft_pct
		box_dict[team]['players'][name]['oreb'] = player[19] or 0
		box_dict[team]['players'][name]['dreb'] = player[20] or 0
		box_dict[team]['players'][name]['reb'] = player[21] or 0
		box_dict[team]['players'][name]['ast'] = player[22] or 0
		box_dict[team]['players'][name]['stl'] = player[23] or 0
		box_dict[team]['players'][name]['blk'] = player[24] or 0
		box_dict[team]['players'][name]['to'] = player[25] or 0
		box_dict[team]['players'][name]['pf'] = player[26] or 0
		box_dict[team]['players'][name]['pts'] = player[27] or 0
		box_dict[team]['players'][name]['plus_minus'] = player[28] or 0

	return box_dict

def get_boxscore_advanced(game_id):
	# ['GAME_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_CITY', 'PLAYER_ID', 'PLAYER_NAME', 'NICKNAME', 'START_POSITION', 'COMMENT', 'MIN', 'E_OFF_RATING', 'OFF_RATING', 'E_DEF_RATING', 'DEF_RATING', 'E_NET_RATING', 'NET_RATING', 'AST_PCT', 'AST_TOV', 'AST_RATIO', 'OREB_PCT', 'DREB_PCT', 'REB_PCT', 'TM_TOV_PCT', 'EFG_PCT', 'TS_PCT', 'USG_PCT', 'E_USG_PCT', 'E_PACE', 'PACE', 'PACE_PER40', 'POSS', 'PIE']
	return boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id).get_dict()


if __name__ == '__main__':
	game_id = 1 # ?
	# get_live_boxscore('42100202')
	# box = get_boxscore_advanced('0042100231')
	# print(box['resultSets'])
	box = get_boxscore_traditional('0042100231')
	box_dict = parse_boxscore_traditional(box)
	print(box_dict)
	# head = box['headers']
	# print(head)
	print(box['data'])