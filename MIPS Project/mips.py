class MIPS_Simulator:
    def __init__(self, file_name = None):
        self.registers = {f'$t{i}': 0 for i in range(8)}    # generates $t0-$t7 registers
        self.memory = {}                                    # holds sparse memory locations
        self.labels = {}                                    # holds labels and their corresponding line numbers
        self.instructions = []                              # holds instructions to run
        self.file_name = file_name                          # holds file name that is being parsed
        self.current_instruction = 0                        # holds current instruction number for rest of code
    
    # sets file name to be parsed in case not set upon creating object
    def set_file_name(self, file_name):
        self.file_name = file_name

    # parses file into necessary data structures such as arrays for processing
    def parse_file(self):
        with open(self.file_name, 'r') as file:
            current_line = 0
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                if ':' in line:
                    label, instruction = line.split(':', 1)
                    label = label.strip()
                    self.labels[label] = current_line
                    line = instruction.strip()
                    if not line:
                        self.instructions.append(label)
                        continue
                else:
                    self.instructions.append(line)
                current_line += 1

    # processes instruction and runs necessary operation
    def execute_instruction(self, instruction):
        label_instruction = []
        parts = []
        if ':' in instruction:
            label_instruction = instruction.split(':', 1)
            parts = label_instruction[1].split()
        else:
            parts = instruction.split()

        operation = parts[0]
        if operation == 'add':
            self.add(parts[1], parts[2], parts[3])
        elif operation == 'sub':
            self.sub(parts[1], parts[2], parts[3])
        elif operation == 'lw':
            self.lw(parts[1], parts[2])
        elif operation == 'sw':
            self.sw(parts[1], parts[2])
        elif operation == 'beq':
            self.beq(parts[1], parts[2], parts[3])
        elif operation == 'bgt':
            self.bgt(parts[1], parts[2], parts[3])
        elif ':' in operation:
            pass
        else:
            print(f'Unknown instruction: {operation}')
        self.current_instruction += 1

    def add(self, dest, src1, src2):
       self.registers[dest] = self.registers[src1] + self.registers[src2]

    def sub(self, dest, src1, src2):
        self.registers[dest] = self.registers[src1] - self.registers[src2]

    # loads word from memory into reg
    def lw(self, dest, src):
        self.registers[dest] = self.memory[src]

    # stores word from reg into memory
    def sw(self, src, dest):
        self.memory[dest] = self.registers[src]

    # branch if equal
    def beq(self, src1, src2, label):
        if self.registers[src1] == self.registers[src2]:
            self.execute_instruction(self.instructions[self.labels[label]])

    # branch if greater than
    def bgt(self, src1, src2, label):
        print("something something bgt")
        if self.registers[src1] > self.registers[src2]:
            self.execute_instruction(self.instructions[self.labels[label]])
            print(f'Jumping to {label}')

    # prints out state of registers for debugging 
    def get_status(self):
        print("Registers:")
        for reg in self.registers: 
            print(f'{reg}: {self.registers[reg]}')
        print(f'Labels: {self.labels}')
        print(f'Instructions: {self.instructions}')
        print(f'Memory: {self.memory}')
        
    # executes the instructions in the given file
    def run(self):
        self.parse_file()
        while self.current_instruction < len(self.instructions):
            instruction = self.instructions[self.current_instruction]
            self.execute_instruction(instruction)
        print(f'Final Register State: {self.registers}')
        print(f'Final Memory State: {self.memory}')
            
if __name__ == "__main__":
    # create mips simulator object
    mips = MIPS_Simulator("example1.txt")

    # initialize register values
    mips.registers["$t2"] = 6
    mips.registers["$t3"] = 4

    # run the simulator/execute instructions in the file fed into the sim
    mips.run()