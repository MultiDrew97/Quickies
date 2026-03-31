from pygame import Color, Surface
from enum import Enum
from typing import NamedTuple

"""
FIXME: Optimization

Currently the game is slow and laggy the more entities are on the screen since it gets massive. My current implementation is looping through every block in the space to perform logic checks and as the screen gets bigger and more entities need to be drawn, the frame rate drops significantly. I need to optimize this by only looping through the entities and their neighbors instead of the entire space. This will require a change in how the world is represented, likely using a grid or a hash map to keep track of where entities are located for faster access.
"""

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