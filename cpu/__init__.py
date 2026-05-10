from enum import Enum
from typing import Any

""" The minimum and maximum values available for memory access """
MEMORY_MIN_ADDRESS, MEMORY_MAX_ADDRESS = 0x0000, 0xFFFF
""" The value to use for a NULL pointer """
NULL_POINTER: int = 0x0

"""
Typing to keep consistency for instruction sets
"""
type Instruction = dict[str, Any]

type InstructionSet = dict[OP_CODES, Instruction]

type Memory = dict[int, int]

"""
Found a site with docs on the instruction set of the 6502 CPU chip form the inspiration video since the web page they were using no longer works

https://www.masswerk.at/6502/6502_instruction_set.html
"""

class FLAGS(Enum):
	N=7
	V=6
	_=5
	B=4
	D=3
	I=2
	Z=1
	C=0

# OP Codes
class OP_CODES(Enum):
	BRK = 0x00
	LDA_IM = 0xA9
	LDA_ZP = 0xA5
	LDA_ZP_IDX = 0xB5
	LDX_IM = 0xA2
	LDX_ZP = 0xA6
	LDX_ZP_IDX = 0xB6
	LDY_IM = 0xA0
	LDY_ZP = 0xA4
	LDY_ZP_IDX = 0xB4
	STA_ZP = 0x85
	STA_ZP_IDX = 0x95
	STX_ZP = 0x86
	STX_ZP_IDX = 0x96
	STY_ZP = 0x84
	STY_ZP_IDX = 0x94
	NOP = 0xEA

""" The instructions recognized by this CPU """
INS_SET: InstructionSet = {
	OP_CODES.BRK: {
		"name": "BRK",
		"bytes": 1,
		"cycles": 7,
	},
	OP_CODES.LDA_IM: {
		"name": "LDA",
		"bytes": 2,
		"cycles": 2,
	},
	OP_CODES.LDX_IM: {
		"name": "LDX",
		"bytes": 2,
		"cycles": 2
	},
	OP_CODES.LDY_IM: {
		"name": "LDY",
		"bytes": 2,
		"cycles": 2
	},
	OP_CODES.NOP: {
		"name": "NOP",
		"bytes": 1,
		"cycles": 1
	},
	OP_CODES.STA_ZP: {
		"name": "STA",
		"bytes": 2,
		"cycles": 2
	},
	OP_CODES.STX_ZP: {
		"name": "STX",
		"bytes": 2,
		"cycles":2
	},
	OP_CODES.STY_ZP: {
		"name": "STY",
		"bytes": 2,
		"cycles":2
	}
}

