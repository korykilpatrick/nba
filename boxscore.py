from nba_api.live.nba.endpoints import boxscore
from termcolor import cprint

headers = {'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'en-US,en;q=0.9',
'Connection': 'keep-alive',
'Host': 'stats.nba.com',
'Origin': 'https://www.nba.com',
'Referer': 'https://www.nba.com/',
'sec-ch-ua': '"Google Chrome";v="87", "\"Not;A\\Brand";v="99", "Chromium";v="87"',
'sec-ch-ua-mobile': '?1',
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-site',
'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36',
'x-nba-stats-origin': 'stats',
'x-nba-stats-token': 'true'}

def get_live_boxscore(game_id):
	# https://github.com/swar/nba_api/blob/master/docs/examples/LiveData.ipynb
	box = boxscore.BoxScore(game_id)
	box = boxscore.BoxScore(str(game_id)).game.get_dict()
	return box

def get_past_boxscore(game_id):
	from nba_api.stats.endpoints import boxscoretraditionalv2
	from nba_api.stats.endpoints import boxscoreadvancedv2
	box = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id, headers=headers)

	# boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id, headers=headers).get_json()
	# box = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id, headers=headers)
	# print(box)

if __name__ == '__main__':
	game_id = 1 # ?
	# get_live_boxscore('42100202')
	get_past_boxscore('42100231')