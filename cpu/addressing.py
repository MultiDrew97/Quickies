def accumulator():
	pass

def absolute(value: int) -> int:
	return value

def absolute_indexed(value: int, register: int) -> int:
	return value + register

def immediate(value: int) -> int:
	return value

def implied(value: int) -> int:
	return value

def indirect(value: int) -> int:
	return value

def x_indexed_indirect(value: int, x_register: int) -> int:
	return value

def indirect_y_indexed(value: int, y_register: int) -> int:
	return value

def relative(value: int) -> int:
	return value

def zero_page(value: int) -> int:
	""" Returns the address value translated and validated """
	if 0x0 > value < 0xFF:
		raise Exception("Invalid address value")

	return value

def zero_page_indexed(value: int, register: int) -> int:
	return value + register