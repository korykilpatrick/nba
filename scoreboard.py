from datetime import datetime, timezone
from dateutil import parser
from termcolor import cprint
from nba_api.live.nba.endpoints import scoreboard

def get_live_games():
	board = scoreboard.ScoreBoard()
	cprint(board.score_board_date, 'magenta', attrs=['bold'])

	games = []
	listed_games = board.games.get_dict()
	for game in listed_games:
		gameTimeLTZ = parser.parse(game["gameTimeUTC"]).replace(tzinfo=timezone.utc).astimezone(tz=None) # my timezone
		cprint(f"{game['gameId']}: {game['awayTeam']['teamName']} vs. {game['homeTeam']['teamName']} @ {gameTimeLTZ}", 'yellow')
		game_id = game['gameId']
		game_code = game['gameCode']
		games.append((game_id, game_code))

	return games

if __name__ == '__main__':
	get_live_games()
