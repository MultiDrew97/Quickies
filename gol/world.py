from typing import Generator

import pygame as pyg
from gol import Point, VisualComponent
from gol.entity import Entity
from gol.engine import block_size

class World(VisualComponent):
	""" The definitions of the space that the entities live in """
	__entities__: list[Entity] = []

	# TODO: Expand for 3D
	def __init__(self, bounds: Point) -> None:
		if bounds.x < 1:
			raise Exception("Invalid x limit")
		if bounds.y < 1:
			raise Exception("Invalid y limit")
		print("[INFO] Loading your earthly realm...")

		self.__color__ = pyg.Color(0, 0, 0) # Set space color to black
		self.__x_limit__, self.__y_limit__ = bounds
		self.flush()
		print("[INFO] Your oyster is ready")

	def __get_neighbors__(self, position) -> int:
		return len([e for e in self.__entities__ if e.position in [Point(position.x - 1, position.y - 1), Point(position.x, position.y - 1), Point(position.x + 1, position.y - 1), Point(position.x - 1, position.y), Point(position.x + 1, position.y), Point(position.x - 1, position.y + 1), Point(position.x, position.y + 1), Point(position.x + 1, position.y + 1)]])

		# An entity survives if it has 2 or 3 neighbors, otherwise it dies
		# return len(neighbors)

	def flush(self):
		""" Clear the space to a clean slate """
		print("[INFO] Sending the flood 🌊...")
		self.__entities__.clear()
		# self.__entities = [[Entity() for _ in range(self.__x_limit__)] for _ in range(self.__y_limit__)]
		# print(self.__entities)
		print("[INFO] You have wiped out the population")

	def draw(self, display: pyg.Surface):
		""" Draw the world onto the canvas """
		display.fill(self.__color__) # Fill in the space background

		for entity in self.__entities__:
			entity.draw(display) # Let each entity draw itself with its own logic

	def get_entity(self, position: Point) -> Entity | None:
		""" Attempt to retrieve an entity that is at the provided location """
		if position.x < 0 or position.x > self.__x_limit__:
			raise Exception("x is invalid")

		if position.y < 0 or position.y > self.__y_limit__:
			raise Exception("y is invalid")

		return next((e for e in self.__entities__ if e.position == position), None)

	def add_entity(self, entity: Entity) -> int:
		""" Add an entity to the space if one does not already occupy that space """

		print(f"[INFO] Placing a new entity at {entity.position}")
		if next((e for e in self.__entities__ if e.position == entity.position), None) is not None:
			raise Exception(f"Entity already present at location {entity.position}")

		self.__entities__.append(entity)

		return self.__entities__.index(entity) if entity in self.__entities__ else -1

	def step(self):
		if len(self.__entities__) <= 0: return # Don't do anything if there are no entities in the world

		 # An entity survives if it has 2 or 3 neighbors, otherwise it dies
		self.__entities__ = [(e for e in self.__entities__.copy() if e.is_alive() and self.__get_neighbors__(e.position) in [2, 3])]


		def will_birth() -> Generator[Entity, None, None]:
			if not self.__entities__: return # Don't do anything if the world isn't initialized
			# births: list[Entity] = []

			yield from [Entity(position=Point(x, y)) for x in range(self.__x_limit__ // block_size) for y in range(self.__y_limit__ // block_size) if next((e for e in self.__entities__ if e.position == Point(x, y)), None) is None and self.__get_neighbors__(Point(x, y)) == 2] # Birth a new entity at the current location if there isn't already one there and the rule is met

			# for x in range(universe_dimensions.x // block_size):
			# 	for y in range(universe_dimensions.y // block_size):
			# 		print(f"[DEBUG] Checking for births at position: {Point(x, y)}")
			# 		if next((e for e in prev_state if e.position == Point(x, y)), None) is not None or get_neighbors(Point(x, y)) != 2:
			# 			continue # Don't birth an entity if one already exists at that location or i fthe rule is not met

			# 		# Send the new entity back to the world if it was birthed successfully
			# 		print(f"[DEBUG] Entity being added at {Point(x, y)}, skipping birth check")
			# 		yield Entity(position=Point(x // block_size, y // block_size))


