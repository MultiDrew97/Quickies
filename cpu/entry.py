from cpu import INS_SET, MEMORY_MIN_ADDRESS, MEMORY_MAX_ADDRESS
from cpu.instr import CPU

cpu = CPU()
# The memory of the system
# FIXME: Convert to use bytes instead of int
mem: dict[int, int] = {
	0x0000: next(key for key, value in INS_SET.items() if value["label"] == "LDA"),
	0x0001: 0x0001
	# 0x0002: next(key for key, value in INS_SET.items() if value["label"] == "NOP"),
}

reg: dict[str, int] = {
	"program_counter": MEMORY_MIN_ADDRESS,
	"stack_pointer": 0x0,
	"accumulator": 0x0,
	"x": 0x0,
	"y": 0x0
}

flags = {
	"negative": False,
	"overflow": False,
	"break": False,
	"decimal": False,
	"interrupt": False,
	"zero": False,
	"carry": False,
}

# pc: int = MEMORY_MIN_ADDRESS # Program Counter
# sp: int | None = None # Stack Pointer
# a_reg: int = 0 # Accumulator Register
# x_reg: int | None = None # X Register
# y_reg: int | None = None # Y Register

# flag_carry: bool = False # Carry Flag
# flag_zero: bool = False # Zero Flag
# flag_interrupt_disable: bool = False # Disable interrupt flag
# flag_decimal_mode: bool = False # Decimal mode flag
# flag_break: bool = False # Break flag
# flag_overflow: bool = False # Overflow flag
# flag_negative: bool = False # Negative flag

def fetch(addr) -> int | None:
	if addr > MEMORY_MAX_ADDRESS or addr < MEMORY_MIN_ADDRESS:
		raise Exception("Address out of bounds")

	try:
		print(f"Fetching memory at address - {hex(addr)}...")
		return mem[addr % MEMORY_MAX_ADDRESS]
	except:
		return 0x0 # Nothing set at the provided address

def decode() -> None:
	print("Decoding instruction...")

def execute() -> None:
	print("Executing instruction...")


def init() -> None:
	print("Initializing unit...")
	reg["program_counter"] = MEMORY_MIN_ADDRESS


def reset() -> None:
	print("Resetting unit...")

	# Reset registers
	for r in reg.keys():
		reg[r] = 0x0

	# Reset flags
	for f in flags.keys():
		flags[f] = False

	init()

def __main__() -> None:
	reset()

	while reg["program_counter"] <= MEMORY_MAX_ADDRESS and not flags["break"]:
		print(f"Current Counter - {hex(reg["program_counter"])}")
		op_code = fetch(reg["program_counter"])
		if op_code is None:
			raise Exception(f"Address {reg["program_counter"]} is invalid")

		ins = INS_SET[op_code]

		if ins["label"] == "BRK":
			flags["break"] = True


		reg["program_counter"] += ins["bytes"]
		""" match (cmd):
			case _ if cmd == INS_SET["LDA"][0]:
				print("LDA Instruction Read")
				args = [fetch(reg["program_counter"] + i + 1) for i in range(INS_SET["LDA"][1] - 1)]
				print(f"Found Args: {args}")
				if (args[0] is None):
					raise Exception("Insufficient parameters for command")

				reg["accumulator"] = args[0]
				flags["negative"] = reg["accumulator"] < 0
				flags["zero"] = reg["accumulator"] == 0
				reg["program_counter"] += INS_SET["LDA"][1]
			case _ if cmd == INS_SET["BRK"][0]:
				print("Halt read. Stopping...")
				flags["break"] = True
			case _ if cmd == INS_SET["NOP"][0]:
				print("Noop read. Continuing...")
				reg["program_counter"] += INS_SET["NOP"][1]
			case None:
				print(f"Unknown command read - {cmd}")
				reg["program_counter"] += 1
		"""

if __name__ == "__main__":
	__main__()