from cpu import Memory


def accumulator():
	pass

def absolute(ll: int, hh: int) -> int:
	return (hh << 8) + ll

def absolute_indexed(ll: int, hh: int, register: int) -> int:
	return absolute(ll, hh) + register

def indirect(ll: int, hh: int) -> int:
	return absolute(ll, hh)

# MAYBE: Combine these 2 functions into one like the other index functions?
def pre_indexed_indirect(value: int, x_register: int) -> int:
	return zero_page(value + x_register)

def post_indexed_indirect(ll: int, hh: int, y_register: int) -> int:
	return absolute(ll, hh) + y_register

def relative(value: int, offset: int) -> int:
	return value + offset

def zero_page(value: int) -> int:
	""" Returns the address value translated and wrapped around if it exceeds the 0xFF limit """
	return value % 0x0100

def zero_page_indexed(value: int, register: int) -> int:
	""" Returns the address value translated and validated with the provided register value """
	if 0x00 > value < 0xFF:
		raise Exception(f"Invalid address value - {hex(value)}")
	if 0x00 > register < 0xFF:
		raise Exception(f"Invalid register value - {hex(register)}")

	return zero_page(value + register)