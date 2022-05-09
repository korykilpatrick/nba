# Query nba.live.endpoints.scoreboard and  list games in localTimeZone
from datetime import datetime, timezone
from dateutil import parser
from termcolor import cprint
import re, time
from collections import defaultdict
from nba_api.live.nba.endpoints import boxscore

from nba import dal
from nba.scoreboard import get_live_games
from nba.boxscore import get_live_boxscore, parse_live_boxscore, get_boxscore_traditional, parse_boxscore_traditional
from nba.shot_luck import calculate_shot_luck_score

def live_main():
	games = get_live_games()
	while True:
		for game_id, game_code in games:
			if 'phi' not in game_code.lower(): continue
			try:
				box = get_live_boxscore(game_id)
				home_team, home_score = box['homeTeam']['teamTricode'], box['homeTeam']['score']
				away_team, away_score = box['awayTeam']['teamTricode'], box['awayTeam']['score']
				box_dict = parse_live_boxscore(box)
				home_score_ev, away_score_ev = calculate_shot_luck_score(box_dict, home_team, print_players=True)
				cprint(f"Score:    {home_team} {home_score} {away_team} {away_score}", 'cyan')
				cprint(f"Score EV: {home_team} {home_score_ev} {away_team} {away_score_ev}\n", 'magenta')
			except Exception as e:
				cprint(e, 'red')
		time.sleep(10)

def shot_luck_lookback():
	games = dal.execute('select * from games where game_date > current_date - interval 2 day order by game_date')
	for game in games:
		# if game.home_team not in ['MEM', 'MIN']: continue
		box = get_boxscore_traditional(game.game_id)
		box_dict = parse_boxscore_traditional(box)
		home_score_ev, away_score_ev = calculate_shot_luck_score(box_dict, game.home_team, print_players=False)
		cprint(f"{game.game_date}", 'yellow')
		cprint(f"Score:    {game.home_team} {game.home_score} {game.away_team} {game.away_score}", 'cyan')
		cprint(f"Score EV: {game.home_team} {home_score_ev} {game.away_team} {away_score_ev}", 'magenta')
		print('\n')

if __name__ == '__main__':
	# live_main()
	shot_luck_lookback()

