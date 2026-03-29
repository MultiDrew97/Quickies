from pygame import Color, Surface
from enum import Enum
from typing import NamedTuple

block_size = 10

class Status(Enum):
	ALIVE="ALIVE"
	DEAD="DEAD"

class Point(NamedTuple):
	x: int
	y: int

	def __str__(self):
		return f"({self.x}, {self.y})"

	def __eq__(self, value: Point):
		return self.x == value.x and self.y == value.y

class VisualComponent:
	__color__: Color

	def draw(self, display: Surface, *args):
		pass