from cpu import FLAGS, MEMORY_MIN_ADDRESS, NULL_POINTER, OP_CODES, STACK_START_LOCATION, Memory
from cpu.test import TEST_VALUE
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
		assert cpu.SP == STACK_START_LOCATION
		assert cpu.A == cpu.X == cpu.Y == NULL_POINTER
		print(cpu.status.values())
		assert len(cpu.status) == 8 and all(status is False for status in cpu.status.values())

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

def test_status_to_bytes():
	with CPU() as cpu:
		for f in FLAGS:
			cpu.status[f] = True

		value = cpu.__status_to_byte__()
		assert value == 0b11111111

def test_bytes_to_status():
	value = 0b11011111
	with CPU() as cpu:
		cpu.__byte_to_status__(value)

		for f in FLAGS:
			if f == FLAGS._:
				# Flag in this place is ignored by chip so doesn't need to be checked at this time
				continue

			assert cpu.status[f] == True

def test_read():
	value = TEST_VALUE
	addr = 0x01
	mem: Memory = {
		addr: value
	}
	with CPU() as cpu:
		assert cpu.__read__(addr, mem=mem) == value
		assert cpu.__read__(addr + 1, mem=mem) == 0x00

def test_write():
	value = TEST_VALUE
	addr = 0x01
	mem: Memory = {}
	with CPU() as cpu:
		cpu.__write__(value, address=addr, mem=mem)
		assert mem[addr] == value