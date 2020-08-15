import sys


class CPU:
    def __init__(self):
        self.running = True
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
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

        # Sprint
        self.branchtable[0b01010000] = self.CALL
        self.branchtable[0b00010001] = self.RET  # return back to address
        self.branchtable[0b10100000] = self.ADD
        self.branchtable[0b10100111] = self.CMP  # compare two values
        self.branchtable[0b01010101] = self.JEQ  # jump if equal
        self.branchtable[0b01010110] = self.JNE  # jump if not equal
        self.branchtable[0b01010100] = self.JMP  # jump to an address

        # self.HLT = 0b00000001  # halt, exit the emulator
        # self.LDI = 0b10000010  # load, sets a value to a specified register
        # self.PRN = 0b01000111  # print, prints value of a register
        # self.MUL = 0b10100010  # multiply

    def AND(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('ADD', self.pc + 1, self.pc + 2)

    def OR(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('ADD', self.pc + 1, self.pc + 2)

    def XOR(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('ADD', self.pc + 1, self.pc + 2)

    def NOT(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('ADD', self.pc + 1, self.pc + 2)

    def SHL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('ADD', self.pc + 1, self.pc + 2)

    def SHR(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('ADD', self.pc + 1, self.pc + 2)

    def MOD(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('ADD', self.pc + 1, self.pc + 2)

    def JEQ(self):
        if self.fl == 1:
            reg_index = self.ram[self.pc + 1]
            next_index = self.reg[reg_index]
            self.pc = next_index
        else:
            self.pc += 1 + (self.ir >> 6)

    def JNE(self):
        if (self.fl & 0b00000001) == 0:
            reg_index = self.ram[self.pc + 1]
            next_index = self.reg[reg_index]
            self.pc = next_index
        else:
            self.pc += 1 + (self.ir >> 6)

    def JMP(self):
        reg_index = self.ram[self.pc + 1]
        next_index = self.reg[reg_index]
        self.pc = next_index

    def CMP(self):
        reg_A = self.ram[self.pc + 1]
        reg_B = self.ram[self.pc + 2]
        self.alu('CMP', reg_A, reg_B)
        self.pc += 1 + (self.ir >> 6)

    def HLT(self):
        self.running = False

    def LDI(self):
        reg_index = self.ram[self.pc + 1]
        value_to_save = self.ram[self.pc + 2]
        self.reg[reg_index] = value_to_save
        self.pc += 1 + (self.ir >> 6)

    def PRN(self):
        reg_index = self.ram[self.pc + 1]
        print(self.reg[reg_index])
        self.pc += 1 + (self.ir >> 6)

    def ADD(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('ADD', operand_a, operand_b)

    def MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu('MUL', operand_a, operand_b)

    def PUSH(self):
        self.reg[7] -= 1
        sp = self.reg[7]
        reg_index = self.ram[self.pc+1]
        value = self.reg[reg_index]
        self.ram[sp] = value

    def POP(self):
        sp = self.reg[7]
        value = self.ram[sp]
        reg_index = self.ram[self.pc + 1]
        self.reg[reg_index] = value
        self.reg[7] += 1

    def CALL(self):
        reg_index = self.ram[self.pc + 1]
        address = self.reg[reg_index]
        return_address = self.pc + 2
        self.reg[7] -= 1
        stack_pointer = self.reg[7]
        self.ram[stack_pointer] = return_address
        self.pc = address

    def RET(self):
        stack_pointer = self.reg[7]
        return_address = self.ram[stack_pointer]
        self.reg[7] += 1
        self.pc = return_address

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

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010

            elif self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100

            else:
                self.fl = 0b00000001

        elif op == "AND":
            result = self.reg[reg_a] & self.reg[reg_b]
            self.reg[reg_a] = result

        elif op == "OR":
            result = self.reg[reg_a] | self.reg[reg_b]
            self.reg[reg_a] = result

        elif op == "XOR":
            result = self.reg[reg_a] ^ self.reg[reg_b]
            self.reg[reg_a] = result

        elif op == "NOT":
            pass

        elif op == "SHL":
            pass

        elif op == "SHR":
            pass

        elif op == "MOD":
            pass

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
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
            # # read memory at pc, set to instruction register
            # # this is the same as the memory[pc] array [PRINT_TIM, PRINT_TIM, HALT]
            self.ir = self.ram_read(self.pc)
            try:
                self.branchtable[self.ir]()
            except KeyError:
                print("Operation does not exist")
                sys.exit()
