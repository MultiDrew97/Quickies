from typing import TYPE_CHECKING

from cpu import Memory, convert_to_absolute_address

if TYPE_CHECKING:
	from cpu.unit import CPU


# TODO: Change so that the register can be specified and retrieved from the passed cpu instance instead of having to pass the register value as an argument
def absolute(cpu: CPU, mem: Memory, offset: int = 0x00) -> int:
	ll = cpu.fetch(mem)
	hh = cpu.fetch(mem)
	return convert_to_absolute_address(ll, hh) + offset

def indirect(cpu: CPU, mem: Memory) -> int:
	ab = absolute(cpu=cpu, mem=mem)
	ll = cpu.__read__(ab, mem=mem)
	hh = cpu.__read__(ab, mem=mem)
	return convert_to_absolute_address(ll, hh)

# MAYBE: Combine these 2 functions into one like the other index functions?
def pre_indexed_indirect(cpu: CPU, mem: Memory) -> int:
	zp = zero_page(cpu=cpu, mem=mem, offset=cpu.X)
	ll = cpu.__read__(zp, mem=mem)
	hh = cpu.__read__((zp + 1) % 0x0100, mem=mem)
	return convert_to_absolute_address(ll, hh)

def post_indexed_indirect(cpu: CPU, mem: Memory) -> int:
	zp = zero_page(cpu=cpu, mem=mem)
	ll = cpu.__read__(zp, mem=mem)
	hh = cpu.__read__((zp + 1) % 0x0100, mem=mem)
	return convert_to_absolute_address(ll, hh) + cpu.Y

def relative(cpu: CPU, mem: Memory) -> int:
	value = cpu.fetch(mem)
	return cpu.PC + value

def zero_page(cpu: CPU, mem: Memory, offset: int = 0x00) -> int:
	value = cpu.fetch(mem)
	return (value + offset) % 0x0100