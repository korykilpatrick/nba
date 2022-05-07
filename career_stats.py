# https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/endpoints/playercareerstats.md
import re, time

from nba_api.stats.endpoints import playercareerstats
from nba.db.models import PlayerStats
from nba import dal
from nba.utils import insert_records

def seed_player_career_stats():
	player_ids = [int(p.player_id) for p in dal.execute('select * from players where not is_active')]
	for p_id in player_ids:
		records = []
		if dal.execute('select * from player_stats where player_id=%s', (p_id,)):
			continue
		time.sleep(2)
		stats = playercareerstats.PlayerCareerStats(per_mode36='Totals', player_id=p_id)
		for res in stats.get_dict()['resultSets']:
			if not re.search('(Season|Career)Totals(Regular|Post)Season', res['name']):
				# Saving career/season regular/post records separately
				continue
			for r in res['rowSet']:
				is_postseason = bool(re.search('Post', res['name']))
				if re.search('Career', res['name']):
					# Career Stats
					fgm = r[6] or 0
					fg3m = r[9] or 0
					fga = r[7] or 0
					fg3a = r[10] or 0
					fg2m = fgm - fg3m
					fg2a = fga - fg3a
					fg2_pct = round(fg2m / fg2a, 2) if fg2a else 0
					records.append(PlayerStats(r[0], 'CAREER', is_postseason, None, None, None, r[3], r[4], r[5], r[6], r[7], r[8], fg2m, fg2a, fg2_pct, r[9], r[10], r[11], r[12], r[13], r[14], r[15], r[16], r[17], r[18], r[19], r[20], r[21], r[22], r[23]))
				else:
					# Season Stats
					fgm = r[9] or 0
					fga = r[10] or 0
					fg3m = r[12] or 0
					fg3a = r[13] or 0
					fg2m = fgm - fg3m
					fg2a = fga - fg3a
					fg2_pct = round(fg2m / fg2a, 2) if fg2a else 0
					records.append(PlayerStats(r[0], r[1], is_postseason, r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], fg2m, fg2a, fg2_pct, r[12], r[13], r[14], r[15], r[16], r[17], r[18], r[19], r[20], r[21], r[22], r[23], r[24], r[25], r[26]))
		insert_records(dal, 'player_stats', records, ignore=False)

if __name__ == '__main__':
	seed_player_career_stats()
