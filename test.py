import re

LOAD1 = {"Name" : "Load1" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}
LOAD2 = {"Name" : "Load2" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}
STORE1 = {"Name" : "Store1" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}
STORE2 = {"Name" : "Store2" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}
ADD_ADDI1 = {"Name" : "Add/Addi_1" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}
ADD_ADDI2 = {"Name" : "Add/Addi_2" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}
ADD_ADDI3 = {"Name" : "Add/Addi_3" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}
NAND = {"Name" : "Nand" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}
DIV = {"Name" : "Div" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}
BNE = {"Name" : "Bne" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}
CALL_RET = {"Name" : "Call/Ret" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None, "Imm":None}

ReservationStation = [LOAD1, LOAD2, STORE1, STORE2, ADD_ADDI1, ADD_ADDI2, ADD_ADDI3, NAND, DIV, BNE, CALL_RET]

mem = [0,3,5,5,6,7,8,9,96,3,2,5]

inst_RS = []
exec_time = []

# for reg/Qi table at the bottom of every slide
RegisterStat = {       
    "r0": None,
    "r1": None,
    "r2": None,
    "r3": None,
    "r4": None,
    "r5": None,
    "r6": None,
    "r7": None,
    "r8": None
}


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

def canIssue(Inst):
    if(Inst[0] == "load"):
        if(LOAD1["Busy"] == 'N'):
            return True, ReservationStation[0]
        elif(LOAD2["Busy"] == "N"):
            return True, ReservationStation[1]
        else:
            return False, None
        
    if(Inst[0] == "add" or Inst[0] == "addi"):
        if(ADD_ADDI1["Busy"] == 'N'):
            return True, ReservationStation[4]
        elif(ADD_ADDI2["Busy"] == "N"):
            return True, ReservationStation[5]
        elif(ADD_ADDI3["Busy"] == "N"):
            return True, ReservationStation[6]
        else:
            return False,None
    
    if(Inst[0] == "store"):
        if(STORE1["Busy"] == 'N'):
            return True, ReservationStation[2]
        elif(STORE2["Busy"] == "N"):
            return True, ReservationStation[3]
        else:
            return False,None
    
    if(Inst[0] == "nand"):
        if(NAND["Busy"] == 'N'):
            return True, ReservationStation[7]
        else:
            return False,None
    
    if(Inst[0] == "div"):
        if(DIV["Busy"] == 'N'):
            return True, ReservationStation[8]
        else:
            return False,None
    
    if(Inst[0] == "bne"):
        if(BNE["Busy"] == 'N'):
            return True, ReservationStation[9]
        else:
            return False,None
    if(Inst[0] == "call" or Inst[0] == "ret"):
        if(CALL_RET["Busy"] == 'N'):
            return True, ReservationStation[10]
        else:
            return False,None

