from nba_api.stats.endpoints import shotchartdetail
from termcolor import cprint
import traceback
import sys

import nba.db.models as models
import nba.utils as utils
from nba import dal
import nickelbot.client.cli.cli_utils as cli_utils

team_lookup = {team.abbreviation: team.team_id for team in dal.execute('select * from teams')}
team_lookup['NOH'] = team_lookup['NOP'] # Dumb shit for NO Hornets vs Pelicans
team_lookup['NOK'] = team_lookup['NOP']
team_lookup['NJN'] = team_lookup['BKN']
team_lookup['SEA'] = team_lookup['OKC']

tn_choices = sorted([k for k in team_lookup]) + ['Skip']
tn_edits = {}

def get_shotchart(player):
	# embiid = dal.execute('select * from players where last_name=%s', args=('Embiid',), one_or_none=True)
	# return shotchartdetail.ShotChartDetail(
	# 		team_id = 0,
	# 		player_id = embiid.player_id,
	# 		context_measure_simple = 'FGA',
	# 		season_type_all_star = ['Regular Season', 'Playoffs']
	# 	)
	return utils.get_data(
			shotchartdetail.ShotChartDetail,
			team_id = 0,
			player_id = player.player_id,
			context_measure_simple = 'FGA',
			season_type_all_star = ['Regular Season', 'Playoffs']
		)

def save_player_attempts(player, data):
	attempts = []
	for row in data:
		try:
			htm_id = team_lookup.get(row.htm)
			vtm_id = team_lookup.get(row.vtm)
		except:
			print(row._fields)
			sys.exit()

		if htm_id is None:
			if row.htm in tn_edits:
				htm_id = team_lookup[tn_edits[row.htm]]
			else:
				choice = cli_utils.choose_from(tn_choices, f'Select the correct name for old team {row.htm}')
				if choice == 'Skip':
					continue
				tn_edits[row.htm] = choice
				htm_id = team_lookup[choice]
		if vtm_id is None:
			if row.vtm in tn_edits:
				vtm_id = team_lookup[tn_edits[row.vtm]]
			else:
				choice = cli_utils.choose_from(tn_choices, f'Select the correct name for old team {row.vtm}')
				if choice == 'Skip':
					continue
				tn_edits[row.vtm] = choice
				vtm_id = team_lookup[choice]

		attempts.append(
				models.ShotAttempt(
						row.game_id,
						row.game_event_id,
						row.player_id,
						row.team_id,
						row.period,
						row.minutes_remaining,
						row.seconds_remaining,
						row.event_type,
						row.action_type,
						row.shot_type,
						row.shot_zone_basic,
						row.shot_zone_area,
						row.shot_zone_range,
						row.shot_distance,
						row.loc_x,
						row.loc_y,
						row.shot_attempted_flag,
						row.shot_made_flag,
						f"{row.game_date[:4]}-{row.game_date[4:6]}-{row.game_date[6:]}",
						htm_id,
						vtm_id
					)
			)

	try:
		utils.insert_records(dal, 'shot_attempts', attempts, print_res=False)
		cprint(f"{player.full_name} - {len(attempts)}", 'green')
	except:
		traceback.print_exc()
		try:
			if cli_utils.you_want_to('insert ignore these shot attempts'):
				utils.insert_records(dal, 'shot_attempts', attempts, print_res=False, ignore=True)
		except KeyboardInterrupt:
			sys.exit()

if __name__ == '__main__':
	players = dal.execute('select * from players where is_active')
	for player in players:
		data = get_shotchart(player)
		save_player_attempts(player, data[0])
