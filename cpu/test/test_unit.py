from cpu import FLAGS, MEMORY_MIN_ADDRESS, NULL_POINTER, OP_CODES
from cpu.unit import CPU

def test_init():
	tmp = CPU()
	assert len(tmp.status) == 8 and all(flag == False for flag in tmp.status.values())

def test_reset():
	loc = 0x1234
	value = 0x69
	mem = {
		0x1234: OP_CODES.LDA_IM.value,
		0x1235: value
	}
	with CPU() as cpu:
		cpu.PC = loc
		cpu.execute(mem)
		assert cpu.PC != loc
		assert cpu.A == value

		cpu.reset()

		assert cpu.PC == MEMORY_MIN_ADDRESS
		assert cpu.SP == cpu.A == cpu.X == cpu.Y == NULL_POINTER
		print(cpu.status.values())
		assert len(cpu.status) == 8 and all(flag is False for flag in cpu.status.values())

def test_negative_flag():
	with CPU() as cpu:
		cpu.__set_a__(0xFF)
		assert cpu.status[FLAGS.N] == True

		cpu.__set_a__(0x7F)
		assert cpu.status[FLAGS.N] == False

def test_zero_flag():
	with CPU() as cpu:
		cpu.__set_a__(0x0)
		assert cpu.status[FLAGS.Z] == True

		cpu.__set_a__(0xFF)
		assert cpu.status[FLAGS.Z] == False

def test_overflow_flag():
	with CPU() as cpu:
		assert cpu.status[FLAGS.V] == False

def test_set_a():
	with CPU() as cpu:
		cpu.__set_a__(0x0)
		assert cpu.A == 0x0
		assert cpu.status[FLAGS.Z] == True
		assert cpu.status[FLAGS.N] == False

		cpu.__set_a__(0xFF)
		assert cpu.A == 0xFF
		assert cpu.status[FLAGS.Z] == False
		assert cpu.status[FLAGS.N] == True

		cpu.__set_a__(0x7F)
		assert cpu.A == 0x7F
		assert cpu.status[FLAGS.Z] == False
		assert cpu.status[FLAGS.N] == False

def test_set_x():
	with CPU() as cpu:
		cpu.__set_x__(0x0)
		assert cpu.X == 0x0
		assert cpu.status[FLAGS.Z] == True
		assert cpu.status[FLAGS.N] == False

		cpu.__set_x__(0xFF)
		assert cpu.X == 0xFF
		assert cpu.status[FLAGS.Z] == False
		assert cpu.status[FLAGS.N] == True

		cpu.__set_x__(0x7F)
		assert cpu.X == 0x7F
		assert cpu.status[FLAGS.Z] == False
		assert cpu.status[FLAGS.N] == False

def test_set_y():
	with CPU() as cpu:
		cpu.__set_y__(0x0)
		assert cpu.Y == 0x0
		assert cpu.status[FLAGS.Z] == True
		assert cpu.status[FLAGS.N] == False

		cpu.__set_y__(0xFF)
		assert cpu.Y == 0xFF
		assert cpu.status[FLAGS.Z] == False
		assert cpu.status[FLAGS.N] == True

		cpu.__set_y__(0x7F)
		assert cpu.Y == 0x7F
		assert cpu.status[FLAGS.Z] == False
		assert cpu.status[FLAGS.N] == False

def test_fetch():
	start = 0x0000
	value = 0x69
	mem = {
		0x0000: value
	}

	with CPU() as cpu:
		cpu.PC = start
		assert cpu.fetch(mem) == value
		assert cpu.PC == start + 1