def issue(Inst, PC):
    if(Inst[0] == "load"):
        if(canIssue(Inst)[0] == True ):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = Reg[Inst[3]]
            station["Vk"] = None
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = int(Inst[2])
            station["Imm"] = None
            
            if(RegisterStat[Inst[3]] != None):       #CHECK FOR RAW
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[3]] 
        
            RegisterStat[Inst[1]] = station["Name"]
            inst_RS.append(station)
            exec_time.append(0)
            return True
        else:
            return False
    
    elif(Inst[0] == "store"):
        if(canIssue(Inst)[0] == True ):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = Reg[Inst[1]]
            station["Vk"] = Reg[Inst[3]]
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = int(Inst[2])
            station["Imm"] = None
            
            if(RegisterStat[Inst[3]] != None):       #CHECK FOR RAW
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[1]] 

            if(RegisterStat[Inst[1]] != None):      #CHECK FOR RAW
                station["Vk"] = None
                station["Qk"] = RegisterStat[Inst[3]]

            inst_RS.append(station)
            exec_time.append(0)
            return True
        else:
            return False         

    elif(Inst[0] == "add" or Inst[0] == "nand" or Inst[0] == "div"):
        if(canIssue(Inst)[0] == True):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = Reg[Inst[2]]
            station["Vk"] = Reg[Inst[3]]
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = None
            station["Imm"] = None

            if(RegisterStat[Inst[2]] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[2]]           
            
            if(RegisterStat[Inst[3]] != None):
                station["Vk"] = None
                station["Qk"] = RegisterStat[Inst[3]]

            RegisterStat[Inst[1]] = station["Name"]
            inst_RS.append(station) 
            exec_time.append(0)
            return True
        else:
            return False                 

    elif(Inst[0] == "addi"):
        if(canIssue(Inst)[0] == True):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = Reg[Inst[2]]
            station["Vk"] = None
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = None
            station["Imm"] = int(Inst[3])

            if(RegisterStat[Inst[2]] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[2]]

            RegisterStat[Inst[1]] = station["Name"]
            inst_RS.append(station)
            exec_time.append(0)
            return True
        else:
            return False

    elif(Inst[0] == "bne"):
        if(canIssue(Inst)[0]==True):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = Reg[Inst[1]]
            station["Vk"] = Reg[Inst[2]]
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = int(Inst[3])
            station["Imm"] = PC

            if(RegisterStat[Inst[1]] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[1]]
            if(RegisterStat[Inst[2]] != None):
                station["Vk"] = None
                station["Qk"] = RegisterStat[Inst[2]]
            
            inst_RS.append(station)
            exec_time.append(0)
            return True
        else:
            return False

    elif(Inst[0]=="call"):
        if(canIssue(Inst)[0] == True):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = None
            station["Vk"] = None
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = int(Inst[1])
            station["Imm"] = PC

            RegisterStat["r1"] = station["Name"]
            inst_RS.append(station)
            exec_time.append(0)
            return True
        else:
            return False

    elif(Inst[0]=="ret"):
        if(canIssue(Inst)[0] == True):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = "r1"
            station["Vk"] = None
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = int(Reg["r1"])

            if(RegisterStat["r1"] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat["r1"]
            inst_RS.append(station)
            exec_time.append(0)
            return True
        else:
            return False

# for testing the function only
Reg = {
    "r0": 0,
    "r1": 1,
    "r2": 10,
    "r3": 19,
    "r4": 20,
    "r5": 30,
    "r6": 40,
    "r7": 7,
    "r8": 50
}

#example in the recordings for now
instructions = [["load", "r6", "0", "r2"],
                ["load", "r2", "1", "r2"], 
                ["div","r0","r2","r4"], 
                ["add", "r8","r2","r6"], 
                ["div","r7","r0","r6"],
                ["add", "r6", "r1","r5"] , 
                ["addi", "r1", "r1", "1"], 
                ["add", "r6", "r1","r5"]]

def issue_test(instruction_list):
    i=1
    for Inst in instruction_list:
        if(canIssue(Inst)[0] == True):
            issue(Inst)
            print("======================================")
            print(i, RegisterStat)
        elif(canIssue(Inst)[0] == False):
            print("Instruction cannot be issued")
        i+=1
    print("******************************")
    print(ReservationStation)

def canExecute(station, count):
    if(station["OP"] == "load"):
        if(station["Qj"] is None and count < 3):
            return True
        else:
            return False

    elif(station["OP"] == "store"):
        if(station["Qj"] is None and station["Qk"] is None and count < 3):
            return True
        else:
            return False         
    elif(station["OP"] == "add"):
        if(station["Qj"] is None and station["Qk"] is None and count < 2):
            return True
        else:
            return False
    elif (station["OP"] == "nand"):
        if(station["Qj"] is None and station["Qk"] is None and count < 1):
            return True
        else:
            return False
 
    elif(station["OP"] == "div"): 
        if(station["Qj"] is None and station["Qk"] is None and count < 10):
            return True
        else:
            return False 
    
    elif(station["OP"] == "bne"): 
        if(station["Qj"] is None and station["Qk"] is None and count < 1):
            return True
        else:
            return False
       
    elif( station["OP"] == "addi"):
        if( station["Qj"] is None and count < 2):
            return True
        else:
            return False
    
    elif(station["OP"] == "call"):
        return (count < 1) 
    
    elif(station["OP"] == "ret"):
        if(station["Qj"] is None and count < 1):
            return True
        else:
            return False    

def Execute(Inst, station, count):
    if(station["OP"] == "load"):
        if (count == 1):
            station["A"] = station["Vj"] + station["A"]
        elif (count == 2):
            Reg[Inst[1]] = mem[station["A"]]
        return(count+1)

    elif(station["OP"] == "store"):
        if (count == 1):
            station["A"] = station["Vk"] + station["A"]
        elif (count == 2):
            mem[station["A"]] = station["Vj"]
        return(count+1) 
    
    elif(station["OP"] == "add"):
        if (count == 1):
            Reg[Inst[1]] = station["Vj"]+station["Vk"]
        return(count+1)
    
    elif(station["OP"] == "nand"):
        Reg[Inst[1]] = ~(station["Vj"] & station["Vk"])
        return(count+1)
    
    elif( station["OP"] == "addi"):
        if (count == 1):
            Reg[Inst[1]] = station["Vj"]+station["Imm"]
        return(count+1)
    
    elif(station["OP"] == "div"):
        if (count == 9):
            Reg[Inst[1]] = station["Vj"]/station["Vk"]
        return(count+1)

    elif(station["OP"] == "bne"):
        if(station["Vj"] != station["Vk"]):
            station["A"] =  station["Imm"] + station["A"] + 1
        return(count+1)
   
    elif(station["OP"] == "call"):
        Reg["r1"] = station["Imm"]+1
        return(count+1)
    
    elif(station["OP"] == "ret"):
        return(count+1)

def simulate(clk, PC):
    if(clk != 0):
        for j in range(len(inst_RS)):
            if(canExecute(inst_RS[j], exec_time[j])):
                print("Executed Instruction ", j, " ", exec_time[j], " cycles")
                exec_time[j] = Execute(instructions[j], inst_RS[j], exec_time[j])

    if(issue(instructions[PC], PC)):
        print("Issued Inst ", PC)
        return(PC + 1)
        
    

def top ():
    clk = 0
    PC = 0
   
    while(True):
        go = input()
        if(go):
            PC = simulate(clk, PC)
            clk += 1

top()