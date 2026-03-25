from gol.entity import Entity

def test_birth():
	assert Entity()

def test_kill():
	entity = Entity()

	assert entity.is_alive()
	assert entity.kill()

def test_ressurect():
	entity = Entity()

	if entity.is_alive():
		entity.kill()
		
	assert entity.ressurect()
