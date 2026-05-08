from typing import Any

MEMORY_MIN_ADDRESS, MEMORY_MAX_ADDRESS = 0x0000, 0xFFFF

"""
Typing to keep consistency for instruction sets
"""
type Instruction = dict[str, Any]

type InstructionSet = dict[int, Instruction]

type tmp = dict[int, function]

"""
Found a site with docs on the instruction set of the 6502 CPU chip form the inspiration video since the web page they were using no longer works

https://www.masswerk.at/6502/6502_instruction_set.html
"""


""" The instructions recognized by this CPU """
INS_SET: InstructionSet = {
	0x00: {
		"label": "BRK",
		"bytes": 1,
		"cycles": 7,
	},
	0xA9: {
		"label": "LDA",
		"bytes": 2,
		"cycles": 2,
	},
	0xA2: {
		"label": "LDX",
		"bytes": 2,
		"cycles": 2
	},
	0xA0: {
		"label": "LDY",
		"bytes": 2,
		"cycles": 2
	},
	0xEA: {
		"label": "NOP",
		"bytes": 1,
		"cycles": 1
	},
}

