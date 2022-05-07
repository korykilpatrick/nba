from nba_api.stats.static import players

from nba import dal
from nba.db.models import Player
from nba.utils import insert_records

def seed_players(state='active'):
	records= []
	player_res = players.get_active_players() if state == 'active' else \
						players.get_inactive_players() if state == 'inactive' else \
						players.get_players()
	for player in player_res:
		records.append(Player(player['id'], player['full_name'], player['first_name'], player['last_name'], player['is_active']))

	insert_records(dal, 'players', records, ignore=False)

if __name__ == '__main__':
	seed_players(state='inactive')
