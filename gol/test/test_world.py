from random import randint
from pytest import raises

from gol.test import *
from gol.world import World

def test_board_creation():
	with raises(Exception):
		World(0, 1) # No rows
		World(-1,1) # Negative rows
		World(1, 0) # No columns
		World(1,-1) # Negative columns

	World(gen_row(), gen_col())

def test_board_toggle():
	rows = gen_row()
	cols = gen_col()
	board = World(rows, cols)

	with raises(Exception):
		board.toggle_space(rows + 1, randint(0, cols)) # Bad row
		board.toggle_space(-1, randint(0, cols)) # Bad row
		board.toggle_space(randint(0, rows), -1) # Bad col
		board.toggle_space(randint(0, rows), cols + 1) # Bad col

	row = randint(0, rows)
	col = randint(0, cols)
	assert board.is_alive(row, col) == False
	board.toggle_space(row, col)
	assert board.is_alive(row, col) == True

def test_board_clear():
	rows, cols = gen_row(), gen_col()
	world = World(rows, cols)

	for r in range(rows):
		for c in range(cols):
			world.toggle_space(r, c)
			assert world.is_alive(r, c) == True

	world.flush()

	for r in range(rows):
		for c in range(cols):
			assert world.is_alive(r, c) == False