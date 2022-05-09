from nba_api.stats.endpoints import leaguegamelog
from collections import defaultdict
from datetime import datetime, timedelta

from nba.db.models import Game
from nba.utils import insert_records, convert_datetime_to_str
from nba import dal

def get_game_ids(direction='DESC', season='Playoffs', date_from=None, date_to=None):
	game_ids = set()
	games = leaguegamelog.LeagueGameLog(
		direction=direction, # ASC
		season_type_all_star=season, # Regular Season, Pre Season, Playoffs, All-Star
		date_from_nullable=date_from, # 2022-05-05
		date_to_nullable=date_to).get_dict()

	for r in games['resultSets'][0]['rowSet']:
		# ['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 'VIDEO_AVAILABLE']
		game_ids.add(r[4])

	return list(game_ids)

def seed_games(target_season=None, date_from=convert_datetime_to_str(datetime.now() - timedelta(days=1)), date_to=convert_datetime_to_str(datetime.now() + timedelta(days=1))):
	game_ids = set()
	records = []
	game_lookup = defaultdict(lambda : defaultdict()) # {game_lookup[game_id]['home_team'] = 'MEM'}
	saved_records = {g.game_id: g._asdict() for g in dal.execute('select * from games')}
	for season in ['Regular Season', 'Playoffs']:
		if target_season and season.lower() != target_season.lower(): continue
		games = leaguegamelog.LeagueGameLog(season_type_all_star=season, date_from_nullable=date_from, date_to_nullable=date_to).get_dict()
		for r in games['resultSets'][0]['rowSet']:
			game_id = r[4]
			game_lookup[game_id]['season_id'] = r[0]
			team_name = r[2]
			is_home = 'vs' in r[6]
			game_lookup[game_id]['home_team' if is_home else 'away_team'] = team_name
			game_lookup[game_id]['game_date'] = r[5]
			game_lookup[game_id]['home_score' if is_home else 'away_score'] = r[-3]

		# THIS COMMENTED CODE WORKED FOR REG SEASON BUT NOT PLAYOFFS???
		# for i in range(0, len(games['resultSets'][0]['rowSet']), 2):
		# 	home_team = away_team = home_score = away_score = None
		# 	t1_data = games['resultSets'][0]['rowSet'][i]
		# 	t2_data = games['resultSets'][0]['rowSet'][i+1]
		# 	print(t1_data, '\n', t2_data)
		# 	game_id = t1_data[4]
		# 	if t1_data[4] != t2_data[4]:
		# 		# fucked up - different games
		# 		print('FUCKEDddddd', t1_data, t2_data)
		# 		continue
		# 	# if game_id in game_ids:
		# 	# 	print(t1_data, t2_data)
		# 	# else:
		# 	# 	game_ids.append(game_id)
		# 	if dal.execute('select * from games where game_id=%s', (game_id,)): continue
		# 	t1_is_home = 'vs' in t1_data[6]
		# 	home_team = t1_data[2] if t1_is_home else t2_data[2]
		# 	home_score = t1_data[-3] if t1_is_home else t2_data[-3]
		# 	away_team = t2_data[2] if t1_is_home else t1_data[2]
		# 	away_score = t2_data[-3] if t1_is_home else t1_data[-3]

			# records.append(Game(t1_data[0], game_id, t1_data[5], home_team, away_team, home_score, away_score))
	# insert_records(dal, 'games', records, ignore=False)
	for game_id, game_data in game_lookup.items():
		if not game_data['home_team'] or not game_data['away_team']:
			print('DONT HAVE BOTH TEAMS', game_id, game_data)
			continue
		elif game_id in saved_records:
			if game_data['home_team'] == saved_records[game_id]['home_team'] and game_data['away_team'] == saved_records[game_id]['away_team']:
				if game_data['home_score'] == saved_records[game_id]['home_score']and game_data['away_score'] == saved_records[game_id]['away_score']:
					# already have this record
					continue
				else:
					cprint(f"Old score: {saved_records[game_id]}\nNew score: {game_data}", 'yellow')
					# if we see a new score, assume its correct
					dal.execute('update games set home_score=%s, away_score=%s where game_id=%s', (game_data['home_score'], game_data['away_score'], game_id,))
			else:
				raise(f'We got problems: {saved_records[game_id]}\n{game_data}')


		records.append(Game(game_data['season_id'], game_id, game_data['game_date'], game_data['home_team'], game_data['away_team'], game_data['home_score'], game_data['away_score']))
	insert_records(dal, 'games', records, ignore=False)





if __name__ == '__main__':
	# game_ids = get_game_ids(date_from='2022-05-03')
	# print(game_ids)
	date_from = convert_datetime_to_str(datetime.now() - timedelta(days=3))
	seed_games(target_season='playoffs', date_from=date_from)