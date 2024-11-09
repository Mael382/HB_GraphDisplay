WOOL: set[tuple[str, str]] = {
	('black_wool', '#141519'),
	('blue_wool', '#35399D'),
	('brown_wool', '#724728'),
	('cyan_wool', '#158991'),
	('gray_wool', '#3E4447'),
	('green_wool', '#546D1B'),
	('light_blue_wool', '#3AAFD9'),
	('light_gray_wool', '#8E8E86'),
	('lime_wool', '#70B919'),
	('magenta_wool', '#BD44B3'),
	('orange_wool', '#F07613'),
	('pink_wool', '#ED8DAC'),
	('purple_wool', '#792AAC'),
	('red_wool', '#A02722'),
	('white_wool', '#E9ECEC'),
	('yellow_wool', '#F8C527')
}

CONCRETE_POWDER: set[tuple[str, str]] = {
	('black_concrete_powder', '#191A1F'),
	('blue_concrete_powder', '#4649A6'),
	('brown_concrete_powder', '#7D5435'),
	('cyan_concrete_powder', '#24939D'),
	('gray_concrete_powder', '#4C5154'),
	('green_concrete_powder', '#61772C'),
	('light_blue_concrete_powder', '#4AB4D5'),
	('light_gray_concrete_powder', '#9A9A94'),
	('lime_concrete_powder', '#7DBD29'),
	('magenta_concrete_powder', '#BD44B3'),
	('orange_concrete_powder', '#E3831F'),
	('pink_concrete_powder', '#E499B5'),
	('purple_concrete_powder', '#8337B1'),
	('red_concrete_powder', '#A83632'),
	('white_concrete_powder', '#E1E3E3'),
	('yellow_concrete_powder', '#E8C736')
}

CONCRETE: set[tuple[str, str]] = {
	('black_concrete', '#080A0F'),
	('blue_concrete', '#2C2E8F'),
	('brown_concrete', '#603B1F'),
	('cyan_concrete', '#157788'),
	('gray_concrete', '#36393D'),
	('green_concrete', '#495B24'),
	('light_blue_concrete', '#2389C6'),
	('light_gray_concrete', '#7D7D73'),
	('lime_concrete', '#5EA818'),
	('magenta_concrete', '#A9309F'),
	('orange_concrete', '#E06100'),
	('pink_concrete', '#D5658E'),
	('purple_concrete', '#641F9C'),
	('red_concrete', '#8E2020'),
	('white_concrete', '#CFD5D6'),
	('yellow_concrete', '#F0AF15')
}

BLOCS = frozenset(WOOL | CONCRETE_POWDER | CONCRETE)
BLOCS_ID, BLOCS_COLOR = zip(*BLOCS)
BLOCS_ID, BLOCS_COLOR = frozenset(BLOCS_ID), frozenset(BLOCS_COLOR)
