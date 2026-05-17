
from cpu import FLAGS, OP_CODES, Memory
from cpu.addressing import *
from cpu.test import TEST_VALUE
from cpu.unit import CPU

def test_zero_page():
	value = TEST_VALUE
	loc: int = 0x10
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.STA_ZP.value,
		0x0003: loc
	}

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.__read__(loc % 0x0100, mem=mem) == value

def test_zero_page_indexed():
	value = TEST_VALUE
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

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.__read__((index + x_value) % 0x0100, mem=mem) == value
		assert cpu.__read__((index + y_value) % 0x0100, mem=mem) == x_value
		assert cpu.__read__((index + 1 + x_value) % 0x0100, mem=mem) == y_value

def test_indirect():
	value = TEST_VALUE
	ll = 0x34
	hh = 0x12
	mem = {
		0x1234: value
	}

	with CPU() as cpu:
		cpu.__write__(ll, 0x0000, mem=mem)
		cpu.__write__(hh, 0x0001, mem=mem)
		assert cpu.__read__(convert_to_absolute_address(ll, hh), mem=mem) == value

def test_absolute():
	value = TEST_VALUE
	ll = 0x34
	hh = 0x12
	addr = convert_to_absolute_address(ll, hh)
	mem: Memory = {
		0x0000: OP_CODES.ASL_ABS.value,
		0x0001: ll,
		0x0002: hh,
		addr: value
	}

	with CPU() as cpu:
		cpu.execute(mem)
		assert mem[addr] == (value << 1) % 0x0100
		assert cpu.status[FLAGS.C] == (value > 0x80)

def test_absolute_indexed():
	value = TEST_VALUE
	and_value = 0x96
	ll = 0x34
	hh = 0x12
	addr = convert_to_absolute_address(ll, hh)
	x_value = 0x10
	y_value = 0x20
	mem: Memory = {
		0x0000: OP_CODES.LDX_IM.value,
		0x0001: x_value,
		0x0002: OP_CODES.LDY_IM.value,
		0x0003: y_value,
		0x0004: OP_CODES.LDA_IM.value,
		0x0005: value,
		0x0006: OP_CODES.AND_ABS_IDX_X.value,
		0x0007: ll,
		0x0008: hh,
		0x0009: OP_CODES.AND_ABS_IDX_Y.value,
		0x000A: ll,
		0x000B: hh,
		addr + x_value: and_value,
		addr + y_value: and_value
	}

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.A == (value & and_value) & and_value

def test_pre_indexed_indirect():
	value = TEST_VALUE
	or_value = 0x96
	x_value = 0x10
	ll = 0x34
	hh = 0x12

	index = 0x40
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.LDX_IM.value,
		0x0003: x_value,
		0x0004: OP_CODES.ORA_IDX_X.value,
		0x0005: index,
		(index + x_value): ll,
		(index + x_value + 1): hh,
		convert_to_absolute_address(ll, hh): or_value
	}

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.A == value | or_value

def test_post_indexed_indirect():
	value = TEST_VALUE
	or_value = 0x96
	y_value = 0x10
	ll = 0x34
	hh = 0x12

	index = 0x40
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.LDY_IM.value,
		0x0003: y_value,
		0x0004: OP_CODES.ORA_IDX_Y.value,
		0x0005: index,
		index: ll,
		index + 1: hh,
		convert_to_absolute_address(ll, hh) + y_value: or_value
	}

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.A == value | or_value