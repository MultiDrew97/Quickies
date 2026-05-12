from cpu import FLAGS, OP_CODES, Memory
from cpu.addressing import absolute, zero_page
from cpu.unit import CPU

def test_brk():
	mem: Memory = {
		0x0000: OP_CODES.BRK.value
	}
	with CPU() as cpu:
		assert cpu.status[FLAGS.B] == False
		cpu.execute(mem)
		assert cpu.status[FLAGS.B] == True

def test_ora_idx_x():
	value = 0x69
	or_vaue = 0x96
	x_value = 0x10
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.LDX_IM.value,
		0x0003: x_value,
		0x0004: OP_CODES.ORA_IDX_X.value,
		0x0005: 0x00,
		0x0010: 0x15,
		0x0011: 0x20,
		0x2015: or_vaue
	}

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.A == value | or_vaue
		assert cpu.X == x_value

def test_ora_zp():
	value = 0x69
	or_vaue = 0x96
	loc: int = 0x10
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.ORA_ZP.value,
		0x0003: loc,
		loc: or_vaue
	}

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.A == value | or_vaue

def test_asl_zp():
	zp_loc = 0x10
	value = 0xFF
	mem: Memory = {
		0x0000: OP_CODES.ASL_ZP.value,
		0x0001: zp_loc,
		zp_loc: value,
	}

	with CPU() as cpu:
		assert cpu.status[FLAGS.C] == False
		cpu.execute(mem)
		assert cpu.__read__(zp_loc, mem=mem) == (value << 1) % 0x100
		assert cpu.status[FLAGS.C] == True

def test_php():
	mem: Memory = {
		0x0000: OP_CODES.PHP.value,
	}

	with CPU() as cpu:
		sp_start = cpu.SP
		cpu.status[FLAGS.N] = True
		cpu.status[FLAGS.V] = True
		cpu.status[FLAGS.B] = False
		cpu.status[FLAGS.D] = True
		cpu.status[FLAGS.I] = True
		cpu.status[FLAGS.Z] = True
		cpu.status[FLAGS.C] = True

		cpu.execute(mem)
		loc = 0x0100 + zero_page(cpu.SP + 1) # Stack pointer is decremented after writing to stack
		assert cpu.__read__(loc, mem=mem)  == 0b11001111
		assert cpu.SP == sp_start - 1

def test_ora_im():
	value = 0x69
	or_vaue = 0x96
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.ORA_IM.value,
		0x0003: or_vaue,
	}

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.A == value | or_vaue

def test_asl():
	value = 0xFF
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.ASL.value,
	}

	with CPU() as cpu:
		assert cpu.status[FLAGS.C] == False
		cpu.execute(mem)
		assert cpu.A == (value << 1) % 0x100
		assert cpu.status[FLAGS.C] == True

def test_ora_abs():
	value = 0x69
	or_vaue = 0x96
	ll = 0x15
	hh = 0x20
	loc: int = absolute(ll, hh)
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.ORA_ABS.value,
		0x0003: ll,
		0x0004: hh,
		loc: or_vaue
	}

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.A == value | or_vaue

def test_asl_abs():
	value = 0xFF
	ll = 0x15
	hh = 0x20
	loc: int = absolute(ll, hh)
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.ASL_ABS.value,
		0x0003: ll,
		0x0004: hh,
		loc: value
	}

	with CPU() as cpu:
		assert cpu.status[FLAGS.C] == False
		cpu.execute(mem)
		assert cpu.__read__(loc, mem=mem) == (value << 1) % 0x100
		assert cpu.status[FLAGS.C] == True

def test_bpl():
	value = 0x69
	or_vaue = 0x96
	ll = 0x15
	hh = 0x20
	loc: int = absolute(ll, hh)
	mem: Memory = {
		0x0000: OP_CODES.LDA_IM.value,
		0x0001: value,
		0x0002: OP_CODES.BPL.value,
		0x0003: 0xF5, # Relative jump of 5 bytes
		0x0004: OP_CODES.ORA_ABS.value,
		0x0005: ll,
		0x0006: hh,
		loc: or_vaue
	}

	with CPU() as cpu:
		cpu.execute(mem)
		assert cpu.A != value | or_vaue