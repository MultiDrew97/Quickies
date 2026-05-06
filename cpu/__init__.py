from typing import Literal, Tuple


MEMORY_MIN_ADDRESS, MEMORY_MAX_ADDRESS = 0x0000, 0xFFFF

"""
Typing to keep consistency for instruction sets

Instruction = (OpCode (0x####), params (int))
"""
type Instruction = Tuple[int, int]

type InstructionSet = dict[str, Instruction]


"""

Found a site with docs on the instruction set of the 6502 CPU chip form the inspiration video since the web page they were using no longer works

https://www.masswerk.at/6502/6502_instruction_set.html
"""


""" The instructions recognized by this CPU """
INS_SET: InstructionSet = {
	"LDA": (0xA9, 2),
	"LDX": (0x00, 1),
	"LDY": (0x00, 1)
}

# enum instructions:
INS_LDA_IM: Instruction = (0xA9, 2) # Load mem into accumulator register
INS_LDX_IM: Instruction = (0x00, 2) # Load mem into X register
INS_LDY_IM: Instruction = (0x00, 2) # Load mem into Y register
# LDX: Instruction = 0 # Load mem into X register
# LDY=0 # Load mem into Y register
# STA=0 # Store value of accumulator register into mem
# STX=0 # Store value of X register into mem
# STY=0 # Store value of Y register into mem

