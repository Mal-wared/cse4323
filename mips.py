class MIPS_Simulator:
    def __init__(self, file_name = None):
        self.registers = {f'$t{i}': 0 for i in range(8)}
        self.memory = {}
        self.labels = {}
        self.instructions = []
        self.file_name = file_name
    
    def set_file_name(self, file_name):
        self.file_name = file_name

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
                        continue

                self.instructions.append(line)
                current_line += 1

    def execute_instruction(self, instruction):
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
        else:
            print(f'Unknown instruction: {operation}')

    def add(self, dest, src1, src2):
       self.registers[dest] = self.registers[src1] + self.registers[src2]

    def sub(self, dest, src1, src2):
        self.registers[dest] = self.registers[src1] - self.registers[src2]

    def lw(self, dest, src):
        self.registers[dest] = self.memory[self.registers[src]]

    def sw(self, src, dest):
        self.memory[self.registers[dest]] = self.registers[src]

    def beq(self, src1, src2, label):
        if self.registers[src1] == self.registers[src2]:
            self.execute_instruction(self.instructions[self.labels[label]])
    
    def bgt(self, src1, src2, label):
        if self.registers[src1] > self.registers[src2]:
            self.execute_instruction(self.instructions[self.labels[label]])

    def get_status(self):
        print("Registers:")
        for reg in self.registers: 
            print(f'{reg}: {self.registers[reg]}')
        print(f'Labels: {self.labels}')
        print(f'Instructions: {self.instructions}')

    def run(self):
        self.parse_file()
        for instruction in self.instructions :
            self.execute_instruction(instruction)
            self.get_status()
        

if __name__ == "__main__":
    mips = MIPS_Simulator("example1.txt")
    mips.registers["$t2"] = 6
    mips.registers["$t3"] = 4
    mips.get_status()
    mips.run()