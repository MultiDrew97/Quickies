class Gameboard():
	board: list[list[bool]]

	def __init__(self, rows: int, cols: int) -> None:
		print("Loading your earthly realm...")
		if rows < 1:
			raise Exception("Invalid row count")
		if cols < 1:
			raise Exception("Invalid column count")

		self.__rows__, self.__cols__ = rows, cols
		self.clear_table()
		print("[DEBUG] Current Board:")
		print(self.board)
		print("Your oyster is ready")

	def clear_table(self):
		print("Sending the nuke...")
		self.board = [[False for _ in range(self.__cols__)] for _ in range(self.__rows__)]
		print("You have wiped out the population")

	def toggle_space(self, row: int, col: int) -> None:
		if row < 0 or row > len(self.board):
			raise Exception("Row is invalid")

		if col < 0 or col > len(self.board):
			raise Exception("Col is invalid")

		self.board[row][col] = not self.board[row][col]

	def get_state(self, row: int, col: int) -> bool:
		return self.board[row][col]


