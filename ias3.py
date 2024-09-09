from sys import *
from math import *



############################## MEMÓRIA - REGISTRADORES ##############################

MEMORIA = []

AC = 0          #ACCUMULATOR
MQ = 0          #MULTIPLAYER QUOTIENT
IR = 0          #INSTRUCTION REGISTER
PC = 0          #PROGRAM COUNTER
MAR = 0         #MEMORY ACESS REGISTER
MBR = 0         #MEMORY BUFFER REGISTER





################################ CICLO DE INSTRUÇÃO #################################

def busca():
    global MEMORIA, PC, MAR, MBR        
    #
    MAR = PC
    MBR = MEMORIA[MAR]

def decodificacao():
    global IR, MAR
    #
    IR, MAR = separaMBR()

def buscaDosOperandos():
    global MEMORIA, MBR, MAR
    #
    MBR = MEMORIA[MAR]

def execucao():
    global MEMORIA,AC,MQ,IR,PC,MAR,MBR
    #
    intCheck()
    #
    match IR:
                        ########## TODAS FUNÇÕES LOAD ##########
        case 'LOADM':
            AC = MBR
        case 'LOADMQ':
            AC = MQ
        case 'LOADMQM':
            MQ = MBR
        case 'LOAD-M':
            AC = MBR*(-1)
        case 'LOAD|M':
            AC = sqrt(MBR**2)
        case 'LOAD-|M':
            AC = (sqrt(MBR**2)) * (-1)
                        ########## FUNÇÕES ARITMÉTICAS ##########
        case 'ADDM':
            AC += MBR
        case 'ADD|M':
            AC += sqrt(MBR**2)
        case 'SUBM':
            AC -= MBR
        case 'SUB|M':
            AC -= sqrt(MBR**2)
        case 'DIVM':
            MQ = AC // MBR
            AC = AC % MBR
        case 'MULM':
            AC = MQ * MBR
        case 'LSH':
            AC *= 2
        case 'RSH':
            AC /= 2
                        ########## STOR E FUNÇÕES JUMP ##########
        case 'STORM':
            MEMORIA[MAR] = AC
        case 'JUMPM':
            PC = MAR - 1
        case 'JUMP+M':
            if AC >= 0:
                PC = MAR - 1





################################ FUNÇÕES AUXILIARES #################################

def carrega_memoria(arquivo):
    with open(arquivo,'r') as fin:
        mem = fin.readlines()
    mem = [item.replace('\n','') for item in mem]
    return mem

def inicia_PC():
    global MEMORIA
    for i in range(len(MEMORIA)):
        try:
            int(MEMORIA[i])
        except:
            return i

def printDadosMemoria():
    for i in range(inicia_PC()):
        print(f'    M({i})  {MEMORIA[i]}')

def separaMBR():
    global MBR
    parenteses = False
    MBR = MBR.replace(' ','')
    for i in range(len(MBR)):
        if MBR[i] == '(':
            parenteses = True
            break
    #
    if parenteses == True:
        MBR_OPCODE = MBR[0:i]
        MBR_OPCODE = MBR_OPCODE.replace(',','')
    elif parenteses == False:
        MBR_OPCODE = MBR[0:i+1]
    #
    MBR_LEAST_SIG_BITS = MBR[i:]
    MBR_LEAST_SIG_BITS = MBR_LEAST_SIG_BITS.replace('M','')
    MBR_LEAST_SIG_BITS = MBR_LEAST_SIG_BITS.replace(',','')
    MBR_LEAST_SIG_BITS = MBR_LEAST_SIG_BITS.replace('(','')
    MBR_LEAST_SIG_BITS = MBR_LEAST_SIG_BITS.replace(')','')
    MBR_LEAST_SIG_BITS = MBR_LEAST_SIG_BITS.replace('|','')
    MBR_LEAST_SIG_BITS = MBR_LEAST_SIG_BITS.replace(' ','')
    #
    try:
        MBR_LEAST_SIG_BITS = int(MBR_LEAST_SIG_BITS)
    except:
        MBR_LEAST_SIG_BITS = 0
    #
    return MBR_OPCODE, MBR_LEAST_SIG_BITS

def intCheck():
    global AC, MQ, MBR, PC
    try:
        AC = int(AC)
    except:
        pass
    try:
        MQ = int(MQ)
    except:
        pass
    try:
        MBR = int(MBR)
    except:
        pass
    try:
        PC = int(PC)
    except:
        pass





#################################### PROCESSADOR ####################################
    
def processador():
    global PC
    PC = inicia_PC()
    while PC < len(MEMORIA):
        busca()
        decodificacao()
        buscaDosOperandos()
        execucao()
        PC += 1





################################# INICIO DO PROGRAMA ################################

MEMORIA = carrega_memoria(argv[1])

processador()

printDadosMemoria()