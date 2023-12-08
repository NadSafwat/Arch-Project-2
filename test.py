import re

def is_valid_instruction(instruction):
    if (instruction[0:4] == "load" or instruction[0:5] == "store"):
       instruction_pattern = re.compile(r'(load|store)r[0-7],[0-9]+\(r[0-7]\)$')
    elif(instruction[0:3] == "bne"):
        instruction_pattern = re.compile(r'bner[0-7],r[0-7],[0-9]+$')
    elif(instruction[0:4] == "call"):
        instruction_pattern = re.compile(r'call[0-9]+$')
    elif(instruction[0:3] == "ret"):
        instruction_pattern = re.compile(r'ret$')
    elif(instruction[0:4] == "addi"):
        instruction_pattern = re.compile(r'addir[0-7],r[0-7],[0-9]+$')
    elif(instruction[0:3] == "add" or instruction[0:4] == "nand" or instruction[0:3] == "div"):
        instruction_pattern = re.compile(r'(add|nand|div)r[0-7],r[0-7],r[0-7]$')

    
    return bool(instruction_pattern.match(instruction))

def getUserInpt():
    instructions_to_run=[]
    print("Available instructions are: \nload rA, offset(rB) \nstore rA, offset(rB) \nbne rA, rB, offset \ncall label \nret \nadd rA, rB, rC \naddi rA, rB, imm \nnand rA, rB, rC \ndiv rA, rB, rC")
    print("Please enter your instructions one by one")
    while(True):
        userInst = input(": ").lower().replace(" ","")
        if (userInst == 0):
            return instructions_to_run
        else:
            if(is_valid_instruction(userInst)==False):
                print("Invalid instruction")
            else:
                if(userInst[0:4] == "load"):
                    userInstList = [userInst[0:4], userInst[4:6], userInst[7:userInst.index('(')], userInst[userInst.index('(')+1:userInst.index('(')+3]]
                elif(userInst[0:5] == "store"):
                    userInstList = [userInst[0:5], userInst[5:7], userInst[8:userInst.index('(')], userInst[userInst.index('(')+1:userInst.index('(')+3]]
                elif(userInst[0:4] == "nand" or userInst[0:4] == "addi"):
                    userInstList = [userInst[0:4], userInst[4:6], userInst[7:9], userInst[10:]] 
                elif(userInst[0:3] == "bne" or userInst[0:3] == "add" or userInst[0:3] == "div"):
                    userInstList = [userInst[0:3], userInst[3:5], userInst[6:8], userInst[9:]]
                elif(userInst[0:4] == "call"):
                    userInstList = [userInst[0:4], userInst[4:], None, None]
                elif(userInst[0:3] == "ret"):
                    userInstList = [userInst[0:3], None, None, None]
                instructions_to_run.append(userInstList)
        
          
getUserInpt()

