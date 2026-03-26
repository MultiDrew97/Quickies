from gol.test import min_iterations
from gol.universe import Universe

def test_start_universe():
	multiverse = [Universe() for _ in range(min_iterations)]
	assert len(multiverse) == min_iterations

def test_tick():
	reality = Universe()
	start_age = reality.age
	reality.tick()

	assert not reality.__space__.get_entity(1, 1).is_alive()
	assert reality.age == start_age + 1