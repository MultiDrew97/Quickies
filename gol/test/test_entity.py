from gol.entity import Entity

def test_birth():
	assert Entity()

def test_kill():
	entity = Entity()

	assert entity.is_alive()
	entity.kill()
	assert not entity.is_alive()
