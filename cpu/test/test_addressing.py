
from cpu import OP_CODES, Memory
from cpu.addressing import indirect, zero_page, zero_page_indexed
from cpu.unit import CPU

def test_zp():
	value = 0x0
	loc: int = 0x0
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.STA_ZP.value,
		0x0003: loc
	}

	assert zero_page(0xFF) == 0xFF
	assert zero_page(0x01) == 0x01

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.__read__(zero_page(loc), mem=mem) == value

def test_zp_indexed():
	value = 0x69
	x_value = 0x10
	y_value = 0x20
	index: int = 0x08
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.LDX_IM.value,
		0x0003: x_value,
		0x0004: OP_CODES.LDY_IM.value,
		0x0005: y_value,
		0x0006: OP_CODES.STA_ZP_IDX.value,
		0x0007: index,
		0x0008: OP_CODES.STX_ZP_IDX.value,
		0x0009: index,
		0x000A: OP_CODES.STY_ZP_IDX.value,
		0x000B: index + 1
	}

	assert zero_page_indexed(index, register=x_value) == 0x18
	assert zero_page_indexed(index, register=y_value) == 0x28

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.__read__(zero_page_indexed(index, register=x_value), mem=mem) == value
		assert cpu.__read__(zero_page_indexed(index, register=y_value), mem=mem) == x_value
		assert cpu.__read__(zero_page_indexed(index + 1, register=x_value), mem=mem) == y_value

def test_indirect():
	lo = 0x34
	hi = 0x12
	value = 0x69
	mem = {
		0x1234: value
	}
	assert indirect(lo, hi) == 0x1234

	with CPU() as cpu:
		cpu.__write__(lo, 0x0000, mem=mem)
		cpu.__write__(hi, 0x0001, mem=mem)
		assert cpu.__read__(indirect(lo, hi), mem=mem) == value