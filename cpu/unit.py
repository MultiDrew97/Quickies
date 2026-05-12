from cpu import OP_CODES, Memory, MEMORY_MAX_ADDRESS, MEMORY_MIN_ADDRESS, NULL_POINTER, FLAGS
from cpu.addressing import absolute, absolute_indexed, indirect, zero_page, zero_page_indexed


class CPU:
	""" The central processing unit of the whole system. This will handle all of the logic preovided within  """
	PC: int
	""" The program counter  """
	SP: int
	""" The stack pointer """
	A: int
	""" Accumulator Register """
	X: int
	""" X Register """
	Y: int
	""" Y Register """
	status: dict[FLAGS, bool]
	""" Status Register - This will include the negative, overflow, break, decimal, interrupt disable, zero, and carry flags"""

	def __init__(self):
		self.status = dict().fromkeys(FLAGS, False)

	def __enter__(self) -> CPU:
		self.reset()
		return self

	def __exit__(self, _type, _value, _tb):
		pass

	def __is_negative__(self, value) -> bool:
		return value & 0b10000000 > 0x0

	def __is_zero__(self, value) -> bool:
		return value == 0x0

	def __set_a__(self, value: int):
		self.A = value
		self.status[FLAGS.Z] = self.__is_zero__(self.A)
		self.status[FLAGS.N] = self.__is_negative__(self.A)

	def __set_x__(self, value: int):
		self.X = value
		self.status[FLAGS.Z] = self.__is_zero__(self.X)
		self.status[FLAGS.N] = self.__is_negative__(self.X)

	def __set_y__(self, value: int):
		self.Y = value
		self.status[FLAGS.Z] = self.__is_zero__(self.Y)
		self.status[FLAGS.N] = self.__is_negative__(self.Y)

	def __read__(self, address: int, mem: Memory):
		""" Read mem from a specific mem location """
		return mem[address]

	def __write__(self, value: int, address: int, mem: Memory):
		""" Write data to a specific mem location """
		mem[address] = value

	def reset(self):
		""" Reset the CPU to it's initial state """
		self.PC = MEMORY_MIN_ADDRESS
		self.SP = self.A = self.X = self.Y = NULL_POINTER
		self.status = dict.fromkeys(FLAGS, False)

	def fetch(self, mem: Memory) -> int:
		""" Fetch the next value at the location of the program counter value and increment the counter """
		data = mem.get(self.PC, 0x00)
		# Increment the program counter and wrap around if it overflows
		self.PC = (self.PC + 1) % MEMORY_MAX_ADDRESS
		return data

	def execute(self, mem: Memory):
		""" Decode the provided op code and perform the actions it represents """
		while not self.status.get(FLAGS.B, False):
			print(f"Reading opcode from - {hex(self.PC)}")
			op_code = self.fetch(mem)
			match(OP_CODES(op_code)):
				case OP_CODES.NOP:
					continue
				case OP_CODES.BRK:
					self.status[FLAGS.B] = True
				case OP_CODES.LDA_IM:
					self.__set_a__(self.fetch(mem))
				case OP_CODES.LDA_ZP:
					data = self.fetch(mem)
					addr = zero_page(data)
					self.__set_a__(self.__read__(addr, mem=mem))
				case OP_CODES.LDA_ZP_IDX:
					data = self.fetch(mem)
					addr = zero_page_indexed(data, self.X)
					self.__set_a__(self.__read__(addr, mem=mem))
				case OP_CODES.LDA_ABS:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = indirect(ll, hh)
					self.__set_a__(self.__read__(addr, mem=mem))
				case OP_CODES.LDA_ABS_IDX_X:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, register=self.X)
					data = self.__read__(addr, mem=mem)
					self.__set_a__(data)
				case OP_CODES.LDA_ABS_IDX_Y:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, register=self.Y)
					self.__set_a__(self.__read__(addr, mem=mem))
				case OP_CODES.LDX_IM:
					self.__set_x__(self.fetch(mem))
				case OP_CODES.LDX_ZP:
					data = self.fetch(mem)
					addr = zero_page(data)
					self.__set_x__(self.__read__(addr, mem=mem))
				case OP_CODES.LDX_ZP_IDX:
					data = self.fetch(mem)
					addr = zero_page_indexed(data, self.Y)
					self.__set_x__(self.__read__(addr, mem=mem))
				case OP_CODES.LDX_ABS:
					data = self.fetch(mem)
					addr = zero_page_indexed(data, self.Y)
					self.__set_x__(self.__read__(addr, mem=mem))
				case OP_CODES.LDX_ABS_IDX:
					data = self.fetch(mem)
					addr = zero_page_indexed(data, self.Y)
					self.__set_x__(self.__read__(addr, mem=mem))
				case OP_CODES.LDY_IM:
					self.__set_y__(self.fetch(mem))
				case OP_CODES.LDY_ZP:
					data = self.fetch(mem)
					addr = zero_page(data)
					self.__set_y__(self.__read__(addr, mem = mem))
				case OP_CODES.LDY_ZP_IDX:
					data = self.fetch(mem)
					addr = zero_page_indexed(data, self.X)
					self.__set_y__(self.__read__(addr, mem= mem))
				case OP_CODES.LDY_ABS:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute(ll, hh)
					self.__set_y__(self.__read__(addr, mem= mem))
				case OP_CODES.LDY_ABS_IDX:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, register=self.X)
					self.__set_y__(self.__read__(addr, mem= mem))
				case OP_CODES.STA_ZP:
					data = self.fetch(mem)
					addr = zero_page(data)
					self.__write__(self.A, address=addr, mem=mem)
				case OP_CODES.STA_ZP_IDX:
					data = self.fetch(mem)
					addr = zero_page_indexed(data, self.X)
					self.__write__(self.A, address=addr, mem=mem)
				case OP_CODES.STA_ABS:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute(ll, hh)
					self.__write__(self.A, address=addr, mem=mem)
				case OP_CODES.STA_ABS_IDX_X:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, register=self.X)
					self.__write__(self.A, address=addr, mem=mem)
				case OP_CODES.STA_ABS_IDX_Y:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, register=self.Y)
					self.__write__(self.A, address=addr, mem=mem)
				case OP_CODES.STX_ZP:
					data = self.fetch(mem)
					addr = zero_page(data)
					self.__write__(self.X, address=addr, mem=mem)
				case OP_CODES.STX_ZP_IDX:
					data = self.fetch(mem)
					addr = zero_page_indexed(data, self.Y)
					self.__write__(self.X, address=addr, mem=mem)
				case OP_CODES.STX_ABS:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute(ll, hh)
					self.__write__(self.X, address=addr, mem=mem)
				case OP_CODES.STY_ZP:
					data = self.fetch(mem)
					addr = zero_page(data)
					self.__write__(self.Y, address=addr, mem=mem)
				case OP_CODES.STY_ZP_IDX:
					data = self.fetch(mem)
					addr = zero_page_indexed(data, self.X)
					self.__write__(self.Y, address=addr, mem=mem)
				case OP_CODES.STY_ABS:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute(ll, hh)
					self.__write__(self.Y, address=addr, mem=mem)
				case _:
					print(f"Unknown opcode - {hex(op_code)}")
