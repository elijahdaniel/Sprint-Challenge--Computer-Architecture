import sys


class CPU:

    def __init__(self):
        self.running = True
        self.ram = [0] * 256
        self.registers = [0] * 8
        self.registers[7] = 0xF4
        self.pc = 0  # program counter
        self.fl = 0  # flags status
        self.ir = 0  # instruction register

        # Commands
        self.branchtable = {}
        self.branchtable[0b00000001] = self.HLT
        self.branchtable[0b10000010] = self.LDI
        self.branchtable[0b01000111] = self.PRN
        self.branchtable[0b10100010] = self.MUL
        self.branchtable[0b01000101] = self.PUSH
        self.branchtable[0b01000110] = self.POP

        # self.HLT = 0b00000001  # HALT, exit the emulator
        # self.LDI = 0b10000010  # LOAD, sets a value to a specified register
        # self.PRN = 0b01000111  # PRINT, prints value of a register
        # self.MUL = 0b10100010  # MULTIPLY

    def HLT(self):
        self.running = False

    def LDI(self):
        reg_index = self.ram[self.pc + 1]
        value_to_save = self.ram[self.pc + 2]
        self.registers[reg_index] = value_to_save
        self.pc += 1 + (self.ir >> 6)

    def PRN(self):
        reg_index = self.ram[self.pc + 1]
        print(self.registers[reg_index])
        self.pc += 1 + (self.ir >> 6)

    def MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('MUL', operand_a, operand_b)
        self.pc += 1 + (self.ir >> 6)

    def PUSH(self):
        self.registers[7] -= 1
        sp = self.registers[7]
        reg_index = self.ram[self.pc+1]
        value = self.registers[reg_index]
        self.ram[sp] = value
        self.pc += 1 + (self.ir >> 6)

    def POP(self):
        sp = self.registers[7]
        value = self.ram[sp]
        reg_index = self.ram[self.pc + 1]
        self.registers[reg_index] = value
        self.registers[7] += 1
        self.pc += 1 + (self.ir >> 6)

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, value, index):
        self.ram[index] = value

    def load(self):
        """Load a program into memory."""

        address = 0
        program = []

        if len(sys.argv) < 2:
            print("Please pass in a second file.")
            sys.exit()

        file_name = sys.argv[1]

        try:
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()

                    if command == '':
                        continue
                    # after factoring append whatever is left to the program array
                    program.append(int(command, 2))

        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        if op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while self.running:
            self.ir = self.ram_read(self.pc)

            try:
                self.branchtable[self.ir]()

            except KeyError:
                print('Operation does not exist')
                sys.exit()

        # running = True
        # while running:
        #     # read memory at pc, set to instruction register
        #     # this is the same as the memory[pc] array [PRINT_TIM, PRINT_TIM, HALT]
        #     ir = self.ram_read(self.pc)

        #     # look at the following 1 or 2 bytes of memory, stored as variables..why exactly??
        #     operand_a = self.ram_read(self.pc + 1)
        #     operand_b = self.ram_read(self.pc + 2)

        #     # if command = LDI
        #     if ir == self.LDI:
        #         # grab the memory address 1 past the command, here the value is the spot in ram to save the value
        #         #   = memory[pc + 1]
        #         reg_index = self.ram[self.pc + 1]
        #         # Grab value 2 pass the command, this value will get stored in the ram slot above
        #         value_to_save = self.ram[self.pc + 2]
        #         self.registers[reg_index] = value_to_save
        #         # increment program counter enough to pass the command + the slot + the value
        #         self.pc += 2
        #     if ir == self.MUL:
        #         self.registers[self.ram_read(
        #             self.pc + 1)] *= self.registers[self.ram_read(self.pc + 2)]
        #         self.pc += 2
        #     if ir == self.PRN:
        #         reg_index = self.ram[self.pc+1]
        #         print(self.registers[reg_index])
        #         self.pc += 1

        #     if ir == self.HLT:
        #         running = False

        #     self.pc += 1
