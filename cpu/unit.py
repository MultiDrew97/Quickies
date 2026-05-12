from cpu import OP_CODES, Memory, MEMORY_MAX_ADDRESS, MEMORY_MIN_ADDRESS, NULL_POINTER, FLAGS
from cpu.addressing import absolute, absolute_indexed, indirect, pre_indexed_indirect, zero_page, zero_page_indexed


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

	def __set_negative__(self, value):
		self.status[FLAGS.N] = value & 0x80 > 0x0

	def __set_zero__(self, value):
		self.status[FLAGS.Z] = value == 0x0

	def __set_overflow__(self, left: int, right: int):
		# TODO: Verify this works correctly for both addition and subtraction
		self.status[FLAGS.V] = (left ^ right) & 0x80 > 0x0

	def __set_carry__(self, value):
		self.status[FLAGS.C] = value & 0x80 > 0x0

	def __set_a__(self, value: int):
		self.A = value
		self.__set_zero__(self.A)
		self.__set_negative__(self.A)

	def __set_x__(self, value: int):
		self.X = value
		self.__set_zero__(self.X)
		self.__set_negative__(self.X)

	def __set_y__(self, value: int):
		self.Y = value
		self.__set_zero__(self.Y)
		self.__set_negative__(self.Y)

	def __read__(self, address: int, mem: Memory):
		""" Read mem from a specific mem location """
		return mem.get(address, NULL_POINTER)

	def __write__(self, value: int, address: int, mem: Memory):
		""" Write data to a specific mem location """
		mem[address] = value

	def __push_to_stack__(self, value: int, mem: Memory):
		""" Push a value onto the stack and decrement the stack pointer """
		addr = 0x0100 + zero_page(self.SP)
		self.__write__(value, address=addr, mem=mem)
		self.SP = (self.SP - 1) % 0x100

	def __status_to_byte__(self) -> int:
		""" Converts the status register into a byte value to be pushed onto the stack """
		value = 0x00
		for flag in FLAGS:
			if self.status[flag]:
				value += 1 << flag.value
		return value

	def __rel_offset__(self, offset: int):
		""" Converts a byte offset into a signed value to be added to the program counter for branching operations """
		# if offset > 0x7F:
		# 	offset -= 0x100
		self.PC = (self.PC + offset) % MEMORY_MAX_ADDRESS

	def reset(self):
		""" Reset the CPU to it's initial state """
		self.PC = MEMORY_MIN_ADDRESS # Place program counter at beginning
		self.SP = 0xFF # Place stack pointer at the "end" of the stack since it is decremented instead of incremented
		self.A = self.X = self.Y = NULL_POINTER
		self.status = dict.fromkeys(FLAGS, False)

	def fetch(self, mem: Memory) -> int:
		""" Fetch the next value at the location of the program counter value and increment the counter """
		data = self.__read__(self.PC, mem=mem)
		# Increment the program counter and wrap around if it overflows
		self.PC = (self.PC + 1) % MEMORY_MAX_ADDRESS
		return data

	def execute(self, mem: Memory):
		""" Decode the provided op code and perform the actions it represents """
		while not self.status.get(FLAGS.B, False):
			print(f"Reading opcode from - {hex(self.PC)}")
			#  Fetch command
			op_code = self.fetch(mem)

			""" TODO: Determine how to combine the different operations into singe functions that can be reused. I still can't find the pattern in the codes to determine what they do and how to handle addressing and combine yet, but will continue to keep an eye out for it. """
			# Decode the command to determine action and addressing mode

			# Execute the command based on decoded info
			match(OP_CODES(op_code)):
				# System based operations
				case OP_CODES.NOP:
					# Perform no operation
					continue
				case OP_CODES.BRK:
					# Set the break flag in status
					self.status[FLAGS.B] = True
				case OP_CODES.RTI:
					# Return from interrupt - Pull the status register from the stack and then pull the program counter from the stack
					continue

				# Status flag based operations
				case OP_CODES.CLC:
					# Clear the carry flag
					self.status[FLAGS.C] = False
				case OP_CODES.CLD:
					# Clear the decimal flag
					self.status[FLAGS.D] = False
				case OP_CODES.CLI:
					# Clear the interrupt disable flag
					self.status[FLAGS.I] = False
				case OP_CODES.CLV:
					# Clear the overflow flag
					self.status[FLAGS.V] = False
				case OP_CODES.SEC:
					# Set the carry flag
					self.status[FLAGS.C] = True
				case OP_CODES.SED:
					# Set the decimal flag
					self.status[FLAGS.D] = True
				case OP_CODES.SEI:
					# Set the interrupt disable flag
					self.status[FLAGS.I] = True

				# Logical based operations
				case OP_CODES.AND_IM:
					# AND memory value with accumulator from immediate value
					value = self.fetch(mem)
					self.__set_a__(self.A & value)
				case OP_CODES.AND_ZP:
					# AND memory value with accumulator from zero page
					zp = self.fetch(mem)
					addr = zero_page(zp)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A & value)
				case OP_CODES.AND_ZP_IDX_X:
					# AND memory value with accumulator from zero page indexed by X
					data = self.fetch(mem)
					zp_addr = zero_page_indexed(data, self.X)
					value = self.__read__(zp_addr, mem=mem)
					self.__set_a__(self.A & value)
				case OP_CODES.AND_ABS:
					# AND memory value with accumulator from absolute address
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute(ll, hh)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A & value)
				case OP_CODES.AND_ABS_IDX_X:
					# AND memory value with accumulator from absolute address indexed by X
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, self.X)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A & value)
				case OP_CODES.AND_ABS_IDX_Y:
					# AND memory value with accumulator from absolute address indexed by Y
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, self.Y)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A & value)
				case OP_CODES.EOR_IM:
					# EOR memory value with accumulator from immediate value
					value = self.fetch(mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_ZP:
					# EOR memory value with accumulator from zero page
					zp = self.fetch(mem)
					addr = zero_page(zp)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_ZP_IDX_X:
					# EOR memory value with accumulator from zero page indexed by X
					data = self.fetch(mem)
					zp_addr = zero_page_indexed(data, self.X)
					value = self.__read__(zp_addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_ABS:
					# EOR memory value with accumulator from absolute address
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute(ll, hh)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_ABS_IDX_X:
					# EOR memory value with accumulator from absolute address indexed by X
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, self.X)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_ABS_IDX_Y:
					# EOR memory value with accumulator from absolute address indexed by Y
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, self.Y)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_IDX_X:
					# EOR memory value with accumulator from Pre-Indexed Indirect X
					data = self.fetch(mem)
					zp_addr = zero_page_indexed(data, self.X)
					ll = self.__read__(zp_addr, mem=mem)
					hh = self.__read__(zero_page(zp_addr + 1), mem=mem)
					addr = absolute(ll, hh)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_IDX_Y:
					# EOR memory value with accumulator from Post-Indexed Indirect Y
					data = self.fetch(mem)
					ll = self.__read__(zp_addr, mem=mem)
					hh = self.__read__(zero_page(zp_addr + 1), mem=mem)
					addr = absolute_indexed(ll, hh, self.Y)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.ORA_IM:
					# OR memory value with accumulator from immediate value
					value = self.fetch(mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_ZP:
					# OR memory value with accumulator from zero page
					zp = self.fetch(mem)
					addr = zero_page(zp)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_ZP_IDX_X:
					# OR memory value with accumulator from zero page indexed by X
					data = self.fetch(mem)
					zp_addr = zero_page_indexed(data, self.X)
					value = self.__read__(zp_addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_ABS:
					# OR memory value with accumulator from absolute address
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute(ll, hh)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_ABS_IDX_X:
					# OR memory value with accumulator from absolute address indexed by X
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, self.X)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_ABS_IDX_Y:
					# OR memory value with accumulator from absolute address indexed by Y
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute_indexed(ll, hh, self.Y)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_IDX_X:
					# OR memory value with accumulator from Pre-Indexed Indirect X
					data = self.fetch(mem)
					zp_addr = zero_page_indexed(data, self.X)
					ll = self.__read__(zp_addr, mem=mem)
					hh = self.__read__(zero_page(zp_addr + 1), mem=mem)
					addr = absolute(ll, hh)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_IDX_Y:
					# OR memory value with accumulator from Post-Indexed Indirect Y
					data = self.fetch(mem)
					ll = self.__read__(zp_addr, mem=mem)
					hh = self.__read__(zero_page(zp_addr + 1), mem=mem)
					addr = absolute_indexed(ll, hh, self.Y)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.BIT_ZP:
					# BIT memory value with accumulator from zero page
					zp = self.fetch(mem)
					addr = zero_page(zp)
					value = self.__read__(addr, mem=mem)

					fla = self.A & value

					self.status[FLAGS.V] = bin(fla)[FLAGS.V.value] == "1"
					self.status[FLAGS.N] = bin(fla)[FLAGS.N.value] == "1"
				case OP_CODES.BIT_ABS:
					# BIT memory value with accumulator from absolute address
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute(ll, hh)
					value = self.__read__(addr, mem=mem)
					fla = self.A & value

					self.status[FLAGS.V] = bin(fla)[FLAGS.V.value] == "1"
					self.status[FLAGS.N] = bin(fla)[FLAGS.N.value] == "1"

				# Arithmetic based operations
				case OP_CODES.ADC_IM:
					# Add with carry from immediate value
				case OP_CODES.SBC_IM:
					# Subtract with carry from immediate value
				case OP_CODES.CMP_IM:
					# Compare memory value with accumulator from immediate value
				case OP_CODES.CPX_IM:
					# Compare memory value with X from immediate value
				case OP_CODES.CPY_IM:
					# Compare memory value with Y from immediate value

				# Register transfer based operations
				case OP_CODES.TAX:
					# Transfer accumulator to X
					self.__set_x__(self.A)
				case OP_CODES.TAY:
					# Transfer accumulator to Y
					self.__set_y__(self.A)
				case OP_CODES.TXA:
					# Transfer X to accumulator
					self.__set_a__(self.X)
				case OP_CODES.TYA:
					# Transfer Y to accumulator
					self.__set_a__(self.Y)

				# Stack related operations
				case OP_CODES.TSX:
					# Transfer stack pointer to X
					self.__set_x__(self.SP)
				case OP_CODES.TXS:
					# Transfer X to stack pointer
					self.SP = self.X
				case OP_CODES.PHP:
					# Push the status register onto the stack
					self.__push_to_stack__(self.__status_to_byte__(), mem=mem)

				# Shift and Rotate based operations
				case OP_CODES.ASL_ZP:
					# Shift memory value left by one
					zp = self.fetch(mem)
					addr = zero_page(zp)
					value = self.__read__(addr, mem=mem)
					self.__set_carry__(value)
					value = (value << 1) % 0x100
					self.__write__(value, address=addr, mem=mem)
				case OP_CODES.ASL:
					# Shift the value in the accumulator left by one
					self.__set_carry__(self.A)
					self.__set_a__((self.A << 1) % 0x100)
				case OP_CODES.ASL_ABS:
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute(ll, hh)
					value = self.__read__(addr, mem=mem)
					self.__set_carry__(value)
					value = (value << 1) % 0x100
					self.__write__(value, address=addr, mem=mem)

				# Jumps and Calls based operations
				case OP_CODES.JMP_ABS:
				case OP_CODES.JMP_IND:
				case OP_CODES.JSR_ABS:
				case OP_CODES.RTS:

				# Branching based operations
				case OP_CODES.BPL:
					# Branch if positive (negative flag is not set)
					if self.status[FLAGS.N]:
						# Continue since N is set
						continue

					self.__rel_offset__(self.fetch(mem))
				case OP_CODES.BMI:
					# Branch if negative (negative flag is set)
					if not self.status[FLAGS.N]:
						# Continue since N is not set
						continue

					self.__rel_offset__(self.fetch(mem))
				case OP_CODES.BEQ:
					# Branch if 0 (zero flag is set)
					if not self.status[FLAGS.Z]:
						# Continue since Z is not set
						continue

					self.__rel_offset__(self.fetch(mem))
				case OP_CODES.BNE:
					# Branch if not equal (zero flag is not set)
					if self.status[FLAGS.Z]:
						# Continue since Z is set
						continue

					self.__rel_offset__(self.fetch(mem))
				case OP_CODES.BCC:
					# Branch if carry is not set (carry flag is cleared)
					if self.status[FLAGS.C]:
						# Continue since C is not set
						continue

					self.__rel_offset__(self.fetch(mem))
				case OP_CODES.BCS:
					# Branch if carry is set (carry flag is set)
					if not self.status[FLAGS.C]:
						# Continue since C is not set
						continue

					self.__rel_offset__(self.fetch(mem))
				case OP_CODES.BVC:
					# Branch if overflow is not set (overflow flag is cleared)
					if self.status[FLAGS.V]:
						# Continue since V is not set
						continue

					self.__rel_offset__(self.fetch(mem))
				case OP_CODES.BVS:
					# Branch if overflow is set (overflow flag is set)
					if not self.status[FLAGS.V]:
						# Continue since V is not set
						continue

					self.__rel_offset__(self.fetch(mem))

				# Load and Store based operations
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
