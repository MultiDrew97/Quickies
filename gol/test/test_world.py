from random import randint
from pytest import raises

from gol import Status
from gol.test import *
from gol.world import World

def test_world_creation():
	with raises(Exception):
		World(0, 1) # No x direction
		World(-1,1) # No 'negative' yet, may add later
		World(1, 0) # No y direction
		World(1,-1) # No 'negative' yet, may add later

	for _ in range(randint(min_iterations, max_iterations)):
		World(gen_x_limit(), gen_y_limit())

def test_entity_retrieval():
	x_limit, y_limit = gen_x_limit(), gen_y_limit()
	world = World(x_limit, y_limit)

	with raises(Exception):
		world.get_entity(x_limit + 1, randint(0, y_limit)) # Bad row
		world.get_entity(-1, randint(0, y_limit)) # Bad row
		world.get_entity(randint(0, x_limit), -1) # Bad col
		world.get_entity(randint(0, x_limit), y_limit + 1) # Bad col

	print(f"World Bounds: {x_limit}x{y_limit}")
	for _ in range(randint(min_iterations, max_iterations)):
		x, y = randint(0, x_limit - 1), randint(0, y_limit - 1)
		print(f"Retrieving Entity: ({x}, {y})...")
		assert world.get_entity(x, y) != None

def test_world_wipe():
	x_limit, y_limit = gen_x_limit(), gen_y_limit()
	world = World(x_limit, y_limit)

	for x in range(x_limit):
		for y in range(y_limit):
			print(f"Retrieving Entity: ({x}, {y})...")
			world.get_entity(x, y).kill()
			assert not world.get_entity(x, y).is_alive()

	world.flush()

	for x in range(x_limit):
		for y in range(y_limit):
			print(f"Retrieving Entity: ({x}, {y})...")
			assert world.get_entity(x, y).is_alive()