from cpu import Memory, OP_CODES
from cpu.unit import CPU

# FIXME: Convert to use bytes instead of int
""" The memory of the system """
mem: Memory

def init() -> None:
	global mem
	print("Initializing unit...")
	mem = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: OP_CODES.NOP.value,
		0x0002: OP_CODES.STA_ZP.value,
		0x0003: 0x04
	}

def __main__() -> None:
	with CPU() as cpu:
		init()
		cpu.execute(mem)
		print(f"Resulting Memory: {mem}")

if __name__ == "__main__":
	__main__()