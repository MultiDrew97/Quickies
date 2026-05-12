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
	# _=5 Ignored bit
	B=4
	D=3
	I=2
	Z=1
	C=0

# OP Codes
class OP_CODES(Enum):
	BRK = 0x00
	ORA_IDX_X= 0x01
	ORA_ZP = 0x05
	ASL_ZP = 0x06
	PHP = 0x08
	ORA_IM = 0x09
	ASL = 0x0A
	ORA_ABS = 0x0D
	ASL_ABS = 0x0E
	BPL = 0x10
	ORA_IDX_Y = 0x11
	ORA_ZP_IDX_X = 0x15
	ASL_ZP_IDX = 0x16
	CLC = 0x18
	ORA_ABS_IDX_Y = 0x19
	ORA_ABS_IDX_X = 0x1D
	ASL_ABS_IDX = 0x1E
	JSR_ABS = 0x20
	AND_IDX_X = 0x21
	BIT_ZP = 0x24
	AND_ZP = 0x25
	ROL_ZP = 0x26
	PLP = 0x28
	AND_IM = 0x29
	ROL = 0x2A
	BIT_ABS = 0x2C
	AND_ABS = 0x2D
	ROL_ABS = 0x2E
	BMI = 0x30
	AND_IDX_Y = 0x31
	AND_ZP_IDX_X = 0x35
	ROL_ZP_IDX = 0x36
	SEC = 0x38
	AND_ABS_IDX_Y = 0x39
	AND_ABS_IDX_X = 0x3D
	ROL_ABS_IDX = 0x3E
	RTI = 0x40
	EOR_IDX_X = 0x41
	EOR_ZP = 0x45
	LSR_ZP = 0x46
	PHA = 0x48
	EOR_IM = 0x49
	LSR = 0x4A
	JMP_ABS = 0x4C
	EOR_ABS = 0x4D
	LSR_ABS = 0x4E
	BVC = 0x50
	EOR_IDX_Y = 0x51
	EOR_ZP_IDX_X = 0x55
	LSR_ZP_IDX = 0x56
	CLI = 0x58
	EOR_ABS_IDX_Y = 0x59
	EOR_ABS_IDX_X = 0x5D
	LSR_ABS_IDX = 0x5E
	RTS = 0x60
	ADC_IDX_X = 0x61
	ADC_ZP = 0x65
	ROR_ZP = 0x66
	PLA = 0x68
	ADC_IM = 0x69
	ROR = 0x6A
	JMP_IND = 0x6C
	ADC_ABS = 0x6D
	ROR_ABS = 0x6E
	BVS = 0x70
	ADC_IDX_Y = 0x71
	ADC_ZP_IDX_X = 0x75
	ROR_ZP_IDX = 0x76
	SEI = 0x78
	ADC_ABS_IDX_Y = 0x79
	ADC_ABS_IDX_X = 0x7D
	ROR_ABS_IDX = 0x7E
	STA_IDX_X = 0x81
	STY_ZP = 0x84
	STA_ZP = 0x85
	STX_ZP = 0x86
	DEY = 0x88
	TXA = 0x8A
	STY_ABS = 0x8C
	STA_ABS = 0x8D
	STX_ABS = 0x8E
	BCC = 0x90
	STA_IDX_Y = 0x91
	STY_ZP_IDX = 0x94
	STA_ZP_IDX = 0x95
	STX_ZP_IDX = 0x96
	TYA = 0x98
	STA_ABS_IDX_Y = 0x99
	TXS = 0x9A
	STA_ABS_IDX_X = 0x9D
	LDY_IM = 0xA0
	LDA_IDX_X = 0xA1
	LDX_IM = 0xA2
	LDY_ZP = 0xA4
	LDA_ZP = 0xA5
	LDX_ZP = 0xA6
	TAY = 0xA8
	LDA_IM = 0xA9
	TAX = 0xAA
	LDY_ABS = 0xAC
	LDA_ABS = 0xAD
	LDX_ABS = 0xAE
	BCS = 0xB0
	LDA_IDX_Y = 0xB1
	LDY_ZP_IDX = 0xB4
	LDA_ZP_IDX = 0xB5
	LDX_ZP_IDX = 0xB6
	CLV = 0xB8
	LDA_ABS_IDX_Y = 0xB9
	TSX = 0xBA
	LDY_ABS_IDX = 0xBC
	LDA_ABS_IDX_X = 0xBD
	LDX_ABS_IDX = 0xBE
	CPY_IM = 0xC0
	CMP_IDX_X = 0xC1
	CPY_ZP = 0xC4
	CMP_ZP = 0xC5
	DEC_ZP = 0xC6
	INY = 0xC8
	CMP_IM = 0xC9
	DEX = 0xCA
	CPY_ABS = 0xCC
	CMP_ABS = 0xCD
	DEC_ABS = 0xCE
	BNE = 0xD0
	CMP_IDX_Y = 0xD1
	CMP_ZP_IDX_X = 0xD5
	DEC_ZP_IDX = 0xD6
	CLD = 0xD8
	CMP_ABS_IDX_Y = 0xD9
	CMP_ABS_IDX_X = 0xDD
	DEC_ABS_IDX = 0xDE
	CPX_IM = 0xE0
	SBC_IDX_X = 0xE1
	CPX_ZP = 0xE4
	SBC_ZP = 0xE5
	INC_ZP = 0xE6
	INX = 0xE8
	SBC_IM = 0xE9
	NOP = 0xEA
	CPX_ABS = 0xEC
	SBC_ABS = 0xED
	INC_ABS = 0xEE
	BEQ = 0xF0
	SBC_IDX_Y = 0xF1
	SBC_ZP_IDX_X = 0xF5
	INC_ZP_IDX = 0xF6
	SED = 0xF8
	SBC_ABS_IDX_Y = 0xF9
	SBC_ABS_IDX_X = 0xFD
	INC_ABS_IDX = 0xFE

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
	},
	OP_CODES.LDA_ZP_IDX: {
		"name": "LDA",
		"bytes": 2,
		"cycles": 4
	},
	OP_CODES.LDX_ZP_IDX: {
		"name": "LDX",
		"bytes": 2,
		"cycles": 4
	},
	OP_CODES.LDY_ZP_IDX: {
		"name": "LDY",
		"bytes": 2,
		"cycles": 4
	}
}

