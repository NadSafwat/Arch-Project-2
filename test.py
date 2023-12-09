import re

LOAD1 = {"Name" : "Load1" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}
LOAD2 = {"Name" : "Load2" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}
STORE1 = {"Name" : "Store1" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}
STORE2 = {"Name" : "Store2" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}
ADD_ADDI1 = {"Name" : "Add/Addi_1" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}
ADD_ADDI2 = {"Name" : "Add/Addi_2" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}
ADD_ADDI3 = {"Name" : "Add/Addi_3" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}
NAND = {"Name" : "Nand" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}
DIV = {"Name" : "Div" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}
BNE = {"Name" : "Bne" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}
CALL_RET = {"Name" : "Call/Ret" ,"Busy": 'N', "OP":None, "Vj":None, "Vk":None, "Qj": None, "Qk":None, "A":None}

ReservationStation = [LOAD1, LOAD2, STORE1, STORE2, ADD_ADDI1, ADD_ADDI2, ADD_ADDI3, NAND, DIV, BNE, CALL_RET]

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

def issue(Inst):

    if(Inst[0] == "load" or Inst[0] == "store"):
        if(canIssue(Inst)[0] == True ):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = Reg[Inst[3]]
            station["Vk"] = None
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = int(Inst[2])
            
            if(RegisterStat[Inst[3]] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[3]] 

            if(Inst[0] == "store" and RegisterStat[Inst[1]] != None):
                station["Vk"] = None
                station["Qk"] = RegisterStat[Inst[1]]
            elif(Inst[0] == "store" and RegisterStat[Inst[1]] == None):
                station["Vk"] = Reg[Inst[1]]
                station["Qk"] = None
        
        RegisterStat[Inst[1]] = station["Name"]
                

    if(Inst[0] == "add" or Inst[0] == "nand" or Inst[0] == "div"):
        if(canIssue(Inst)[0] == True):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = Reg[Inst[2]]
            station["Vk"] = Reg[Inst[3]]
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = None
             
            if(RegisterStat[Inst[2]] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[2]]           
            
            if(RegisterStat[Inst[3]] != None):
                station["Vk"] = None
                station["Qk"] = RegisterStat[Inst[3]]

        RegisterStat[Inst[1]] = station["Name"]                  

    if(Inst[0] == "addi"):
        if(canIssue(Inst)[0] == True):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = Reg[Inst[2]]
            station["Vk"] = Inst[3]
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = None
            if(RegisterStat[Inst[2]] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[2]]

        RegisterStat[Inst[1]] = station["Name"]

# habd gamed MOT starts from here *standing girl emoji*
    if(Inst[0] == "bne"):
        if(canIssue(Inst)[0]==True):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = Reg[Inst[1]]
            station["Vk"] = Reg[Inst[2]]
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = int(Inst[3])
            if(RegisterStat[Inst[1]] != None):
                station["Vj"] = None
                station["Qj"] = RegisterStat[Inst[1]]
            if(RegisterStat[Inst[2]] != None):
                station["Vk"] = None
                station["Qk"] = RegisterStat[Inst[2]]

    if(Inst[0]=="call"):
        if(canIssue(Inst)[0] == True):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = None
            station["Vk"] = None
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = int(Inst[1])

#idk if i should play around with the vk/vj if r1 is busy or not....
    if(Inst[0]=="ret"):
        if(canIssue(Inst)[0] == True):
            station = canIssue(Inst)[1]
            station["Busy"] = 'Y'
            station["OP"] = Inst[0]
            station["Vj"] = None
            station["Vk"] = None
            station["Qj"] = None
            station["Qk"] = None
            station["A"] = int(Reg["r1"])
        
    # print(Inst[0], station)




#example in the recordings for now
instructions = [["load", "r6", "32", "r2"],["load", "r2", "44", "r3"], 
                ["div","r0","r2","r4"], ["add", "r8","r2","r6"], ["div","r7","r0","r6"],
                ["add", "r6", "r1","r5"] , ["addi", "r1", "r1", "1"], ["add", "r6", "r1","r5"]]
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
    

issue_test(instructions)
print("after func: \n")
print(ReservationStation)


def canExecute(station):
    
    if(station["OP"] == "load"):
        if( station["Qj"] == None ):
            station["A"] = int(station["Vj"]) + station["A"]
            return True
        else:
            return False
        
    if(station["OP"] == "store"):
        if( station["Qj"]):
            return True
        else:
            return False
                
    if(station["OP"] == "add" or station["OP"] == "nand"
        or station["OP"] == "div" or station["OP"] == "bne"):
        if( station["Qj"] == None and station["Qk"] == None):
            return True
        else:
            return False
        
    #assuming we dont store immediate until cherif replies
    if( station["OP"] == "addi"):
        if( station["Qj"] == None):
            return True
        else:
            return False
        
   # idk the check condition for call and ret tbh
    

 # PROBLEM IN TESTING CHECK EXECUT--> cannot map the reservation station to its instruction 
 # also everything so far is not accounting for the clock cycle stuff
 # 
 #    
# def test_everything(instruction_list):
#     i=0
#     for i in range(len(instruction_list)):
#         if(canIssue(instruction_list[i])[0] == True):
#             issue(instruction_list[i])
#             print("Instruction issued")
#             print(instruction_list[i])
#             print(ReservationStation[i])
#         else:
#             print("Instruction cannot be issued")
#         i+=1
#     print("\n")
#     print(ReservationStation)
#     print(len(ReservationStation))
#     print("\nEND OF LOOP 1\n")

#     j=0
#     for j in range(len(instruction_list)):
#         if(canExecute(ReservationStation[j]) == True):
#             print("**************************************")
#             print("Instruction can execute")
#             print(instruction_list[j])
#             print(ReservationStation[j])
#             print("**************************************")
#         else:
#             print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#             print(instruction_list[j])
#             print(ReservationStation[j])
#             print("Instruction cannot execute")
#             print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
#         j+=1

           
# test_everything(instructions)


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

def simulate():
    print("Pending: ")

# getUserInpt()

