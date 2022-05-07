# https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/cumestatsplayer.md
import re

from nba_api.stats.endpoints import cumestatsplayer
# from nba.db.models import CumeStatsPlayer
from nba import dal

def seed_cume_stats_player():
	stats = cumestatsplayer.CumeStatsPlayer(player_id='203099')
	for res in stats.get_dict():
		input(res)
if __name__ == '__main__':
	seed_cume_stats_player()
