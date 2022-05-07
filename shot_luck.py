from collections import defaultdict
import re
from termcolor import cprint

from nba import dal

def get_base_rates(player_id):
	return dal.callproc('get_base_rates', args=(player_id,), one_or_none=True)

def calculate_shot_luck_score(box, print_players=True):
	"""
	Given a boxscore, calculate our shot-luck adjusted score.
	In here is where we will tinker.
	"""
	score_dict = defaultdict(lambda : defaultdict(list))
	score_ev = []
	for team in [box['homeTeam'], box['awayTeam']]:
		team_score_ev, ev_3, actual_3 = 0, 0, 0
		cprint(f"\n{team['teamName']}", 'white', attrs=['bold'])
		for player in team['players']:
			try:
				player_id = player['personId']
				name = player['name']
				last_name = player['familyName']
				stats = player['statistics'] # a bunch of stats here, just gonna start with some scoring
				if not re.search('[1-9]+', stats['minutes']):
					# skip players who haven't played
					continue
				# print(name, player_id)
				fouls = stats['foulsPersonal']
				ft_attempts = stats['freeThrowsAttempted']
				ft_makes = stats['freeThrowsMade']
				three_attempts = stats['threePointersAttempted']
				three_makes = stats['threePointersMade']
				two_attempts = stats['twoPointersAttempted']
				two_makes = stats['twoPointersMade']
				base_rates = get_base_rates(player_id)
				try:
					ft_avg = float(base_rates.ft_pct)
					two_avg = float(base_rates.fg2_pct)
					three_avg = float(base_rates.fg3_pct)
				except Exception as e:
					cprint(f"Couldnt get base rates for {name}: {e}", 'yellow')
					ft_avg = float(input(f"what do you want to say {name}'s ft_avg is? "))/100
					two_avg = float(input(f"what do you want to say {name}'s two_avg is? "))/100
					three_avg = float(input(f"what do you want to say {name}'s three_avg is? "))/100
				player_points_actual = stats['points']
				# player_points_ev = round(1*ft_attempts*ft_avg + 2*two_attempts*two_avg + 3*three_attempts*three_avg, 2)
				player_points_ev = round(1*ft_attempts*ft_avg + 2*two_makes + 3*three_attempts*three_avg, 2) # excluding 2p ev
				player_differential = round(player_points_ev - player_points_actual, 2)
				if print_players:
					cprint(f"{name}: Actual = {player_points_actual}, EV = {player_points_ev}, {abs(player_differential)} points {'above' if player_differential <= 0 else 'below'} ev", 'green' if player_differential < 0 else 'red' if player_differential > 0 else 'white')
				team_score_ev += player_points_ev
				ev_3 += 3*three_attempts*three_avg
				actual_3 += 3*three_makes
			except Exception as e:
				input(e)

		score_ev.append(round(team_score_ev, 1))
		# cprint(f"THREE EV: {round(ev_3, 2)} THREE ACTUAL: {round(actual_3, 2)}", 'white')

	return score_ev