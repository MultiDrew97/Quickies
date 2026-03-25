from gol import Status


class Entity:
	def __init__(self, name="New Entity"):
		print("Creating Entity...")
		self.__name__ = name
		self.__status__ = Status.ALIVE

	def is_alive(self):
		return self.__status__ != Status.DEAD

	def kill(self) -> None:
		self.__status__ = Status.DEAD