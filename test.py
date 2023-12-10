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
ReservationStation = [LOAD1, LOAD2, STORE1, STORE2, ADD_ADDI1, ADD_ADDI2, ADD_ADDI3, NAND, DIV, BNE, CALL_RET]

mem = []
inst_issed = []
inst_RS = []
exec_time = []
can_write = []
write_queue = []
instructions = []

call_ret_issued = False
call_ret_written = False
stall_issuing = False

branchIssued = False
BranchWritten = False
BranchIndex = 100000
BranchTaken = False
stall_executing = False

Number_of_branches = 0
Number_of_branches_taken = 0

Reg = {
    "r0": 0,
    "r1": 7,
    "r2": 0,
    "r3": 0,
    "r4": 0,
    "r5": 0,
    "r6": 1,
    "r7": 0,
    "r8": 0
}

def IntializeMem ():
    for i in range(6400):
        mem.append(0)

def is_valid_instruction(instruction):
    if (instruction[0:4] == "load" or instruction[0:5] == "store"):
        if(instruction[7:9]=="32"):
           return False
        instruction_pattern = re.compile(r'(load|store)r[0-7],(-?(?:[0-9]|[1-2][0-9]|3[0-2]))\(r[0-7]\)$')

    elif(instruction[0:3] == "bne"):
        if(instruction[9:11]=="32"):
            return False
        instruction_pattern = re.compile(r'bner[0-7],r[0-7],(-?(?:[0-9]|[1-2][0-9]|3[0-2]))$')

    elif(instruction[0:4] == "call"):
        if(instruction[4:6]=="32"):
            return False
        instruction_pattern = re.compile(r'call(-?(?:[0-9]|[1-2][0-9]|3[0-2]))$')

    elif(instruction[0:3] == "ret"):
        instruction_pattern = re.compile(r'ret$')

    elif(instruction[0:4] == "addi"):
        if(instruction[10:12]=="32"):
            return False
        instruction_pattern = re.compile(r'addir[0-7],r[0-7],(-?(?:[0-9]|[1-2][0-9]|3[0-2]))$')

    elif(instruction[0:3] == "add" or instruction[0:4] == "nand" or instruction[0:3] == "div"):
        instruction_pattern = re.compile(r'(add|nand|div)r[0-7],r[0-7],r[0-7]$')

    return bool(instruction_pattern.match(instruction))

def getUserInptInst():
    instructions_to_run=[]
    print("Available instructions are: \nload rA, offset(rB) \nstore rA, offset(rB) \nbne rA, rB, offset \ncall label \nret \nadd rA, rB, rC \naddi rA, rB, imm \nnand rA, rB, rC \ndiv rA, rB, rC")
    print("Please enter your instructions one by one or 0 to signal end")
    while(True):
        userInst = input(": ").lower().replace(" ","")
        if (userInst == '0'):
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

def getUserInptMem():
    print("Please enter your required memory values or press enter to signal end: ")
    while(True):
        try: 
            addr = int(input("Enter Address: "))
            if(addr > 7):
                print("Invalid address")
            else:
                try: 
                    data_in = int(input("Enter data (16 bit): "))
                    if(data_in > 65536):
                        print("Data is too large")
                    else:
                        mem[addr] = data_in
                except: print("Invalid Input")
        except: return 

instructions = [["load", "r5", "0", "r2"],  #0
                ["load", "r2", "1", "r2"],  #1
                ["div","r0","r2","r4"],     #2
                ["add", "r4","r2","r6"],    #3
                ["bne","r1","r2","2"],      #4  
                ["add", "r2", "r1","r5"],   #5
                ["ret", None, None, None],  #6
                ["add", "r6", "r1","r5"],   #7
                ["bne","r5","r6","5"],      #8
                ["store", "r1",2,"r2"],     #9
                ["bne", "r1","r2","1"],     #10
                ["call", -5, None, None],   #11
                ["add", "r0","r0","r0"]     #12
                ]
                
                

IntializeMem()
getUserInptMem()
# instructions = getUserInptInst()

# for reg/Qi table at the bottom of every slide
def fix_after_write(functional_unit_name, inst):
    if (inst[0] == "store" or inst[0]== "bne" or inst[0]=="ret" ):
        rd = None
    elif (inst[0] == "call"):
        rd = "r1"
    else:
        rd = inst[1]
    for rs in ReservationStation:
        if(rs["Qj"] == functional_unit_name):
            rs["Qj"] = None
            rs["Vj"] = Reg[rd]
        if(rs["Qk"] == functional_unit_name):
            rs["Qk"] = None
            rs["Vk"] = Reg[rd]
    if(rd is not None):
        RegisterStat[rd] = None

