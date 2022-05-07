# Query nba.live.endpoints.scoreboard and  list games in localTimeZone
from datetime import datetime, timezone
from dateutil import parser
from termcolor import cprint
import re, time
from collections import defaultdict
from nba_api.live.nba.endpoints import boxscore

from nba import dal
from nba.scoreboard import get_live_games
from nba.boxscore import get_live_boxscore, get_past_boxscore
from nba.shot_luck import calculate_shot_luck_score

def live_main():
	games = get_live_games()
	while True:
		for game_id, game_code in games:
			try:
				box = get_live_boxscore(game_id)
				home_team, home_score = box['homeTeam']['teamTricode'], box['homeTeam']['score']
				away_team, away_score = box['awayTeam']['teamTricode'], box['awayTeam']['score']
				home_score_ev, away_score_ev = calculate_shot_luck_score(box, print_players=False)
				cprint(f"Score:    {home_team} {home_score} {away_team} {away_score}", 'cyan')
				cprint(f"Score EV: {home_team} {home_score_ev} {away_team} {away_score_ev}", 'magenta')
			except Exception as e:
				continue
				cprint(e, 'red')
		time.sleep(10)

def shot_luck_lookback():
	games = dal.execute('select * from games where game_date > now() - interval 1 week')
	for game in games:
		box = get_past_boxscore(game.game_id)
		home_score_ev, away_score_ev = calculate_shot_luck_score(box, print_players=False)
		cprint(f"Score:    {game.home_team} {game.home_score} {game.away_team} {game.away_score}", 'cyan')
		cprint(f"Score EV: {game.home_team} {home_score_ev} {game.away_team} {away_score_ev}", 'magenta')

if __name__ == '__main__':
	live_main()
	# shot_luck_lookback()

