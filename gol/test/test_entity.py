from gol import Point
from gol.entity import Entity

def test_birth():
	assert Entity()
	assert Entity(name="Testing Entity")
	assert Entity(position=Point(0, 0))
	assert Entity(name="Testing Entity 2", position=Point(1,1))

def test_kill():
	entity = Entity()

	assert entity.is_alive()
	assert entity.kill()

def test_ressurect():
	entity = Entity()

	if entity.is_alive():
		entity.kill()

	assert entity.revive()
