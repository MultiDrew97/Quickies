from gol.engine import Universe, universe_dimensions
from gol.world import World

def test_big_bang() -> None:
	universe = Universe()

	try:
		assert universe.__world__ is None
		assert universe.__paused__ == False
		assert universe.__bg_color__ == (255,255,255)
		assert universe.__display__.get_size() == (universe_dimensions.x, universe_dimensions.y)
		assert universe.__clock__ is not None
	finally:
		universe.__cleanup__()

def test_space_render() -> None:
	universe = Universe()

	try:
		assert universe.__world__ is None
		universe.__draw_space__() # Shouldn't render anything since the world is not initialized
	finally:
		universe.__cleanup__()

	try:
		universe.__world__ = World(universe_dimensions) # Initialize the world
	finally:
		universe.__cleanup__()
