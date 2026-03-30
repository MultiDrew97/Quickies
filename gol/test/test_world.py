from pytest import raises

from random import randint
from gol.entity import Entity

from gol import Point
from gol.test import gen_x_limit, gen_y_limit, min_iterations, max_iterations
from gol.world import World

def test_world_creation():
	with raises(Exception):
		World(Point(0, 1)) # No x direction
		World(Point(-1,1)) # No 'negative' yet, may add later
		World(Point(1, 0)) # No y direction
		World(Point(1,-1)) # No 'negative' yet, may add later

	for _ in range(randint(min_iterations, max_iterations)):
		World(Point(gen_x_limit(), gen_y_limit()))

def test_entity_retrieval():
	x_limit, y_limit = gen_x_limit(), gen_y_limit()
	world = World(Point(x_limit, y_limit))

	with raises(Exception):
		world.get_entity(Point(x_limit + 1, randint(0, y_limit))) # Bad row
		world.get_entity(Point(-1, randint(0, y_limit))) # Bad row
		world.get_entity(Point(randint(0, x_limit), -1)) # Bad col
		world.get_entity(Point(randint(0, x_limit), y_limit + 1)) # Bad col

	print(f"World Bounds: {x_limit}x{y_limit}")
	for _ in range(randint(min_iterations, max_iterations)):
		x, y = randint(0, x_limit - 1), randint(0, y_limit - 1)
		print(f"Retrieving Entity: ({x}, {y})...")
		assert world.get_entity(Point(x, y)) is None

def test_world_wipe():
	x_limit, y_limit = gen_x_limit(), gen_y_limit()
	world = World(Point(x_limit, y_limit))
	world.add_entity(Entity(position=Point(0, 0)))

	entity = world.get_entity(Point(0, 0))
	assert entity is not None
	assert entity.is_alive()

	world.flush()

	entity = world.get_entity(Point(0, 0))
	assert entity is None