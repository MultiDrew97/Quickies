from argparse import ArgumentError
from typing import Any

from cpu import INS_HALT, MEMORY_MIN_ADDRESS, MEMORY_MAX_ADDRESS, INS_LDA_IM

# The memory of the system
mem = {
	0x0000: INS_LDA_IM[0],
	0x0001: 0x0001,
	0x0002: INS_HALT[0]
}

pc: int = MEMORY_MIN_ADDRESS # Program Counter
sp: int | None = None # Stack Pointer
a_reg: int = 0 # Accumulator Register
x_reg: int | None = None # X Register
y_reg: int | None = None # Y Register

flag_carry: bool = False # Carry Flag
flag_zero: bool = False # Zero Flag
flag_interrupt_disable: bool = False # Disable interrupt flag
flag_decimal_mode: bool = False # Decimal mode flag
flag_break: bool = False # Break flag
flag_overflow: bool = False # Overflow flag
flag_negative: bool = False # Negative flag

def fetch(addr) -> int | None:
	if addr > MEMORY_MAX_ADDRESS or addr < MEMORY_MIN_ADDRESS:
		raise Exception("Address out of bounds")

	try:
		print("Fetching instruction...")
		return mem[addr % MEMORY_MAX_ADDRESS]
	except:
		return None # Nothing at the provided address

def decode() -> None:
	print("Decoding instruction...")

def execute(cmd, args) -> None:
	global pc
	print("Executing instruction...")
	data = fetch(pc)
	print(f"Retrieved Data: {data}")
	if (data is None):
		print(f"No command found")
		return

	pc += 1
	print(f"Fetched Data: {fetch(pc)}")


def init() -> None:
	print("Initializing...")


def reset() -> None:
	global pc, sp, a_reg, x_reg, y_reg, flag_break, flag_carry, flag_zero, flag_interrupt_disable, flag_decimal_mode, flag_overflow, flag_negative
	print("Resetting...")
	pc = MEMORY_MIN_ADDRESS # Reset to the start of the memory stack
	a_reg = 0
	sp = x_reg = y_reg = None
	flag_carry = flag_zero = flag_interrupt_disable = flag_decimal_mode = flag_break = flag_overflow = flag_negative = False
	init()

def __main__() -> None:
	global pc, a_reg,flag_carry, flag_break, flag_decimal_mode, flag_interrupt_disable, flag_decimal_mode, flag_negative, flag_overflow, flag_zero
	reset()
	while pc < MEMORY_MAX_ADDRESS:
		print("Current Counter", pc)
		cmd = fetch(pc)
		match (cmd):
			case _ if cmd == INS_LDA_IM[0]:
				print("LDA Instruction Read")
				args = [fetch(pc + i + 1) for i in range(INS_LDA_IM[1] - 1)]
				print(f"Found Args: {args}")
				if (args[0] is None):
					raise Exception("Insufficient parameters for command")

				a_reg = args[0]
				flag_negative = a_reg < 0
				flag_zero = a_reg == 0
				pc += INS_LDA_IM[1]
			case _ if cmd == INS_HALT[0]:
				print("Halt read. Stopping...")
				break
			case _:
				pc += 1
		print("Current Accumulator", a_reg)


if __name__ == "__main__":
	__main__()