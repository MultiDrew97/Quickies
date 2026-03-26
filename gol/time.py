from typing import Generator

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
	__paused__ = True
	__running__ = False

	def __init__(self):
		print("[INFO] Defining the laws of the universe 🙇🏾‍♂️...")
		self.__clock__ = pyg.time.Clock()
		self.__setup__()
		print("[INFO] Your universe is ready. Don't go mad or something 👀")

	def __setup__(self):
		""" Perform any setup necessary before the game starts """
		pyg.display.set_caption("GOL: Game of Life")

	def __cleanup__(self):
		""" Perform cleanup after the game is stopped """
		print("[INFO] The singularity has spawned 🕳️...")
		pyg.quit()
		print("[INFO] The singularity has swallowed everything. Thanks for playing GOL!")

	def __draw_space__(self):
		""" Draw the world and all of its entities onto the canvas """
		# if self.__paused__: return
		self.__world__.draw(self.__display__) if self.__world__ else None

	def __add_entity__(self, entity: Entity):
		""" Add a new entity to the world at the provided location if possible """
		# if self.__paused__: return
		try:
			self.__world__.add_entity(entity) if self.__world__ else None
		except Exception as ex:
			print(f"[ERROR] Unable to place entity at {entity.position}: {ex}")

	def __handle_events__(self):
		""" Handle any events that have arisen since the last tick of the game """
		for e in pyg.event.get():
			if e.type == pyg.QUIT or (e.type == pyg.KEYDOWN and e.key == pyg.K_q):
				self.__running__ = False # Stop the game
			elif e.type == pyg.WINDOWHIDDEN or (e.type == pyg.KEYDOWN and e.key == pyg.K_p):
				# Pause and unpause the game
				self.__pause_game__() if not self.__paused__ else self.__unpause_game__()
			elif e.type == pyg.KEYDOWN and e.key == pyg.K_n:
				if not self.__world__:
					# Start a fresh world if one doen't already exist
					self.__world__ = World(universe_dimensions)
				else:
					# Wipe the world to start fresh if it already exists
					self.__world__.flush()
			elif e.type == pyg.MOUSEBUTTONDOWN:
				if not self.__world__:
					continue # Don't place an entity if the world isn't initialized

				mouse_pos_x, mouse_pos_y = pyg.mouse.get_pos()
				pos = Point(mouse_pos_x // block_size, mouse_pos_y // block_size)
				if self.__world__.get_entity(pos) is not None:
					print(f"[INFO] Removing entity at {pos}...")
					self.__world__.remove_entity(pos) # Remove the entity if one already exists at that location
				else:
					print(f"[INFO] Placing a new entity at {pos}...")
					self.__add_entity__(Entity(position=pos))

	def __entropy__(self):
		""" Change the state of the world and its entities according to the rules of the game """
		if self.__paused__: return # Don't change the state of the world while paused
		if not self.__world__: return # Don't do anything if the world isn't initialized

		self.__world__.step() # Step the world forward according to the rules of the game


	def __wipe_display__(self):
		""" Wipe the display to be redrawn on the next render """
		self.__display__.fill(self.__bg_color__)

	def __draw_cursor__(self):
		""" Draw the cursor on top of the game space to indicate where the next entity will be placed """
		mouse_pos = pyg.mouse.get_pos()

		if mouse_pos[0] < 0 or mouse_pos[0] > universe_dimensions.x or mouse_pos[1] < 0 or mouse_pos[1] > universe_dimensions.y:
			return # Don't draw the cursor if it's out of bounds
		pyg.draw.circle(self.__display__, color=pyg.Color(255, 0, 0), center=mouse_pos, radius=block_size // 2)

	def __render__(self):
		""" Render the game to the player """
		# if self.__paused__: return # Don't render while paused
		self.__wipe_display__() # Wipe the display to be redrawn
		self.__entropy__() # Change the state of the world according to the rules of the game
		self.__draw_space__() # Draw the game space
		self.__draw_cursor__() # Draw the cursor on top of the game space
		pyg.display.update() # Update the display

	def __pause_game__(self):
		""" Pause the game to freeze the state of the game and allow the player to inspect it without any changes occurring """
		print("[INFO] Freezing the state of the universe ❄️...")
		self.__paused__ = True

	def __unpause_game__(self):
		""" Unpause the game to allow the state of the game to change again and continue playing """
		print("[INFO] Thawing out the universe 🔥...")
		self.__paused__ = False

	def start(self):
		""" Start the game loop to begin playing the game """
		self.__running__ = True
		self.__display__ = pyg.display.set_mode(universe_dimensions)

		try:
			while self.__running__:
				self.__handle_events__() # Parse any events that arose
				self.__render__() # Render the game
				self.__clock__.tick(tick_rate) # Tick the clock
		finally:
			self.__cleanup__() # Cleanup anything after the game is stopped
