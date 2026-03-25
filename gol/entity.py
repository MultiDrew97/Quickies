from gol import Status


class Entity:
	def __init__(self, name="New Entity"):
		print(f"{name} is gestating...")
		self.__name__ = name
		self.__status__ = Status.ALIVE

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

	def ressurect(self) -> bool:
		print(f"Attempting to revive {self.__name__}")
		if not self.can_revive():
			raise Exception(f"{self.__name__} cannot be revived. GG brother 😅")

		self.__status__ = Status.ALIVE
		return self.is_alive()