def canIssue(Inst, written_FU):
    if(Inst[0] == "load"):
        if(LOAD1["Busy"] == 'N' and written_FU != "Load1"):
            return True, ReservationStation[0]
        elif(LOAD2["Busy"] == "N" and written_FU != "Load2"):
            return True, ReservationStation[1]
        else:
            return False, None
        
    elif(Inst[0] == "add" or Inst[0] == "addi"):
        if(ADD_ADDI1["Busy"] == 'N' and written_FU != "Add/Addi_1"):
            return True, ReservationStation[4]
        elif(ADD_ADDI2["Busy"] == "N" and written_FU != "Add/Addi_2"):
            return True, ReservationStation[5]
        elif(ADD_ADDI3["Busy"] == "N" and written_FU != "Add/Addi_3"):
            return True, ReservationStation[6]
        else:
            return False,None
    
    elif(Inst[0] == "store"):
        if(STORE1["Busy"] == 'N' and written_FU != "Store1"):
            return True, ReservationStation[2]
        elif(STORE2["Busy"] == "N" and written_FU != "Store2"):
            return True, ReservationStation[3]
        else:
            return False,None
    
    elif(Inst[0] == "nand"):
        if(NAND["Busy"] == 'N' and written_FU != "Nand" ):
            return True, ReservationStation[7]
        else:
            return False,None
    
    elif(Inst[0] == "div" and written_FU != "Div"):
        if(DIV["Busy"] == 'N'):
            return True, ReservationStation[8]
        else:
            return False,None
    
    elif(Inst[0] == "bne"):
        if(BNE["Busy"] == 'N' and written_FU != "Bne"):
            return True, ReservationStation[9]
        else:
            return False,None
    elif(Inst[0] == "call" or Inst[0] == "ret"):
        if(CALL_RET["Busy"] == 'N'and written_FU != "Call/Ret"):
            return True, ReservationStation[10]
        else:
            return False,None
    else:
        return False,None

def issue(Inst, PC, written_FU):
    global branchIssued
    global BranchIndex
    global call_ret_issued

    issue_flag, issue_station = canIssue(Inst, written_FU)
    if(Inst[0] == "load"):
        if(issue_flag == True):
            station = issue_station
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
            inst_issed.append(Inst)
            exec_time.append(0)
            can_write.append(0)
            return True
        else:
            return False
    
    elif(Inst[0] == "store"):
        if(issue_flag == True ):
            station = issue_station
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
            inst_issed.append(Inst)
            exec_time.append(0)
            can_write.append(0)
            return True
        else:
            return False       

    elif(Inst[0] == "add" or Inst[0] == "nand" or Inst[0] == "div"):
        if(issue_flag == True):
            station = issue_station
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
            inst_issed.append(Inst)
            exec_time.append(0)
            can_write.append(0)
            return True
        else:
            return False
                   

    elif(Inst[0] == "addi"):
        if(issue_flag == True):
            station = issue_station
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
            inst_issed.append(Inst)
            exec_time.append(0)
            can_write.append(0)
            return True
        else:
            return False

    elif(Inst[0] == "bne"):
        if(issue_flag ==True):
            station = issue_station
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
            inst_issed.append(Inst)
            exec_time.append(0)
            can_write.append(0)

            branchIssued = True
            BranchIndex = (len(inst_issed) - 1)
            return True
        else:
            return False

    elif(Inst[0]=="call"):
        if(issue_flag == True):
            station = issue_station
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
            inst_issed.append(Inst)
            exec_time.append(0)
            can_write.append(0)

            call_ret_issued = True
            return True
        else:
            return False

    elif(Inst[0]=="ret"):
        if(issue_flag == True):
            station = issue_station
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
            inst_issed.append(Inst)
            exec_time.append(0)
            can_write.append(0)

            call_ret_issued = True
            return True
        else:
            return False

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
    global Number_of_branches

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
                Number_of_branches += 1
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
        try:
            if(count < 1):
                can_write[j] = 1
                return (count+1)
            else:
                return count
        except:
            return count
    
    elif(station["OP"] == "ret"):
        try:
            if(station["Qj"] is None and count < 1):
                can_write[j] = 1 
                return (count+1)
            else:
                return count
        except:
            return count

    else:
        return None

