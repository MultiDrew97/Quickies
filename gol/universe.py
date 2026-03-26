from gol.entity import Entity
from gol.world import World

max_space_x, max_space_y = 9, 9

class Universe:
	age: int
	def __init__(self, tick_rate: int = 1) -> None:
		self.__space__ = World(max_space_x, max_space_y)
		self.__tick_rate__ = tick_rate
		self.age = 0

	def tick(self) -> None:
		self.age += self.__tick_rate__
		for x in range(max_space_x):
			for y in range(max_space_y):
				self.__entropy__(x, y)

	def __entropy__(self, x: int, y: int):
		try:
			curr_entity = self.__space__.get_entity(x, y)
			live_neighbors = self.__count_live_neighbors(x, y)

			if curr_entity == None:
				raise Exception(f"No entity at space coordinates ({x}, {y})")

			if not curr_entity.is_alive() and live_neighbors == 3:
				curr_entity.revive()
				return

			if curr_entity.is_alive() and (live_neighbors < 2 or live_neighbors > 3):
				curr_entity.kill()
				return
		except Exception:
			print("An error occured")

	def __count_live_neighbors(self, x: int, y: int) -> int:
		count: int = 0
		for dX in range(x - 1, x + 1):
			for dY in range(y - 1, y + 1):
				count += 1 if (dX != x and dY != y) and self.__space__.get_entity(dX, dY).is_alive() else 0

		return count




