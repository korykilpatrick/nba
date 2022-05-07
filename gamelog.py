from nba_api.stats.endpoints import leaguegamelog

from nba.db.models import Game
from nba.utils import insert_records
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

def seed_games():
	game_ids = set()
	records = []
	for season in ['Regular Season', 'Playoffs']:
		games = leaguegamelog.LeagueGameLog(season_type_all_star=season).get_dict()
		home_team = away_team = home_score = away_score = None
		for i in range(0, len(games['resultSets'][0]['rowSet']), 2):
			t1_data = games['resultSets'][0]['rowSet'][i]
			t2_data = games['resultSets'][0]['rowSet'][i+1]
			t1_is_home = 'vs' in t1_data[6]
			home_team = t1_data[2] if t1_is_home else t2_data[2]
			home_score = t1_data[-3] if t1_is_home else t2_data[-3]
			away_team = t2_data[2] if t1_is_home else t1_data[2]
			away_score = t2_data[-3] if t1_is_home else t1_data[-3]

			records.append(Game(t1_data[0], t1_data[4], t1_data[5], home_team, away_team, home_score, away_score))

	insert_records(dal, 'games', records, ignore=False)



if __name__ == '__main__':
	# game_ids = get_game_ids(date_from='2022-05-03')
	# print(game_ids)
	seed_games()