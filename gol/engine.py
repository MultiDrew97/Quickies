import pygame as pyg

from gol import Point, block_size
from gol.entity import Entity
from gol.world import World

tick_rate = 60
universe_dimensions: Point = Point(x=600, y=600)

class Universe:
	__bg_color__ = pyg.Color(255,255,255)
	__display__: pyg.Surface
	__clock__: pyg.time.Clock
	__world__: World | None = None
	__paused__ = False
	__running__ = False

	def __init__(self):
		print("[INFO] Defining the laws of the universe 🙇🏾‍♂️...")
		self.__clock__ = pyg.time.Clock()
		self.__setup__()
		print("[INFO] Your universe is ready. Don't go mad or something 👀")

	def __setup__(self):
		pyg.display.set_caption("GOL: Game of Life")
		self.__display__ = pyg.display.set_mode(universe_dimensions)

	def __cleanup__(self):
		print("[INFO] The singularity has spawned 🕳️...")
		pyg.quit()
		print("[INFO] The singularity has swallowed everything. Thanks for playing GOL!")

	def __draw_space__(self):
		if self.__paused__: return
		self.__world__.draw(self.__display__) if self.__world__ else None

	def __add_entity__(self, entity: Entity):
		if self.__paused__: return
		try:
			self.__world__.add_entity(entity) if self.__world__ else None
		except Exception as ex:
			print(f"[ERROR] Unable to place entity at {entity.position}: {ex}")

	def __handle_events__(self):
		for e in pyg.event.get():
			print(f"[DEBUG] Event: {e}")
			if e.type == pyg.QUIT or (e.type == pyg.KEYDOWN and e.key == pyg.K_q):
				self.__running__ = False # Stop the game
			elif e.type == pyg.WINDOWHIDDEN or (e.type == pyg.KEYDOWN and e.key == pyg.K_p):
				self.__pause_game__() if not self.__paused__ else self.__unpause_game__() # Pause and unpause the game
			elif e.type == pyg.KEYDOWN and e.key == pyg.K_n:
				if self.__paused__: continue
				if not self.__world__:
					self.__world__ = World(universe_dimensions) # Start a fresh world if one doen't already exist
				else:
					self.__world__.flush() # Wipe the world to start fresh if it already exists
			elif e.type == pyg.MOUSEBUTTONDOWN:
				mouse_pos = pyg.mouse.get_pos()
				self.__add_entity__(Entity(position=Point(mouse_pos[0] // block_size, mouse_pos[1] // block_size)))


	def __wipe_display__(self):
		if self.__paused__: return # Don't wipe the display while paused

		self.__display__.fill(self.__bg_color__)

	def __draw_cursor__(self):
		if self.__paused__: return # Don't update mouse while paused

		mouse_pos = pyg.mouse.get_pos()

		if mouse_pos[0] < 0 or mouse_pos[0] > universe_dimensions.x or mouse_pos[1] < 0 or mouse_pos[1] > universe_dimensions.y:
			return # Don't draw the cursor if it's out of bounds
		pyg.draw.circle(self.__display__, color=pyg.Color(255, 0, 0), center=mouse_pos, radius=block_size // 2)

	def __render__(self):
		""" Render the game to the player """
		if self.__paused__: return # Don't render while paused
		self.__wipe_display__() # Wipe the display to be redrawn
		self.__draw_space__() # Draw the game space
		self.__draw_cursor__() # Draw the cursor on top of the game space
		pyg.display.update() # Update the display

	def __pause_game__(self):
		print("[INFO] Freezing the state of the universe ❄️...")
		self.__paused__ = True

	def __unpause_game__(self):
		print("[INFO] Thawing out the universe 🔥...")
		self.__paused__ = False

	def start(self):
		self.__running__ = True

		try:
			while self.__running__:
				self.__handle_events__() # Parse any events that arose
				self.__render__() # Render the game
				self.__clock__.tick(tick_rate) # Tick the clock
		finally:
			self.__cleanup__() # Cleanup anything after the game is stopped
