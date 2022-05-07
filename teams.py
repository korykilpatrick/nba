from nba_api.stats.static import teams

from nba import dal
from nba.db.models import Team
from nba.utils import insert_records

def seed_teams():
	records = []
	for team in teams.get_teams():
		records.append(Team(team['id'], team['full_name'], team['abbreviation'], team['nickname'], team['city'], team['state'], team['year_founded'], None))
	insert_records(dal, 'teams', records, ignore=False)

if __name__ == '__main__':
	seed_teams()

