import pygame as pyg
from gol import Point, VisualComponent
from gol.entity import Entity

class World(VisualComponent):
	""" The definitions of the space that the entities live in """
	__entities__: list[Entity] = []

	# TODO: Expand for 3D
	def __init__(self, bounds: Point) -> None:
		if bounds.x < 1:
			raise Exception("Invalid x limit")
		if bounds.y < 1:
			raise Exception("Invalid y limit")
		print("Loading your earthly realm...")

		self.__color__ = pyg.Color(0, 0, 0) # Set space color to black
		self.__x_limit__, self.__y_limit__ = bounds
		self.flush()
		print("[DEBUG] Current Space:")
		print(self.__entities__)
		print("Your oyster is ready")

	def flush(self):
		""" Clear the space to a clean slate """
		print("Sending the flood...")
		self.__entities__.clear()
		# self.__entities = [[Entity() for _ in range(self.__x_limit__)] for _ in range(self.__y_limit__)]
		# print(self.__entities)
		print("You have wiped out the population")

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
		if next((e for e in self.__entities__ if e.position == entity.position), None) != None:
			raise Exception(f"Entity already present at location {entity.position}")

		self.__entities__.append(entity)

		return self.__entities__.index(entity) if entity in self.__entities__ else -1


