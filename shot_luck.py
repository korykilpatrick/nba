from collections import defaultdict
import re
from termcolor import cprint

from nba import dal
def get_base_rates(player_id):
	return dal.callproc('get_base_rates', args=(player_id,), one_or_none=True)

def calculate_shot_luck_score(box_dict, home_team, print_players=True):
	"""
	Given a boxscore, calculate our shot-luck adjusted score.
	In here is where we will tinker.
	"""
	home_score_ev = away_score_ev = 0
	for team in box_dict:
		ev_3, actual_3 = 0, 0
		if print_players: cprint(f"\n{team}", 'white', attrs=['bold'])
		for name, player_data in box_dict[team]['players'].items():
			try:
				if not re.search('[1-9]+', player_data['min']):
					# skip players who haven't played
					continue
				# print(name, player_id)
				base_rates = get_base_rates(player_data['id'])
				try:
					ft_avg = float(base_rates.ft_pct)
					two_avg = float(base_rates.fg2_pct)
					three_avg = float(base_rates.fg3_pct)
					if team == home_team: three_avg += .01
					else: three_avg -= .01
				except Exception as e:
					# continue
					cprint(f"Couldnt get base rates for {name}: {e}", 'yellow')
					# if input('do you want to skip this bro? (y/n)').lower() == 'y':
						# continue
					ft_avg = float(input(f"what do you want to say {name}'s ft_avg is? "))/100
					two_avg = float(input(f"what do you want to say {name}'s two_avg is? "))/100
					three_avg = float(input(f"what do you want to say {name}'s three_avg is? "))/100
				player_points_actual = player_data['pts']
				# player_points_ev = round(1*player_data['fta']*ft_avg + 2*player_data['2pa']*two_avg + 3*player_data['fg3a']*three_avg, 2)
				player_points_ev = round(1*player_data['fta']*ft_avg + 2*player_data['fg2m'] + 3*player_data['fg3a']*three_avg, 2) # excluding 2p ev
				player_differential = round(player_points_ev - player_points_actual, 2)
				if print_players:
					cprint(f"{name}: Actual = {player_points_actual}, EV = {player_points_ev}, {abs(player_differential)} points {'above' if player_differential <= 0 else 'below'} ev", 'green' if player_differential < 0 else 'red' if player_differential > 0 else 'white')
				if team == home_team: home_score_ev += player_points_ev
				else: away_score_ev += player_points_ev
				# team_score_ev += player_points_ev
				ev_3 += 3*player_data['fg3a']*three_avg
				actual_3 += 3*player_data['fg3m']
			except Exception as e:
				cprint(player_data, 'red')
				input(e)

		# cprint(f"THREE EV: {round(ev_3, 2)} THREE ACTUAL: {round(actual_3, 2)}", 'white')

	return round(home_score_ev, 1), round(away_score_ev, 1)