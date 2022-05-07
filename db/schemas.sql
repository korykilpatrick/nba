drop table if exists teams;
create table teams (
	team_id int unsigned auto_increment primary key,
  full_name varchar(100) not null,
  abbreviation varchar(3) not null,
  nickname varchar(50) not null,
  city varchar(50) not null,
  state varchar(50) not null,
  year_founded int,
  alias varchar(10)
);

drop table if exists players;
create table players (
  player_id int unsigned auto_increment primary key,
    full_name varchar(100) not null,
    first_name varchar(50) not null,
    last_name varchar(50) not null,
    is_active bool default 1,
    create_date datetime default now()
);

drop table if exists player_stats;
create table player_stats (
  player_id int unsigned not null,
    season_id varchar(10),
    is_postseason bool default 0,
    team_id int unsigned,
    team_abbreviation varchar(4),
    player_age int unsigned,
    gp int unsigned,
    gs int unsigned,
    min int unsigned,
    fgm int unsigned,
    fga int unsigned,
    fg_pct decimal(5, 2),
    fg3m int unsigned,
    fg3a int unsigned,
    fg3_pct decimal(5,2),
    ftm int unsigned,
    fta int unsigned default 0,
    ft_pct decimal(5,2),
    oreb int unsigned,
    dreb int unsigned,
    reb int unsigned,
    ast int unsigned,
    stl int unsigned,
    blk int unsigned,
    tov int unsigned,
    pf int unsigned,
    pts int unsigned,
    create_date datetime default now(),
    foreign key pl_id(player_id) references players(player_id)
);

drop table if exists player_adjustments;
create table player_adjustments (
  id int unsigned auto_increment primary key,
    player_id int unsigned not null,
    stat varchar(10) not null,
    operation enum('add', 'replace') not null,
    val decimal(5,2) not null,
    foreign key p_id(player_id) references players(player_id),
    unique(player_id, stat, operation)
);


drop table if exists games;
create table games (
  season_id varchar(30),
  game_id varchar(30) primary key,
    game_date datetime not null,
    home_team varchar(3) not null,
    away_team varchar(3) not null,
    home_score int unsigned,
    away_score int unsigned,
    create_date datetime default now()
);

create table shot_luck_snapshot (
  id int unsigned auto_increment primary key,
    create_date datetime default now(),
    game_id int unsigned not null,
    home_score decimal(5,2) not null,
    away_score decimal(5,2) not null
);
