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
can_write = []
write_queue = []

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

def fix_after_write(functional_unit_name, rd):
    for rs in ReservationStation:
      
        if(rs["Qj"] == functional_unit_name):
            rs["Qj"] = None
            rs["Vj"] = Reg[rd]
        if(rs["Qk"] == functional_unit_name):
            rs["Qk"] = None
            rs["Vk"] = Reg[rd]
          
      

    
    if(rd is not None):
        RegisterStat[rd] = None

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
            
            if(Inst[3] != "r0" and RegisterStat[Inst[3]] != None):       #CHECK FOR RAW
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[3]] 
        
            RegisterStat[Inst[1]] = station["Name"]
            inst_RS.append(station)
            exec_time.append(0)
            can_write.append(0)
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
            
            if(Inst[3] != "r0" and RegisterStat[Inst[3]] != None):       #CHECK FOR RAW
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[3]] 

            if(Inst[1] != "r0" and RegisterStat[Inst[1]] != None):      #CHECK FOR RAW
                station["Vk"] = None
                station["Qk"] = RegisterStat[Inst[1]]

            inst_RS.append(station)
            exec_time.append(0)
            can_write.append(0)
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

            if(Inst[2] != "r0" and RegisterStat[Inst[2]] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[2]]           
            
            if(Inst[3] != "r0" and RegisterStat[Inst[3]] != None):
                station["Vk"] = None
                station["Qk"] = RegisterStat[Inst[3]]

            RegisterStat[Inst[1]] = station["Name"]
            inst_RS.append(station) 
            exec_time.append(0)
            can_write.append(0)
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

            if(Inst[2] != "r0" and RegisterStat[Inst[2]] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[2]]

            RegisterStat[Inst[1]] = station["Name"]
            inst_RS.append(station)
            exec_time.append(0)
            can_write.append(0)
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

            if(Inst[1] != "r0" and RegisterStat[Inst[1]] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[1]]
            if(Inst[2] != "r0" and RegisterStat[Inst[2]] != None):
                station["Vk"] = None
                station["Qk"] = RegisterStat[Inst[2]]
            
            inst_RS.append(station)
            exec_time.append(0)
            can_write.append(0)
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
            can_write.append(0)
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
            can_write.append(0)
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

def removeInst(station):
    station["Busy"] = 'N'
    station["OP"] = None
    station["Vj"] = None
    station["Vk"] = None
    station["Qj"] = None
    station["Qk"] = None
    station["A"] = None
    station["Imm"] = None

    return station
    
def canExecute(j, station, count):
    if(station["OP"] == "load"):
        try:
            if(station["Qj"] is None and count < 3):
                if (count == 1):
                    station["A"] = station["Vj"] + station["A"]
                if(count == 2):
                    can_write[j] = 1
                return (count+1)
            else:
                return count
        except:
            return count

    elif(station["OP"] == "store"):
        try:
            if(station["Qj"] is None and station["Qk"] is None and count < 3):
                if (count == 1):
                    station["A"] = station["Vk"] + station["A"]
                if(count == 2):
                    can_write[j] = 1
                return (count+1)
            else:
                return count
        except:
            return count
                 
    elif(station["OP"] == "add"):
        try:
            if(station["Qj"] is None and station["Qk"] is None and count < 2):
                if(count == 1):
                    can_write[j] = 1
                return (count+1)
            else:
                return count
        except:
            return count
        
    elif (station["OP"] == "nand"):
        try:
            if(station["Qj"] is None and station["Qk"] is None and count < 1):
                can_write[j] = 1
                return (count+1)
            else:
                return count
        except:
            return count
 
    elif(station["OP"] == "div"):
        try: 
            if(station["Qj"] is None and station["Qk"] is None and count < 10):
                if(count == 9):
                    can_write[j] = 1
                return (count+1)
            else:
                return count
        except:
            return count
    
    elif(station["OP"] == "bne"): 
        try:
            if(station["Qj"] is None and station["Qk"] is None and count < 1):
                if(station["Vj"] != station["Vk"]):
                    station["A"] =  station["Imm"] + station["A"] + 1
                can_write[j] = 1
                return (count+1)
            else:
                return count
        except:
            return count
       
    elif( station["OP"] == "addi"):
        try:
            if( station["Qj"] is None and count < 2):
                if(count == 1):
                    can_write[j] = 1
                return (count+1)
            else:
                return count
        except:
            return count
    
    elif(station["OP"] == "call"):
        if(count < 1):
            can_write[j] = 1
            return (count+1)
        else:
            return count 
    
    elif(station["OP"] == "ret"):
        if(station["Qj"] is None and count < 1):
            can_write[j] = 1 
            return (count+1)
        else:
            return count    

def WriteBack(Inst, station):
    if(station["OP"] == "load"):
        if(Inst[1] != "r0"):
            Reg[Inst[1]] = mem[station["A"]]
        fix_after_write(station["Name"], Inst[1])
        station = removeInst(station)

    elif(station["OP"] == "store"):
        mem[station["A"]] = station["Vj"]
        fix_after_write(station["Name"], None)
        station = removeInst(station)

    elif(station["OP"] == "add"):
        if(Inst[1] != "r0"):
            Reg[Inst[1]] = station["Vj"]+station["Vk"]
        fix_after_write(station["Name"], Inst[1])
        station = removeInst(station)

    elif(station["OP"] == "nand"):
        if(Inst[1] != "r0"):
            Reg[Inst[1]] = ~(station["Vj"] & station["Vk"])
        fix_after_write(station["Name"], Inst[1])
        station = removeInst(station)

    elif( station["OP"] == "addi"):
        if(Inst[1] != "r0"):
            Reg[Inst[1]] = station["Vj"]+station["Imm"]
        fix_after_write(station["Name"], Inst[1])
        station = removeInst(station)

    elif(station["OP"] == "div"):
        if(Inst[1] != "r0"):
            Reg[Inst[1]] = station["Vj"]/station["Vk"]
        fix_after_write(station["Name"], Inst[1])
        station = removeInst(station)

    elif(station["OP"] == "bne"):
        fix_after_write(station["Name"], None)
        station = removeInst(station)

    elif(station["OP"] == "call"):
        Reg["r1"] = station["Imm"]+1
        fix_after_write(station["Name"], "r1")
        station = removeInst(station)

    elif(station["OP"] == "ret"):
        fix_after_write(station["Name"], None)
        station = removeInst(station)

def simulate(clk, PC):
    if(clk > 1):
        if(len(write_queue)):
            i = write_queue[0]
            WriteBack(instructions[i], inst_RS[i])
            print("Inst ", i, "Written")
            write_queue.pop(0)

    if(clk != 0):
        for j in range(len(inst_RS)):
            exec_time[j] = canExecute(j, inst_RS[j], exec_time[j])
            print("Executed inst", j, " ", exec_time[j], " cycles")
            if(can_write[j]):
                write_queue.append(j)
                can_write[j] = 0

    if(PC < len(instructions)):
        if(issue(instructions[PC], PC)):
            print("Issued Inst ", PC)
            return(PC + 1)
        else:
            return PC
    else:
        return PC
        

def top ():
    clk = 0
    PC = 0
    
    for i in range (30):
        PC = simulate(clk, PC)
        print("==============================================")
        clk += 1

    #print(Reg)
    # while(True):
    #     go = input()
    #     if(go):
    #         PC = simulate(clk, PC)
    #         clk += 1

top()