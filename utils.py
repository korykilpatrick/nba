from termcolor import cprint

def insert_records(dal, tablename, records, ret=False, ignore=False, print_res=True, color='green'):
	if not records:
		cprint(f"No {tablename} records passed to insert_records", 'yellow')
		return

	insert_val = ', '.join(records[0]._fields)
	values_formatter = ', '.join(["%s" for _ in range(len(records[0]._fields))])
	sql = f"INSERT{' IGNORE' if ignore else ''} INTO {tablename} ({insert_val}) VALUES ({values_formatter})"

	dal.execute(sql, records, many=True, insert=True)
	if print_res:
		cprint(f"Inserted {len(records)} records into {tablename}.", color)

	if ret:
		return dal.execute(f'select * from {tablename} order by id desc limit {len(records)}')

def clean_shooting_figs(fgm, fga, fg2m, fg2a, fg3m, fg3a, ftm, fta):
	fgm = fgm or 0
	fga = fga or 0
	fg_pct = round(fgm / fga, 2) if fga else 0
	fg3m = fg3m or 0
	fg3a = fg3a or 0
	fg3_pct = round(fg3m / fg3a, 2) if fg3a else 0
	fg2m = fgm - fg3m
	fg2a = fga - fg3a
	fg2_pct = round(fg2m / fg2a, 2) if fg2a else 0
	ftm = ftm or 0
	fta = fta or 0
	ft_pct = round(ftm / fta, 2) if fta else 0

	return fgm, fga, fg_pct, fg2m, fg2a, fg2_pct, fg3m, fg3a, fg3_pct, ftm, fta, ft_pct