from random import randint
from pytest import raises

from gol.test import *
from gol.board import Gameboard

def test_board_creation():
	with raises(Exception):
		Gameboard(0, 1) # No rows
		Gameboard(-1,1) # Negative rows
		Gameboard(1, 0) # No columns
		Gameboard(1,-1) # Negative columns

	Gameboard(getRow(), getCol())

def test_board_toggle():
	rows = getRow()
	cols = getCol()
	board = Gameboard(rows, cols)

	with raises(Exception):
		board.toggle_space(rows + 1, randint(0, cols)) # Bad row
		board.toggle_space(-1, randint(0, cols)) # Bad row
		board.toggle_space(randint(0, rows), -1) # Bad col
		board.toggle_space(randint(0, rows), cols + 1) # Bad col

	row = randint(0, rows)
	col = randint(0, cols)
	assert board.get_state(row, col) == False
	board.toggle_space(row, col)
	assert board.get_state(row, col) == True