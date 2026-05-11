def accumulator():
	pass

def absolute(value: int) -> int:
	return value

def absolute_indexed(value: int, register: int) -> int:
	return value + register

def indirect(least: int, highest: int) -> int:
	return (highest << 8) + least

# MAYBE: Combine these 2 functions into one like the other index functions?
def x_indexed_indirect(value: int, x_register: int) -> int:
	return (value + x_register) % 0x0100

def indirect_y_indexed(value: int, y_register: int) -> int:
	return (value + y_register) % 0x0100

def relative(value: int) -> int:
	return value

def zero_page(value: int) -> int:
	""" Returns the address value translated and validated """
	if 0x0 > value < 0xFF:
		raise Exception(f"Invalid address value - {hex(value)}")

	return value

def zero_page_indexed(value: int, register: int) -> int:
	""" Returns the address value translated and validated with the provided register value """
	if 0x00 > value < 0xFF:
		raise Exception(f"Invalid address value - {hex(value)}")
	if 0x00 > register < 0xFF:
		raise Exception(f"Invalid register value - {hex(register)}")

	return (value + register) % 0x0100