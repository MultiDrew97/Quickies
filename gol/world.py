class World():
	# TODO: Expand for 3D
	def __init__(self, x: int, y: int) -> None:
		print("Loading your earthly realm...")
		if x < 1:
			raise Exception("Invalid x limit")
		if y < 1:
			raise Exception("Invalid y limit")

		self.__x_limit__, self.__y_limit__ = x, y
		self.flush()
		print("[DEBUG] Current Space:")
		print(self.__space__)
		print("Your oyster is ready")

	def flush(self):
		print("Sending the flood...")
		self.__space__ = [[False for _ in range(self.__x_limit__)] for _ in range(self.__y_limit__)]
		print("You have wiped out the population")

	def toggle_space(self, x: int, y: int) -> None:
		if x < 0 or x > self.__x_limit__:
			raise Exception("x is invalid")

		if y < 0 or y > self.__y_limit__:
			raise Exception("y is invalid")

		self.__space__[x][y] = not self.__space__[x][y]

	def is_alive(self, x: int, y: int) -> bool:
		return self.__space__[x][y]