def WriteBack(Inst, station,PC):
    global BranchWritten
    global BranchTaken
    global Number_of_branches_taken
    
    global call_ret_written

    if(station["OP"] == "load"):
        if(Inst[1] != "r0"):
            Reg[Inst[1]] = mem[station["A"]]
        fix_after_write(station["Name"], Inst)
        station = removeInst(station)

    elif(station["OP"] == "store"):
        mem[station["A"]] = station["Vj"]
        fix_after_write(station["Name"], Inst)
        station = removeInst(station)

    elif(station["OP"] == "add"):
        if(Inst[1] != "r0"):
            Reg[Inst[1]] = station["Vj"]+station["Vk"]
        fix_after_write(station["Name"], Inst)
        station = removeInst(station)

    elif(station["OP"] == "nand"):
        if(Inst[1] != "r0"):
            Reg[Inst[1]] = ~(station["Vj"] & station["Vk"])
        fix_after_write(station["Name"], Inst)
        station = removeInst(station)

    elif( station["OP"] == "addi"):
        if(Inst[1] != "r0"):
            Reg[Inst[1]] = station["Vj"]+station["Imm"]
        fix_after_write(station["Name"], Inst)
        station = removeInst(station)

    elif(station["OP"] == "div"):
        if(Inst[1] != "r0"):
            Reg[Inst[1]] = station["Vj"]/station["Vk"]
        fix_after_write(station["Name"], Inst)
        station = removeInst(station)

    elif(station["OP"] == "bne"):
        if(station["Vj"] != station["Vk"]):
            BranchTaken = True
            Number_of_branches_taken += 1
            PC = station["A"]
        BranchWritten = True
        fix_after_write(station["Name"], Inst)
        station = removeInst(station)

    elif(station["OP"] == "call"):
        Reg["r1"] = station["Imm"]+1
        PC = station["A"]
        call_ret_written = True
        fix_after_write(station["Name"], Inst)
        station = removeInst(station)

    elif(station["OP"] == "ret"):
        PC = station["A"]
        call_ret_written = True
        fix_after_write(station["Name"], Inst)
        station = removeInst(station)
    
    return PC

def simulate(clk, PC):
    written_FU = None
    global inst_issed
    global inst_RS
    global stall_issuing
    global stall_executing
    global call_ret_written
    global call_ret_issued
    global branchIssued
    global BranchWritten
    global BranchIndex
    global BranchTaken

    stall_issuing = call_ret_issued and not call_ret_written
    stall_executing = branchIssued and not BranchWritten

    if(not stall_issuing):
        call_ret_issued = False
        call_ret_written = False
    
    if(not stall_executing):
        branchIssued = False
        BranchWritten = False
        BranchIndex = 100000
        BranchTaken = False

    if(clk > 1):
        if(len(write_queue)):
            i = write_queue[0]
            written_FU = inst_RS[i]["Name"]
            PC_target = WriteBack(inst_issed[i], inst_RS[i],PC)
            print("Inst ", i, "Written")                
            write_queue.pop(0)

    if(clk != 0):
        for j in range(len(inst_RS)):
            if(j <= BranchIndex):
                exec_time[j] = canExecute(j, inst_RS[j], exec_time[j])
                print("Executed inst", inst_issed[j][0] , " ", exec_time[j], " cycles")
                if(can_write[j]):
                    write_queue.append(j)
                    can_write[j] = 0

    if(PC < len(instructions)):
        if (not stall_issuing):
            issue_flag = issue(instructions[PC], PC, written_FU)
            if(issue_flag):
                print("Issued Inst ", PC)
        if(BranchTaken):
            stall_issuing = False
            for i in range(BranchIndex+1, len(inst_RS)):
                fix_after_write(inst_RS[i]["Name"], inst_issed[i])
                inst_RS[i] = removeInst(inst_RS[i])
            inst_issed = inst_issed[:BranchIndex+1]
            inst_RS = inst_RS[:BranchIndex+1]
           
            return PC_target
        elif(stall_issuing):
            return (PC)
        else:
            return(PC+1)
    else:
        return PC
    
        
def top ():
    clk = 0
    PC = 0

    while(True):
        
        go = input()
        if(go):
            PC = simulate(clk, PC)
            print("==============================================")
            clk += 1
        else:
            return                  

top()

print(Reg)
# print(mem)
print(inst_issed)

print("Number of Branches: ", Number_of_branches)
print("Number of Branches Taken: ", Number_of_branches_taken)

print("IC: ", len(inst_issed))