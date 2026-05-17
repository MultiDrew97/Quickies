from cpu import OP_CODES, STACK_START_LOCATION, Memory, MEMORY_MAX_ADDRESS, MEMORY_MIN_ADDRESS, NULL_POINTER, FLAGS
from cpu.addressing import *


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

	def __set_negative__(self, value: int):
		self.status[FLAGS.N] = value & 0x80 > 0x00

	def __set_zero__(self, value: int):
		self.status[FLAGS.Z] = value == 0x00

	def __set_overflow__(self, left: int, right: int):
		# TODO: Verify this works correctly for both addition and subtraction
		self.status[FLAGS.V] = (left ^ right) & 0x80 > 0x00

	def __set_carry__(self, value: int):
		self.status[FLAGS.C] = value & 0x80 > 0x00

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

	def __read__(self, address: int, mem: Memory) -> int:
		""" Read mem from a specific mem location """
		return mem.get(address, NULL_POINTER)

	def __write__(self, value: int, address: int, mem: Memory):
		""" Write data to a specific mem location """
		mem[address] = value

	def __push_to_stack__(self, value: int, mem: Memory):
		""" Push a value onto the stack and decrement the stack pointer """
		addr = 0x0100 + (self.SP % 0x0100)
		self.__write__(value, address=addr, mem=mem)
		self.SP = (self.SP - 1) % 0x100

	def __pull_from_stack__(self, mem: Memory) -> int:
		""" Push a value onto the stack and decrement the stack pointer """
		addr = 0x0100 + (self.SP % 0x0100)
		value = self.__read__(addr, mem=mem)
		self.SP = (self.SP + 1) % 0x100
		return value

	def __status_to_byte__(self) -> int:
		""" Converts the status register into a byte value to be pushed onto the stack """
		value = 0x00
		for flag in FLAGS:
			if self.status[flag]:
				value += 1 << flag.value
		return value

	def __byte_to_status__(self, value: int):
		""" Converts the status register into a byte value to be pushed onto the stack """
		# value = 0x00
		for flag in FLAGS:
			print(f"Current Flag - {flag}")
			print(f"Value - {bin(value)}")
			print(f"Shifted Value - {bin(value >> flag.value)}")
			print(f"Set - {(value >> flag.value) % 0b10}")
			self.status[flag] = (value >> flag.value) % 0b10 == 1

	# def __rel_offset__(self, offset: int):
	# 	""" Converts a byte offset into a signed value to be added to the program counter for branching operations """
	# 	# if offset > 0x7F:
	# 	# 	offset -= 0x100
	# 	self.PC = (self.PC + offset) % MEMORY_MAX_ADDRESS

	def reset(self):
		""" Reset the CPU to it's initial state """
		# Reset the program counter
		self.PC = MEMORY_MIN_ADDRESS

		# Reset the stack pointer
		self.SP = STACK_START_LOCATION

		# Reset registers
		self.A = self.X = self.Y = NULL_POINTER

		# Reset status register
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
					addr = zero_page(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A & value)
				case OP_CODES.AND_ZP_IDX_X:
					# AND memory value with accumulator from zero page indexed by X
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A & value)
				case OP_CODES.AND_ABS:
					# AND memory value with accumulator from absolute address
					addr = absolute(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A & value)
				case OP_CODES.AND_ABS_IDX_X:
					# AND memory value with accumulator from absolute address indexed by X
					addr = absolute(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A & value)
				case OP_CODES.AND_ABS_IDX_Y:
					# AND memory value with accumulator from absolute address indexed by Y
					addr = absolute(cpu=self, mem=mem, offset=self.Y)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A & value)
				case OP_CODES.EOR_IM:
					# EOR memory value with accumulator from immediate value
					value = self.fetch(mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_ZP:
					# EOR memory value with accumulator from zero page
					addr = zero_page(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_ZP_IDX_X:
					# EOR memory value with accumulator from zero page indexed by X
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_ABS:
					# EOR memory value with accumulator from absolute address
					addr = absolute(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_ABS_IDX_X:
					# EOR memory value with accumulator from absolute address indexed by X
					addr = absolute(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_ABS_IDX_Y:
					# EOR memory value with accumulator from absolute address indexed by Y
					addr = absolute(cpu=self, mem=mem, offset=self.Y)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_IDX_X:
					# EOR memory value with accumulator from Pre-Indexed Indirect X
					addr = pre_indexed_indirect(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.EOR_IDX_Y:
					# EOR memory value with accumulator from Post-Indexed Indirect Y
					addr = post_indexed_indirect(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A ^ value)
				case OP_CODES.ORA_IM:
					# OR memory value with accumulator from immediate value
					value = self.fetch(mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_ZP:
					# OR memory value with accumulator from zero page
					addr = zero_page(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_ZP_IDX_X:
					# OR memory value with accumulator from zero page indexed by X
					data = self.fetch(mem)
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_ABS:
					# OR memory value with accumulator from absolute address
					addr = absolute(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_ABS_IDX_X:
					# OR memory value with accumulator from absolute address indexed by X
					addr = absolute(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_ABS_IDX_Y:
					# OR memory value with accumulator from absolute address indexed by Y
					addr = absolute(cpu=self, mem=mem, offset=self.Y)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_IDX_X:
					# OR memory value with accumulator from Pre-Indexed Indirect X
					addr = pre_indexed_indirect(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.ORA_IDX_Y:
					# OR memory value with accumulator from Post-Indexed Indirect Y
					addr = post_indexed_indirect(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_a__(self.A | value)
				case OP_CODES.BIT_ZP:
					# BIT memory value with accumulator from zero page
					addr = zero_page(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)

					cmp = self.A & value

					self.status[FLAGS.V] = bin(cmp)[FLAGS.V.value] == "1"
					self.status[FLAGS.N] = bin(cmp)[FLAGS.N.value] == "1"
				case OP_CODES.BIT_ABS:
					# BIT memory value with accumulator from absolute address
					addr = absolute(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)

					cmp = self.A & value

					self.status[FLAGS.V] = bin(cmp)[FLAGS.V.value] == "1"
					self.status[FLAGS.N] = bin(cmp)[FLAGS.N.value] == "1"

				# Arithmetic based operations
				# TODO: Fix overflow setting
				case OP_CODES.ADC_IM:
					# Add with carry from immediate value
					value = self.fetch(mem)
					carry = 1 if self.status[FLAGS.C] else 0
					self.__set_a__(self.A + value + carry)
				case OP_CODES.ADC_ZP:
					# Add with carry from zero page
					addr = zero_page(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					carry = 1 if self.status[FLAGS.C] else 0
					self.__set_a__(self.A + value + carry)
				case OP_CODES.ADC_ZP_IDX_X:
					# Add with carry from zero page indexed by X
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					carry = 1 if self.status[FLAGS.C] else 0
					self.__set_a__(self.A + value + carry)
				case OP_CODES.ADC_ABS:
					# Add with carry from absolute address
					addr = absolute(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					carry = 1 if self.status[FLAGS.C] else 0
					self.__set_a__(self.A + value + carry)
				case OP_CODES.ADC_ABS_IDX_X:
					# Add with carry from absolute address indexed by X
					addr = absolute(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					carry = 1 if self.status[FLAGS.C] else 0
					self.__set_a__(self.A + value + carry)
				case OP_CODES.ADC_ABS_IDX_Y:
					# Add with carry from absolute address indexed by Y
					addr = absolute(cpu=self, mem=mem, offset=self.Y)
					value = self.__read__(addr, mem=mem)
					carry = 1 if self.status[FLAGS.C] else 0
					self.__set_a__(self.A + value + carry)
				case OP_CODES.ADC_IDX_X:
					# Add with carry from Pre-Indexed Indirect X
					addr = pre_indexed_indirect(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					carry = 1 if self.status[FLAGS.C] else 0
					self.__set_a__(self.A + value + carry)
				case OP_CODES.ADC_IDX_Y:
					# Add with carry from Post-Indexed Indirect Y
					addr = post_indexed_indirect(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					carry = 1 if self.status[FLAGS.C] else 0
					self.__set_a__(self.A + value + carry)
				case OP_CODES.SBC_IM:
					# Subtract with carry from immediate value
					value = self.fetch(mem)
					carry = 0 if self.status[FLAGS.C] else 1
					self.__set_a__(self.A - value - carry)
				case OP_CODES.SBC_ZP:
					# Subtract with carry from zero page
					addr = zero_page(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					carry = 0 if self.status[FLAGS.C] else 1
					self.__set_a__(self.A - value - carry)
				case OP_CODES.SBC_ZP_IDX_X:
					# Subtract with carry from zero page indexed by X
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					carry = 0 if self.status[FLAGS.C] else 1
					self.__set_a__(self.A - value - carry)
				case OP_CODES.SBC_ABS:
					# Subtract with carry from absolute address
					addr = absolute(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					carry = 0 if self.status[FLAGS.C] else 1
					self.__set_a__(self.A - value - carry)
				case OP_CODES.SBC_ABS_IDX_X:
					# Subtract with carry from absolute address indexed by X
					addr = absolute(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					carry = 0 if self.status[FLAGS.C] else 1
					self.__set_a__(self.A - value - carry)
				case OP_CODES.SBC_ABS_IDX_Y:
					# Subtract with carry from absolute address indexed by Y
					addr = absolute(cpu=self, mem=mem, offset=self.Y)
					value = self.__read__(addr, mem=mem)
					carry = 0 if self.status[FLAGS.C] else 1
					self.__set_a__(self.A - value - carry)
				case OP_CODES.SBC_IDX_X:
					# Subtract with carry from Pre-Indexed Indirect X
					addr = pre_indexed_indirect(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					carry = 0 if self.status[FLAGS.C] else 1
					self.__set_a__(self.A - value - carry)
				case OP_CODES.SBC_IDX_Y:
					# Subtract with carry from Post-Indexed Indirect Y
					addr = post_indexed_indirect(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					carry = 0 if self.status[FLAGS.C] else 1
					self.__set_a__(self.A - value - carry)
				case OP_CODES.CMP_IM:
					# Compare memory value with accumulator from immediate value
					value = self.fetch(mem)
					cmp = self.A - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CMP_ZP:
					# Compare memory value with accumulator from zero page
					addr = zero_page(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					cmp = self.A - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CMP_ZP_IDX_X:
					# Compare memory value with accumulator from zero page indexed by X
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					cmp = self.A - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CMP_ABS:
					# Compare memory value with accumulator from absolute address
					addr = absolute(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					cmp = self.A - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CMP_ABS_IDX_X:
					# Compare memory value with accumulator from absolute address indexed by X
					ll = self.fetch(mem)
					hh = self.fetch(mem)
					addr = absolute(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					cmp = self.A - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CMP_ABS_IDX_Y:
					# Compare memory value with accumulator from absolute address indexed by Y
					addr = absolute(cpu=self, mem=mem, offset=self.Y)
					value = self.__read__(addr, mem=mem)
					cmp = self.A - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CMP_IDX_X:
					# Compare memory value with accumulator from Pre-Indexed Indirect X
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					value = self.__read__(addr, mem=mem)
					cmp = self.A - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CMP_IDX_Y:
					# Compare memory value with accumulator from Post-Indexed Indirect Y
					addr = post_indexed_indirect(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					cmp = self.A - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CPX_IM:
					# Compare memory value with X from immediate value
					value = self.fetch(mem)
					cmp = self.X - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CPX_ZP:
					# Compare memory value with X from zero page
					addr = zero_page(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					cmp = self.X - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CPX_ABS:
					# Compare memory value with X from absolute address
					addr = absolute(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					cmp = self.X - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CPY_IM:
					# Compare memory value with Y from immediate value
					value = self.fetch(mem)
					cmp = self.Y - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CPY_ZP:
					# Compare memory value with Y from zero page
					addr = zero_page(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					cmp = self.Y - value
					self.status[FLAGS.C] = cmp > 0x00
					self.__set_zero__(cmp)
					self.__set_negative__(cmp)
				case OP_CODES.CPY_ABS:
					# Compare memory value with Y from absolute address
					# TODO: Convert to use a match that can seect between the addressing modes when I finally figure out the pattern in the op codes to determine how to combine them into single functions that can be reused instead of having to write out each one separately like this
					# ll = self.fetch(mem)
					# hh = self.fetch(mem)
					addr = absolute(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					fla = self.Y - value
					self.status[FLAGS.C] = fla > 0x00
					self.__set_zero__(fla)
					self.__set_negative__(fla)

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
				case OP_CODES.PHP:
					# Push the status register onto the stack
					self.__push_to_stack__(self.__status_to_byte__(), mem=mem)
				case OP_CODES.TSX:
					# Transfer stack pointer to X
					self.__set_x__(self.SP)
				case OP_CODES.TXS:
					# Transfer X to stack pointer
					self.SP = self.X

				# Shift and Rotate based operations
				case OP_CODES.ASL:
					# Shift the value in the accumulator left by one
					self.__set_carry__(self.A)
					self.__set_a__((self.A << 1) % 0x100)
				case OP_CODES.ASL_ZP:
					addr = zero_page(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_carry__(value)
					value = (value << 1) % 0x100
					self.__write__(value, address=addr, mem=mem)
				case OP_CODES.ASL_ABS:
					addr = absolute(cpu=self, mem=mem)
					value = self.__read__(addr, mem=mem)
					self.__set_carry__(value)
					value = (value << 1) % 0x100
					self.__write__(value, address=addr, mem=mem)

				# Jumps and Calls based operations
				case OP_CODES.JMP_ABS:
					addr = absolute(cpu=self, mem=mem)
					self.PC = addr
				case OP_CODES.JMP_IND:
					addr = indirect(cpu=self, mem=mem)
					self.PC = addr
				case OP_CODES.JSR_ABS:
					addr = absolute(cpu=self, mem=mem)
					self.PC = addr
				case OP_CODES.RTS:
					ll = self.__pull_from_stack__(mem=mem)
					hh = self.__pull_from_stack__(mem=mem)

					self.PC = (hh << 8) + ll - 1

				# Branching based operations
				case OP_CODES.BPL:
					# Branch if positive (negative flag is not set)
					if self.status[FLAGS.N]:
						# Continue since N is set
						continue

					addr = relative(cpu=self, mem=mem)
				case OP_CODES.BMI:
					# Branch if negative (negative flag is set)
					if not self.status[FLAGS.N]:
						# Continue since N is not set
						continue

					addr = relative(cpu=self, mem=mem)
				case OP_CODES.BEQ:
					# Branch if 0 (zero flag is set)
					if not self.status[FLAGS.Z]:
						# Continue since Z is not set
						continue

					addr = relative(cpu=self, mem=mem)
				case OP_CODES.BNE:
					# Branch if not equal (zero flag is not set)
					if self.status[FLAGS.Z]:
						# Continue since Z is set
						continue

					addr = relative(cpu=self, mem=mem)
				case OP_CODES.BCC:
					# Branch if carry is not set (carry flag is cleared)
					if self.status[FLAGS.C]:
						# Continue since C is not set
						continue

					addr = relative(cpu=self, mem=mem)
				case OP_CODES.BCS:
					# Branch if carry is set (carry flag is set)
					if not self.status[FLAGS.C]:
						# Continue since C is not set
						continue

					addr = relative(cpu=self, mem=mem)
				case OP_CODES.BVC:
					# Branch if overflow is not set (overflow flag is cleared)
					if self.status[FLAGS.V]:
						# Continue since V is not set
						continue

					addr = relative(cpu=self, mem=mem)
				case OP_CODES.BVS:
					# Branch if overflow is set (overflow flag is set)
					if not self.status[FLAGS.V]:
						# Continue since V is not set
						continue

					addr = relative(cpu=self, mem=mem)

				# Load and Store based operations
				case OP_CODES.LDA_IM:
					value = self.fetch(mem)
					self.__set_a__(value)
				case OP_CODES.LDA_ZP:
					addr = zero_page(cpu=self, mem=mem)
					self.__set_a__(self.__read__(addr, mem=mem))
				case OP_CODES.LDA_ZP_IDX:
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					self.__set_a__(self.__read__(addr, mem=mem))
				case OP_CODES.LDA_ABS:
					addr = absolute(cpu=self, mem=mem)
					self.__set_a__(self.__read__(addr, mem=mem))
				case OP_CODES.LDA_ABS_IDX_X:
					addr = absolute(cpu=self, mem=mem, offset=self.X)
					data = self.__read__(addr, mem=mem)
					self.__set_a__(data)
				case OP_CODES.LDA_ABS_IDX_Y:
					addr = absolute(cpu=self, mem=mem, offset=self.Y)
					self.__set_a__(self.__read__(addr, mem=mem))
				case OP_CODES.LDX_IM:
					self.__set_x__(self.fetch(mem))
				case OP_CODES.LDX_ZP:
					addr = zero_page(cpu=self, mem=mem)
					self.__set_x__(self.__read__(addr, mem=mem))
				case OP_CODES.LDX_ZP_IDX:
					addr = zero_page(cpu=self, mem=mem, offset=self.Y)
					self.__set_x__(self.__read__(addr, mem=mem))
				case OP_CODES.LDX_ABS:
					addr = zero_page(cpu=self, mem=mem, offset=self.Y)
					self.__set_x__(self.__read__(addr, mem=mem))
				case OP_CODES.LDX_ABS_IDX:
					addr = zero_page(cpu=self, mem=mem, offset=self.Y)
					self.__set_x__(self.__read__(addr, mem=mem))
				case OP_CODES.LDY_IM:
					self.__set_y__(self.fetch(mem))
				case OP_CODES.LDY_ZP:
					addr = zero_page(cpu=self, mem=mem)
					self.__set_y__(self.__read__(addr, mem = mem))
				case OP_CODES.LDY_ZP_IDX:
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					self.__set_y__(self.__read__(addr, mem= mem))
				case OP_CODES.LDY_ABS:
					addr = absolute(cpu=self, mem=mem)
					self.__set_y__(self.__read__(addr, mem= mem))
				case OP_CODES.LDY_ABS_IDX:
					addr = absolute(cpu=self, mem=mem, offset=self.X)
					self.__set_y__(self.__read__(addr, mem= mem))
				case OP_CODES.STA_ZP:
					addr = zero_page(cpu=self, mem=mem)
					self.__write__(self.A, address=addr, mem=mem)
				case OP_CODES.STA_ZP_IDX:
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					print(f"Stored address - {addr}")
					self.__write__(self.A, address=addr, mem=mem)
				case OP_CODES.STA_ABS:
					addr = absolute(cpu=self, mem=mem)
					self.__write__(self.A, address=addr, mem=mem)
				case OP_CODES.STA_ABS_IDX_X:
					addr = absolute(cpu=self, mem=mem, offset=self.X)
					self.__write__(self.A, address=addr, mem=mem)
				case OP_CODES.STA_ABS_IDX_Y:
					addr = absolute(cpu=self, mem=mem, offset=self.Y)
					self.__write__(self.A, address=addr, mem=mem)
				case OP_CODES.STX_ZP:
					addr = zero_page(cpu=self, mem=mem)
					self.__write__(self.X, address=addr, mem=mem)
				case OP_CODES.STX_ZP_IDX:
					addr = zero_page(cpu=self, mem=mem, offset=self.Y)
					self.__write__(self.X, address=addr, mem=mem)
				case OP_CODES.STX_ABS:
					addr = absolute(cpu=self, mem=mem)
					self.__write__(self.X, address=addr, mem=mem)
				case OP_CODES.STY_ZP:
					addr = zero_page(cpu=self, mem=mem)
					self.__write__(self.Y, address=addr, mem=mem)
				case OP_CODES.STY_ZP_IDX:
					addr = zero_page(cpu=self, mem=mem, offset=self.X)
					self.__write__(self.Y, address=addr, mem=mem)
				case OP_CODES.STY_ABS:
					addr = absolute(cpu=self, mem=mem)
					self.__write__(self.Y, address=addr, mem=mem)
				case _:
					print(f"Unknown opcode - {hex(op_code)}")
