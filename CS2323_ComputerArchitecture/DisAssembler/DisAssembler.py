import json
# global pc   # program counter
# global lc   # loop counter

def convert_bin(command):
    bin_str = ""
    for i in range(len(command)):
        binary = bin(int(command[i] , 16))
        binary = binary[2:]   # removing 0b prefix
        bin_str += binary.zfill(4) # padding with 0s
    return bin_str

def convert_bin_to_signed(val):
    if val[0] == "1":
        return int(val[1:] , 2) - (2 ** (len(val)-1))
    else:
        return int(val , 2)


def disassemble(command , opt_dict , pc , lc , loop_dict):
    bin_str = convert_bin(command)
    opcode = bin_str[25 :  ]

    if opcode == "0110011":
        type = 'R'
        funct7 = bin_str[ : 7]
        rs2 = bin_str[7 : 12]
        rs1 = bin_str[12 : 17]
        funct3 = bin_str[17 : 20]
        rd = bin_str[20 : 25]
        # two different operations for the same funct3 value
        opt = opt_dict[opcode][funct3][funct7] if funct3 == "000" or funct3 == "101" else opt_dict[opcode][funct3]
        pc += 4
        return type, loop_dict , pc , lc ,   str(pc-4) + ": " + opt + " " + "x" + str(int(rd , 2)) + " , " + "x" + str(int(rs1 , 2)) + " , " + "x" + str(int(rs2 , 2))

    elif opcode == "0010011":
        type = 'I'
        imm = bin_str[ : 12]
        rs1 = bin_str[12 : 17]
        funct3 = bin_str[17 : 20]
        rd = bin_str[20 : 25]
        opt = opt_dict[opcode][funct3][imm[6 : ]] if funct3 == "101" else opt_dict[opcode][funct3]
        pc += 4

        # if slli , srli , slai return str(pc-4) + ": " only part of imm value
        if funct3 == "001" or funct3 == "101":
            return type, loop_dict , pc , lc ,  str(pc-4) + ": " + opt + " " + "x" + str(int(rd , 2)) + " , " + "x" + str(int(rs1 , 2)) + " , "  + str(convert_bin_to_signed(imm[ : 6]))
        else:
            return type, loop_dict , pc , lc , str(pc-4) + ": " + opt + " " + "x" + str(int(rd , 2)) + " , " + "x" + str(int(rs1 , 2)) + " , "  + str(convert_bin_to_signed(imm))

    elif opcode == "0000011":
        type = 'I'
        imm = bin_str[ : 12]
        rs1 = bin_str[12 : 17]
        funct3 = bin_str[17 : 20]
        rd = bin_str[20 : 25]
        opt = opt_dict[opcode][funct3]
        pc += 4
        return type, loop_dict , pc , lc ,  str(pc-4) + ": " + opt + " " + "x" + str(int(rd , 2)) + " , " + str(convert_bin_to_signed(imm)) + "(x" + str(int(rs1 , 2)) + ")"  

    elif opcode == "0100011":
        type = 'S'
        rs2 = bin_str[7 : 12]
        rs1 = bin_str[12 : 17]
        imm = (bin_str[ : 7] + bin_str[20 : 25])
        funct3 = bin_str[17 : 20]
        opt = opt_dict[opcode][funct3]
        pc += 4
        return type, loop_dict , pc , lc ,  str(pc-4) + ": " + opt + " " + "x" + str(int(rs2 , 2)) + " , " + str(int(imm , 2)) + "(x" + str(int(rs1 , 2)) + ")"  

    elif opcode == "1100011":
        type = 'B'
        rs2 = bin_str[7 : 12]
        rs1 = bin_str[12 : 17]
        funct3 = bin_str[17 : 20]
        imm = bin_str[0] + bin_str[24] + bin_str[1 : 7] + bin_str[20 : 24] + "0"
        opt = opt_dict[opcode][funct3]
        newLoop = False
        if pc + convert_bin_to_signed(imm) not in loop_dict.keys():
            loop_dict[pc + convert_bin_to_signed(imm)] = lc
            lc += 1
            newLoop = True
    
        pc += 4
        if newLoop:
            return type, loop_dict , pc , lc ,  str(pc-4) + ": " + opt + " " + "x" + str(int(rs1 , 2)) + " , " + "x" + str(int(rs2 , 2)) + " , L" + str(lc - 1)
        else:
            return type, loop_dict , pc , lc , str(pc-4) + ": " + opt + " " + "x" + str(int(rs1 , 2)) + " , " + "x" + str(int(rs2 , 2)) + " , L" + str(loop_dict[pc - 4+ convert_bin_to_signed(imm)])

    elif opcode == "1101111":
        type = 'J'
        opt = "jal"
        rd = bin_str[20 : 25]
        imm = bin_str[0] + bin_str[12 : 20] + bin_str[11] + bin_str[1 : 11] + "0"
        newLoop = False
        if pc + convert_bin_to_signed(imm) not in loop_dict.keys():
            loop_dict[pc + convert_bin_to_signed(imm)] = lc
            lc += 1
            newLoop = True
    
        pc += 4
        if newLoop:
            return type, loop_dict , pc , lc ,  str(pc-4) + ": " + opt + " " + "x" + str(int(rd , 2)) + " , L" + str(lc - 1)
        else:
            return type, loop_dict , pc , lc , str(pc-4) + ": " + opt + " " + "x" + str(int(rd , 2)) + " , L" + str(loop_dict[pc - 4 + convert_bin_to_signed(imm)])

    elif opcode == "1100111":  
        type = 'I'
        opt = "jalr" 
        imm = bin_str[ : 12]
        rs1 = bin_str[12 : 17]
        funct3 = bin_str[17 : 20]
        rd = bin_str[20 : 25]
        pc += 4
        return type, loop_dict , pc , lc ,  str(pc-4) + ": " + opt + " " + "x" + str(int(rd , 2)) + " , " + "x" + str(int(rs1 , 2)) + " , " + str(convert_bin_to_signed(imm))

    elif opcode == "0110111":
        type = 'U'
        opt = "lui"
        rd = bin_str[20 : 25]
        imm = hex(int(bin_str[ : 20] , 2))
        pc += 4
        return type, loop_dict , pc , lc ,  str(pc-4) + ": " + opt + " " + "x" + str(int(rd , 2)) + " , " + imm

    else:
        type = 'X'
        return type, loop_dict , pc , lc , "Invalid Command"
def main():

    # loading dictionary containing operations
    dict_name = 'opt_dict.json'    
    with open(dict_name,'r') as json_file:
        opt_dict = json.load(json_file)

    pc = 0  # program counter
    lc = 1  # loop counter
    loop_dict = {}

    # loading commands
    file_name = "input.txt"
    data = []
    disassembled_commands = []

    with open(file_name , "r") as f:
        for line in f:
            data.append(line[: 8]) if line[-1] == '\n' else data.append(line)

    for command in data:
        if command == '\n':
            continue    
        _ , loop_dict , pc , lc , dis = disassemble(command , opt_dict , pc , lc , loop_dict)
        disassembled_commands.append(dis)

    # printing disassembled commands
    pc = 0
    for command in disassembled_commands:
        if pc in loop_dict.keys():
            print("\nL" + str(loop_dict[pc]) + ":")
        print(command)
        pc += 4

if __name__ == '__main__':
   
    main()
