from random import randint

min_board_rows=3
max_board_rows=1000
min_board_cols=3
max_board_cols=1000

def gen_row():
	return randint(min_board_cols, max_board_cols)
def gen_col():
	return randint(min_board_cols, max_board_cols)