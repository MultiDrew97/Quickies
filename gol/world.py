import pygame as pyg
from gol import Point, VisualComponent
from gol.entity import Entity
from gol.universe import block_size

class World(VisualComponent):
	""" The definitions of the space that the entities live in """
	__entities__: list[Entity]

	# TODO: Expand for 3D
	def __init__(self, bounds: Point) -> None:
		if bounds.x < 1:
			raise Exception("Invalid x limit")
		if bounds.y < 1:
			raise Exception("Invalid y limit")
		print("[INFO] Loading your earthly realm...")

		self.__color__ = pyg.Color(0, 0, 0) # Set space color to black
		self.__x_limit__, self.__y_limit__ = bounds
		self.__entities__ = []
		print("[INFO] Your oyster is ready 🌎")

	def __get_neighbors__(self, position) -> int:
		""" Get the number of living neighbors around the provided position """
		neighbor_blocks = [
			Point(position.x - 1, position.y - 1), # NW
			Point(position.x, position.y - 1), # N
			Point(position.x + 1, position.y - 1), # NE
			Point(position.x - 1, position.y), # W
			Point(position.x + 1, position.y), # E
			Point(position.x - 1, position.y + 1), # SW
			Point(position.x, position.y + 1), # S
			Point(position.x + 1, position.y + 1) # SE
		]

		return len([e for e in self.__entities__ if e.position in neighbor_blocks and e.is_alive()])

	def flush(self):
		""" Clear the space to a clean slate """
		print("[INFO] Sending the flood 🌊...")
		self.__entities__.clear()
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

	def add_entity(self, entity: Entity) -> bool:
		""" Add an entity to the space if one does not already occupy that space """

		if next((e for e in self.__entities__ if e.position == entity.position), None) is not None:
			raise Exception(f"Entity already present at location {entity.position}")

		self.__entities__.append(entity)

		return entity in self.__entities__

	def remove_entity(self, position: Point) -> bool:
		""" Remove an entity from the space if one occupies that space """
		entity = next((e for e in self.__entities__ if e.position == position), None)

		if entity is None:
			raise Exception(f"No entity present at location {position}")

		self.__entities__.remove(entity)

		return entity not in self.__entities__

	def step(self):
		if len(self.__entities__) <= 0: return # Don't do anything if there are no entities in the world

		deaths = []
		births = []
		for x in range(self.__x_limit__ // block_size):
			for y in range(self.__y_limit__ // block_size):
				loc = Point(x, y)
				curr = self.get_entity(loc)
				neighbors = self.__get_neighbors__(loc)

				if curr is not None:
					# An entity is already at this location
					if neighbors in [2, 3]:
						continue # Entity survives to the next generation

					deaths.append(curr) # Underpopulated or overcrowded, so die if there is an entity there
				else:
					# No entity present at this location
					if neighbors != 3:
						continue # Birth rule not met

					births.append(Entity(position=loc))

		# Clean out dead entities
		self.__entities__ = [e for e in self.__entities__ if e not in deaths]

		# Insert birthed entities
		self.__entities__.extend(births)
