from gol import Point, Status, VisualComponent, block_size
import pygame as pyg


class Entity(VisualComponent):
	position: Point

	def __init__(self, name="New Entity", position: Point = Point(0, 0)):
		super().__init__()
		print(f"{name} is gestating...")
		self.__color__ = pyg.Color(255,255,255)
		self.__name__ = name
		self.__status__ = Status.ALIVE
		self.position = position
		print(f"{name} has been born at {position} 🎉")

	def draw(self, display: pyg.Surface):
		if not self.is_alive():
			return # Don't draw dead entities by default

		pyg.draw.rect(display, color=self.__color__, width=1,rect=pyg.Rect((self.position.x * block_size, self.position.y * block_size), (block_size, block_size)))

		return super().draw(display)

	def is_alive(self):
		return self.__status__ != Status.DEAD

	def can_kill(self) -> bool:
		# Determines whether the entity can be set to dead
		return True

	def kill(self) -> bool:
		print(f"Attempting to kill {self.__name__}...")
		if not self.can_kill():
			raise Exception(f"{self.__name__} cannot die 👎🏾")

		self.__status__ = Status.DEAD
		return not self.is_alive()

	def can_revive(self) -> bool:
		# Determines whether the entity can be set to alive again
		return True

	def revive(self) -> bool:
		print(f"Attempting to revive {self.__name__}")
		if not self.can_revive():
			raise Exception(f"{self.__name__} cannot be revived. GG brother 😅")

		self.__status__ = Status.ALIVE
		return self.is_alive()