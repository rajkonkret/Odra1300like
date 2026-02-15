class OdraLiteCPU:
    def __init__(self, memory_size=4096):
        self.memory = [0] * memory_size
        self.ACC = 0
        self.IX = 0
        self.PC = 0
        self.FLAG_Z = False
        self.running = True

    def load_program(self, program):
        for i, instruction in enumerate(program):
            self.memory[i] = instruction

    def fetch(self):
        instruction = self.memory[self.PC]
        self.PC += 1
        return instruction

    def decode_execute(self, instruction):
        opcode = (instruction >> 16) & 0xFF
        operand = instruction & 0xFFFF

        if opcode == 0x01:  # LOAD
            self.ACC = self.memory[operand]

        elif opcode == 0x02:  # STORE
            self.memory[operand] = self.ACC

        elif opcode == 0x03:  # ADD
            self.ACC += self.memory[operand]

        elif opcode == 0x04:  # SUB
            self.ACC -= self.memory[operand]

        elif opcode == 0x05:  # JMP
            self.PC = operand

        elif opcode == 0x06:  # JZ
            if self.ACC == 0:
                self.PC = operand

        elif opcode == 0x07:  # LOADIX
            self.IX = self.memory[operand]

        elif opcode == 0x08:  # LOADX
            self.ACC = self.memory[operand + self.IX]

        elif opcode == 0xFF:  # HALT
            self.running = False

        # 24-bit overflow
        self.ACC &= 0xFFFFFF

        self.FLAG_Z = (self.ACC == 0)

    def run(self):
        while self.running:
            instr = self.fetch()
            self.decode_execute(instr)

def instr(opcode, operand=0):
    return (opcode << 16) | operand

print("Start Odra 1300")
cpu = OdraLiteCPU()

cpu.memory[100] = 7
cpu.memory[101] = 5

program = [
    instr(0x01, 100),  # LOAD 100
    instr(0x03, 101),  # ADD 101
    instr(0x02, 102),  # STORE 102
    instr(0xFF)        # HALT
]

cpu.load_program(program)
cpu.run()

print("Wynik:", cpu.memory[102])