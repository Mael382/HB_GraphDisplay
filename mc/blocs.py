from typing import Optional


CONCRETE: set[(str, Optional[str])] = {
	('white_concrete', '#CFD5D6'),
	('orange_concrete', '#E06101'),
	('magenta_concrete', '#A9309F'),
	('light_blue_concrete', '#2489C7'),
	('yellow_concrete', '#F1AF15'),
	('lime_concrete', '#5EA918'),
	('pink_concrete', '#D5658F'),
	('gray_concrete', '#373A3E'),
	('light_gray_concrete', '#7D7D73'),
	('cyan_concrete', '#157788'),
	('purple_concrete', '#64209C'),
	('blue_concrete', '#2D2F8F'),
	('brown_concrete', '#603C20'),
	('green_concrete', '#495B24'),
	('red_concrete', '#8E2121'),
	('black_concrete', '#080A0F')
}

BLOCS = frozenset(CONCRETE)
