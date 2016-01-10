#!/usr/bin/python
import curses

NORMAL = 0
KERNEL = -1

MY_IP_COLOR = 2 #TODO: Hard-code some RGB colors
O_IP_COLOR = 6
B_IP_COLOR = 12
O_CHANGE_COLOR = 24
CURS_COLOR = 255

KEY_ESC = 27
KEY_ENTER = 10

DIRECT = 0b01
IMMEDIATE = 0b10
LESS = 0b001
EQUAL = 0b010
GREATER = 0b100
JMP = 0b111

OP_WORD_SHIFT = 0x10
OP_WORD_SHIFT_SMALL = 0x03
OP_INDIRECT_SHIFT_DST = 0x04
OP_IMMEDIATE_SHIFT_DST = 0x04
OP_INDIRECT_SHIFT_SRC = 0x02
OP_REGISTER_SHIFT_SRC = 0x01
OP_INDIRECT_SHIFT_SMALL = 0x01
OP_IMMEDIATE_SHIFT_SMALL = 0x01

OP_MOV = 0x10
OP_MOV_R_I = 0x10
OP_MOV_R_R = 0x11
OP_MOV_R_IP = 0x12
OP_MOV_R_RP = 0x13
OP_MOV_RP_I = 0x14
OP_MOV_RP_R = 0x15
OP_MOV_RP_IP = 0x16
OP_MOV_RP_RP = 0x17
OP_MOV_IP_I = 0x18
OP_MOV_IP_R = 0x19
OP_MOV_IP_IP = 0x1a
OP_MOV_IP_RP = 0x1b
OP_MOV_R_I2 = 0x20
OP_MOV_R_R2 = 0x21
OP_MOV_R_IP2 = 0x22
OP_MOV_R_RP2 = 0x23
OP_MOV_RP_I2 = 0x24
OP_MOV_RP_R2 = 0x25
OP_MOV_RP_IP2 = 0x26
OP_MOV_RP_RP2 = 0x27
OP_MOV_IP_I2 = 0x28
OP_MOV_IP_R2 = 0x29
OP_MOV_IP_IP2 = 0x2a
OP_MOV_IP_RP2 = 0x2b

OP_ADD = 0x30
OP_ADD_R_I = 0x30
OP_ADD_R_R = 0x31
OP_ADD_R_IP = 0x32
OP_ADD_R_RP = 0x33
OP_ADD_RP_I = 0x34
OP_ADD_RP_R = 0x35
OP_ADD_RP_IP = 0x36
OP_ADD_RP_RP = 0x37
OP_ADD_IP_I = 0x38
OP_ADD_IP_R = 0x39
OP_ADD_IP_IP = 0x3a
OP_ADD_IP_RP = 0x3b
OP_ADD_R_I2 = 0x40
OP_ADD_R_R2 = 0x41
OP_ADD_R_IP2 = 0x42
OP_ADD_R_RP2 = 0x43
OP_ADD_RP_I2 = 0x44
OP_ADD_RP_R2 = 0x45
OP_ADD_RP_IP2 = 0x46
OP_ADD_RP_RP2 = 0x47
OP_ADD_IP_I2 = 0x48
OP_ADD_IP_R2 = 0x49
OP_ADD_IP_IP2 = 0x4a
OP_ADD_IP_RP2 = 0x4b

OP_SUB = 0x50
OP_SUB_R_I = 0x50
OP_SUB_R_R = 0x51
OP_SUB_R_IP = 0x52
OP_SUB_R_RP = 0x53
OP_SUB_RP_I = 0x54
OP_SUB_RP_R = 0x55
OP_SUB_RP_IP = 0x56
OP_SUB_RP_RP = 0x57
OP_SUB_IP_I = 0x58
OP_SUB_IP_R = 0x59
OP_SUB_IP_IP = 0x5a
OP_SUB_IP_RP = 0x5b
OP_SUB_R_I2 = 0x60
OP_SUB_R_R2 = 0x61
OP_SUB_R_IP2 = 0x62
OP_SUB_R_RP2 = 0x63
OP_SUB_RP_I2 = 0x64
OP_SUB_RP_R2 = 0x65
OP_SUB_RP_IP2 = 0x66
OP_SUB_RP_RP2 = 0x67
OP_SUB_IP_I2 = 0x68
OP_SUB_IP_R2 = 0x69
OP_SUB_IP_IP2 = 0x6a
OP_SUB_IP_RP2 = 0x6b

OP_CMP = 0x70
OP_CMP_R_I = 0x70
OP_CMP_R_R = 0x71
OP_CMP_R_IP = 0x72
OP_CMP_R_RP = 0x73
OP_CMP_RP_I = 0x74
OP_CMP_RP_R = 0x75
OP_CMP_RP_IP = 0x76
OP_CMP_RP_RP = 0x77
OP_CMP_IP_I = 0x78
OP_CMP_IP_R = 0x79
OP_CMP_IP_IP = 0x7a
OP_CMP_IP_RP = 0x7b
OP_CMP_R_I2 = 0x80
OP_CMP_R_R2 = 0x81
OP_CMP_R_IP2 = 0x82
OP_CMP_R_RP2 = 0x83
OP_CMP_RP_I2 = 0x84
OP_CMP_RP_R2 = 0x85
OP_CMP_RP_IP2 = 0x86
OP_CMP_RP_RP2 = 0x87
OP_CMP_IP_I2 = 0x88
OP_CMP_IP_R2 = 0x89
OP_CMP_IP_IP2 = 0x8a
OP_CMP_IP_RP2 = 0x8b

OP_JMP = 0x90
OP_JE = 0x91
OP_JL = 0x92
OP_JG = 0x93
OP_JNE = 0x94
OP_JLE = 0x95
OP_JGE = 0x96

OP_INC = 0xa0
OP_INC_R = 0xa0
OP_INC_RP = 0xa1
OP_INC_IP = 0xa2
OP_INC_R2 = 0xa3
OP_INC_RP2 = 0xa4
OP_INC_IP2 = 0xa5

OP_DEC = 0xb0
OP_DEC_R = 0xb0
OP_DEC_RP = 0xb1
OP_DEC_IP = 0xb2
OP_DEC_R2 = 0xb3
OP_DEC_RP2 = 0xb4
OP_DEC_IP2 = 0xb5

szMem = 12
szBlock = 64
szReg = 8
ipFov = 8
nSteps = 1
nTokens= 16

maxCol = 16

class NotByteError(Exception):
    def __init__(self):
        pass

class UnknownInstruction(Exception):
    def __init__(self):
        pass

class TooFewTokens(Exception):
    def __init__(self):
        pass

class IpDeadError(Exception):
    def __init__(self):
        pass

class MemBlock(list):
    def __init__(self, hidden=True):
        self.hidden = hidden
        return super().__init__([Byte() for i in range(szBlock)])

class Player:
    def __init__(self, tokens=nTokens, name='player'):
        self.tokens = tokens
        self.mem = [MemBlock() for i in range(szMem)]
        self.curs = (0,0)
        self.name = name
class Ip:
    def __init__(self, pos, owner):
        self.owner = owner
        self.pos = pos
        self.cmpBit = 1

class Byte:
    def __init__(self):
        self.hidden = True
        self.my_ip = False
        self.o_ip = False
        self.ip_d = False
        self.im = False
        self.change = None
    def reset(self):
        self.__init__()

def printMem(plId):
    global memToScr
    memToScr = dict()
    plMem = players[plId].mem
    scr.clear()
    scr.move(0, 8)
    for i in range(maxCol):
        scr.addstr('%02x ' % i)
    #scr.move(0, maxCol*3+22)
    #for i in range(szReg):
    #    scr.addstr('%02x  ' % i)
    scr.move(1, maxCol*3+16)
    scr.addstr('REGISTERS: ')
    for reg in regs:
        scr.addstr('%02x  ' % reg)
    scr.move(2, 0)
    for i, block in enumerate(plMem):
        if block.hidden:
            scr.addstr(scr.getyx()[0], 3*maxCol+9,'?')
            scr.move(scr.getyx()[0], 0)
        elif blPrivs[i] == KERNEL:
            scr.addstr(scr.getyx()[0], 3*maxCol+9,'KERNEL')
            scr.move(scr.getyx()[0], 0)

        col = 0
        scr.addstr('%#06x  ' % (szBlock*i))
        for y, byte in enumerate(block):
            if col == maxCol:
                scr.move(scr.getyx()[0]+1, 0)
                scr.addstr('%#06x  ' % (szBlock*i+y))
                col = 0
            if byte.hidden:
                s = '??'
                scr.addstr(s+' ')
            else:
                s = '%02x' % mem[i][y]
                mode = curses.A_NORMAL
                if byte.im:
                    mode |= curses.A_BOLD
                if byte.ip_d:
                    mode |= curses.A_REVERSE
                if byte.o_ip & byte.my_ip:
                    scr.addstr(s, curses.color_pair(B_IP_COLOR) | mode)
                    scr.addstr(' ')
                elif byte.o_ip:
                    scr.addstr(s, curses.color_pair(O_IP_COLOR) | mode)
                    scr.addstr(' ')
                elif byte.my_ip:
                    scr.addstr(s, curses.color_pair(MY_IP_COLOR) | mode)
                    scr.addstr(' ')
                elif byte.change is not None and byte.change != plId:
                    scr.addstr(s, curses.color_pair(O_CHANGE_COLOR) | mode)
                    scr.addstr(' ')
                else:
                    scr.addstr(s+' ', mode)
            memToScr[(i,y)] = scr.getyx()
            col += 1
        scr.move(scr.getyx()[0]+2, 0)

def printUI(plId):
    player = players[plId]
    global cmdyx
    cmdyx = (scr.getyx()[0]+1, 0)
    scr.addstr('PLAYER=%s\t' % player.name)
    scr.addstr('TOKENS=%02x\t' % player.tokens)
    scr.addstr('INSTRUCTION PTRS=%02x\t' % len([None for ip in ips if ip.owner == plId]))

def run(plId):
    player = players[plId]
    plMem = player.mem
    for ip in (i for i in ips if i.owner == plId):
        try:
            for i in range(nSteps):
                runByte(plId, ip)
                if ip.pos[1]+1 == szBlock:
                    if ip.pos[0]+1 == szMem:
                        raise IpDeadError
                    else:
                        ip.pos = (ip.pos[0]+1, 0)
                else:
                    ip.pos = (ip.pos[0], ip.pos[1]+1)
        except IpDeadError:
            ipDead = True
        else:
            ipDead = False

        for i, pl in enumerate(players):
            if i == plId:
                pl.mem[ip.pos[0]][ip.pos[1]].my_ip = True
            else:
                pl.mem[ip.pos[0]][ip.pos[1]].o_ip = True
            if ipDead:
                pl.mem[ip.pos[0]][ip.pos[1]].ip_d = True
        if not ipDead:
            plMem[ip.pos[0]].hidden = False
            if ip.pos[1]+ipFov >= szBlock:
                for i in range(ip.pos[1], szBlock):
                    plMem[ip.pos[0]][i].hidden = False
            else:
                for i in range(ip.pos[1], ip.pos[1]+ipFov):
                    plMem[ip.pos[0]][i].hidden = False
        else:
            ips.remove(ip)

def runByte(plId, ip):
    player = players[plId]
    plMem = player.mem
    byte = mem[ip.pos[0]][ip.pos[1]]
    mov  = lambda x, y, mod: y
    add = lambda x, y, mod: (x + y) % mod
    sub = lambda x, y, mod: (x - y) % mod
    jmp = lambda o, j: o if j is None else j
    if byte == OP_MOV_R_I:
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r, DIRECT, im, DIRECT | IMMEDIATE, mov, plId)
    elif byte == OP_MOV_R_I2:
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, DIRECT, (imh, iml), DIRECT | IMMEDIATE, mov, plId, word=True)
    elif byte == OP_MOV_R_R:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, DIRECT, mov, plId)
    elif byte == OP_MOV_R_R2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, DIRECT, mov, plId, word=True)
    elif byte == OP_MOV_R_IP:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, DIRECT, (mh, ml), IMMEDIATE, mov, plId)
    elif byte == OP_MOV_R_IP2:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, DIRECT, (mh, ml), IMMEDIATE, mov, plId, word=True)
    elif byte == OP_MOV_R_RP:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, 0, mov, plId)
    elif byte == OP_MOV_R_RP2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, 0, mov, plId, word=True)
    elif byte == OP_MOV_RP_I:
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r, 0, im, DIRECT | IMMEDIATE, mov, plId)
    elif byte == OP_MOV_RP_I2:
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, 0, (imh, iml), DIRECT | IMMEDIATE, mov, plId, word=True)
    elif byte == OP_MOV_RP_R:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, DIRECT, mov, plId)
    elif byte == OP_MOV_RP_R2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, DIRECT, mov, plId, word=True)
    elif byte == OP_MOV_RP_IP:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, 0, (mh, ml), IMMEDIATE, mov, plId)
    elif byte == OP_MOV_RP_IP2:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, 0, (mh, ml), IMMEDIATE, mov, plId, word=True)
    elif byte == OP_MOV_RP_RP:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, 0, mov, plId)
    elif byte == OP_MOV_RP_RP2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, 0, mov, plId, word=True)
    elif byte == OP_MOV_IP_I:
        (mh, ml, im), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, im, DIRECT | IMMEDIATE, mov, plId)
    elif byte == OP_MOV_IP_I2:
        (mh, ml, imh, iml), mvIpTo = readBytes([], ip.pos, 4)
        movByte((mh, ml), IMMEDIATE, (imh, iml), DIRECT | IMMEDIATE, mov, plId, word=True)
    elif byte == OP_MOV_IP_R:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, DIRECT, mov, plId)
    elif byte == OP_MOV_IP_R2:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, DIRECT, mov, plId, word=True)
    elif byte == OP_MOV_IP_IP:
        (mh1, ml1, mh2, ml2), mvIpTo = readBytes([], ip.pos, 4)
        movByte((mh1, ml1), IMMEDIATE, (mh2, ml2), IMMEDIATE, mov, plId)
    elif byte == OP_MOV_IP_IP2:
        (mh1, ml1, mh2, ml2), mvIpTo = readBytes([], ip.pos, 4)
        movByte((mh1, ml1), IMMEDIATE, (mh2, ml2), IMMEDIATE, mov, plId, word=True)
    elif byte == OP_MOV_IP_RP:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, 0, mov, plId)
    elif byte == OP_MOV_IP_RP2:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, 0, mov, plId, word=True)
    elif byte == OP_ADD_R_I:
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r, DIRECT, im, DIRECT | IMMEDIATE, add, plId)
    elif byte == OP_ADD_R_I2:
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, DIRECT, (imh, iml), DIRECT | IMMEDIATE, add, plId, word=True)
    elif byte == OP_ADD_R_R:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, DIRECT, add, plId)
    elif byte == OP_ADD_R_R2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, DIRECT, add, plId, word=True)
    elif byte == OP_ADD_R_IP:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, DIRECT, (mh, ml), IMMEDIATE, add, plId)
    elif byte == OP_ADD_R_IP2:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, DIRECT, (mh, ml), IMMEDIATE, add, plId, word=True)
    elif byte == OP_ADD_R_RP:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, 0, add, plId)
    elif byte == OP_ADD_R_RP2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, 0, add, plId, word=True)
    elif byte == OP_ADD_RP_I:
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r, 0, im, DIRECT | IMMEDIATE, add, plId)
    elif byte == OP_ADD_RP_I2:
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, 0, (imh, iml), DIRECT | IMMEDIATE, add, plId, word=True)
    elif byte == OP_ADD_RP_R:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, DIRECT, add, plId)
    elif byte == OP_ADD_RP_R2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, DIRECT, add, plId, word=True)
    elif byte == OP_ADD_RP_IP:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, 0, (mh, ml), IMMEDIATE, add, plId)
    elif byte == OP_ADD_RP_IP2:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, 0, (mh, ml), IMMEDIATE, add, plId, word=True)
    elif byte == OP_ADD_RP_RP:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, 0, add, plId)
    elif byte == OP_ADD_RP_RP2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, 0, add, plId, word=True)
    elif byte == OP_ADD_IP_I:
        (mh, ml, im), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, im, DIRECT | IMMEDIATE, add, plId)
    elif byte == OP_ADD_IP_I2:
        (mh, ml, imh, iml), mvIpTo = readBytes([], ip.pos, 4)
        movByte((mh, ml), IMMEDIATE, (imh, iml), DIRECT | IMMEDIATE, add, plId, word=True)
    elif byte == OP_ADD_IP_R:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, DIRECT, add, plId)
    elif byte == OP_ADD_IP_R2:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, DIRECT, add, plId, word=True)
    elif byte == OP_ADD_IP_IP:
        (mh1, ml1, mh2, ml2), mvIpTo = readBytes([], ip.pos, 4)
        movByte((mh1, ml1), IMMEDIATE, (mh2, ml2), IMMEDIATE, add, plId)
    elif byte == OP_ADD_IP_IP2:
        (mh1, ml1, mh2, ml2), mvIpTo = readBytes([], ip.pos, 4)
        movByte((mh1, ml1), IMMEDIATE, (mh2, ml2), IMMEDIATE, add, plId, word=True)
    elif byte == OP_ADD_IP_RP:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, 0, add, plId)
    elif byte == OP_ADD_IP_RP2:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, 0, add, plId, word=True)
    elif byte == OP_SUB_R_I:
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r, DIRECT, im, DIRECT | IMMEDIATE, sub, plId)
    elif byte == OP_SUB_R_I2:
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, DIRECT, (imh, iml), DIRECT | IMMEDIATE, sub, plId, word=True)
    elif byte == OP_SUB_R_R:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, DIRECT, sub, plId)
    elif byte == OP_SUB_R_R2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, DIRECT, sub, plId, word=True)
    elif byte == OP_SUB_R_IP:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, DIRECT, (mh, ml), IMMEDIATE, sub, plId)
    elif byte == OP_SUB_R_IP2:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, DIRECT, (mh, ml), IMMEDIATE, sub, plId, word=True)
    elif byte == OP_SUB_R_RP:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, 0, sub, plId)
    elif byte == OP_SUB_R_RP2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, DIRECT, r2, 0, sub, plId, word=True)
    elif byte == OP_SUB_RP_I:
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r, 0, im, DIRECT | IMMEDIATE, sub, plId)
    elif byte == OP_SUB_RP_I2:
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, 0, (imh, iml), DIRECT | IMMEDIATE, sub, plId, word=True)
    elif byte == OP_SUB_RP_R:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, DIRECT, sub, plId)
    elif byte == OP_SUB_RP_R2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, DIRECT, sub, plId, word=True)
    elif byte == OP_SUB_RP_IP:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, 0, (mh, ml), IMMEDIATE, sub, plId)
    elif byte == OP_SUB_RP_IP2:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        movByte(r, 0, (mh, ml), IMMEDIATE, sub, plId, word=True)
    elif byte == OP_SUB_RP_RP:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, 0, sub, plId)
    elif byte == OP_SUB_RP_RP2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        movByte(r1, 0, r2, 0, sub, plId, word=True)
    elif byte == OP_SUB_IP_I:
        (mh, ml, im), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, im, DIRECT | IMMEDIATE, sub, plId)
    elif byte == OP_SUB_IP_I2:
        (mh, ml, imh, iml), mvIpTo = readBytes([], ip.pos, 4)
        movByte((mh, ml), IMMEDIATE, (imh, iml), DIRECT | IMMEDIATE, sub, plId, word=True)
    elif byte == OP_SUB_IP_R:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, DIRECT, sub, plId)
    elif byte == OP_SUB_IP_R2:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, DIRECT, sub, plId, word=True)
    elif byte == OP_SUB_IP_IP:
        (mh1, ml1, mh2, ml2), mvIpTo = readBytes([], ip.pos, 4)
        movByte((mh1, ml1), IMMEDIATE, (mh2, ml2), IMMEDIATE, sub, plId)
    elif byte == OP_SUB_IP_IP2:
        (mh1, ml1, mh2, ml2), mvIpTo = readBytes([], ip.pos, 4)
        movByte((mh1, ml1), IMMEDIATE, (mh2, ml2), IMMEDIATE, sub, plId, word=True)
    elif byte == OP_SUB_IP_RP:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, 0, sub, plId)
    elif byte == OP_SUB_IP_RP2:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        movByte((mh, ml), IMMEDIATE, r, 0, sub, plId, word=True)
    elif byte == OP_CMP_R_I:
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        ip.cmpBit = cmpByte(r, DIRECT, im, DIRECT | IMMEDIATE)
    elif byte == OP_CMP_R_I2:
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte(r, DIRECT, (imh, iml), DIRECT | IMMEDIATE, word=True)
    elif byte == OP_CMP_R_R:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        ip.cmpBit = cmpByte(r1, DIRECT, r2, DIRECT)
    elif byte == OP_CMP_R_R2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        ip.cmpBit = cmpByte(r1, DIRECT, r2, DIRECT, word=True)
    elif byte == OP_CMP_R_IP:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte(r, DIRECT, (mh, ml), IMMEDIATE)
    elif byte == OP_CMP_R_IP2:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte(r, DIRECT, (mh, ml), IMMEDIATE, word=True)
    elif byte == OP_CMP_R_RP:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        ip.cmpBit = cmpByte(r1, DIRECT, r2, 0)
    elif byte == OP_CMP_R_RP2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        ip.cmpBit = cmpByte(r1, DIRECT, r2, 0, word=True)
    elif byte == OP_CMP_RP_I:
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        ip.cmpBit = cmpByte(r, 0, im, DIRECT | IMMEDIATE)
    elif byte == OP_CMP_RP_I2:
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte(r, 0, (imh, iml), DIRECT | IMMEDIATE, word=True)
    elif byte == OP_CMP_RP_R:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        ip.cmpBit = cmpByte(r1, 0, r2, DIRECT)
    elif byte == OP_CMP_RP_R2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        ip.cmpBit = cmpByte(r1, 0, r2, DIRECT, word=True)
    elif byte == OP_CMP_RP_IP:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte(r, 0, (mh, ml), IMMEDIATE)
    elif byte == OP_CMP_RP_IP2:
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte(r, 0, (mh, ml), IMMEDIATE, word=True)
    elif byte == OP_CMP_RP_RP:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        ip.cmpBit = cmpByte(r1, 0, r2, 0)
    elif byte == OP_CMP_RP_RP2:
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        ip.cmpBit = cmpByte(r1, 0, r2, 0, word=True)
    elif byte == OP_CMP_IP_I:
        (mh, ml, im), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte((mh, ml), IMMEDIATE, im, DIRECT | IMMEDIATE)
    elif byte == OP_CMP_IP_I2:
        (mh, ml, imh, iml), mvIpTo = readBytes([], ip.pos, 4)
        ip.cmpBit = cmpByte((mh, ml), IMMEDIATE, (imh, iml), DIRECT | IMMEDIATE, word=True)
    elif byte == OP_CMP_IP_R:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte((mh, ml), IMMEDIATE, r, DIRECT)
    elif byte == OP_CMP_IP_R2:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte((mh, ml), IMMEDIATE, r, DIRECT, word=True)
    elif byte == OP_CMP_IP_IP:
        (mh1, ml1, mh2, ml2), mvIpTo = readBytes([], ip.pos, 4)
        ip.cmpBit = cmpByte((mh1, ml1), IMMEDIATE, (mh2, ml2), IMMEDIATE)
    elif byte == OP_CMP_IP_IP2:
        (mh1, ml1, mh2, ml2), mvIpTo = readBytes([], ip.pos, 4)
        ip.cmpBit = cmpByte((mh1, ml1), IMMEDIATE, (mh2, ml2), IMMEDIATE, word=True)
    elif byte == OP_CMP_IP_RP:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte((mh, ml), IMMEDIATE, r, 0)
    elif byte == OP_CMP_IP_RP2:
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        ip.cmpBit = cmpByte((mh, ml), IMMEDIATE, r, 0, word=True)
    elif byte == OP_JMP:
        (jh, jl), mvIpTo = readBytes([], ip.pos, 2)
        mvIpTo = jmp(mvIpTo, jmpByte(ip.cmpBit, jh, jl, JMP))
    elif byte == OP_JE:
        (jh, jl), mvIpTo = readBytes([], ip.pos, 2)
        mvIpTo = jmp(mvIpTo, jmpByte(ip.cmpBit, jh, jl, EQUAL))
    elif byte == OP_JL:
        (jh, jl), mvIpTo = readBytes([], ip.pos, 2)
        mvIpTo = jmp(mvIpTo, jmpByte(ip.cmpBit, jh, jl, LESS))
    elif byte == OP_JG:
        (jh, jl), mvIpTo = readBytes([], ip.pos, 2)
        mvIpTo = jmp(mvIpTo, jmpByte(ip.cmpBit, jh, jl, GREATER))
    elif byte == OP_JNE:
        (jh, jl), mvIpTo = readBytes([], ip.pos, 2)
        mvIpTo = jmp(mvIpTo, jmpByte(ip.cmpBit, jh, jl, ~EQUAL))
    elif byte == OP_JLE:
        (jh, jl), mvIpTo = readBytes([], ip.pos, 2)
        mvIpTo = jmp(mvIpTo, jmpByte(ip.cmpBit, jh, jl, EQUAL | LESS))
    elif byte == OP_JGE:
        (jh, jl), mvIpTo = readBytes([], ip.pos, 2)
        mvIpTo = jmp(mvIpTo, jmpByte(ip.cmpBit, jh, jl, EQUAL | GREATER))
    elif byte == OP_INC_R:
        (r,), mvIpTo = readBytes([], ip.pos, 1)
        movByte(r, DIRECT, 1, DIRECT | IMMEDIATE, add, plId)
    elif byte == OP_INC_RP:
        (r,), mvIpTo = readBytes([], ip.pos, 1)
        movByte(r, 0, 1, DIRECT | IMMEDIATE, add, plId)
    elif byte == OP_INC_IP:
        (mh, ml), mvIpTo = readBytes([], ip.pos, 2)
        movByte((mh, ml), IMMEDIATE, 1, DIRECT | IMMEDIATE, add, plId)
    elif byte == OP_INC_R2:
        (r,), mvIpTo = readBytes([], ip.pos, 1)
        movByte(r, DIRECT, (0, 1), DIRECT | IMMEDIATE, add, plId, word=True)
    elif byte == OP_INC_RP2:
        (r,), mvIpTo = readBytes([], ip.pos, 1)
        movByte(r, 0, (0, 1), DIRECT | IMMEDIATE, add, plId, word=True)
    elif byte == OP_INC_IP2:
        (mh, ml), mvIpTo = readBytes([], ip.pos, 2)
        movByte((mh, ml), IMMEDIATE, (0, 1), DIRECT | IMMEDIATE, add, plId, word=True)
    elif byte == OP_DEC_R:
        (r,), mvIpTo = readBytes([], ip.pos, 1)
        movByte(r, DIRECT, 1, DIRECT | IMMEDIATE, sub, plId)
    elif byte == OP_DEC_RP:
        (r,), mvIpTo = readBytes([], ip.pos, 1)
        movByte(r, 0, 1, DIRECT | IMMEDIATE, sub, plId)
    elif byte == OP_DEC_IP:
        (mh, ml), mvIpTo = readBytes([], ip.pos, 2)
        movByte((mh, ml), IMMEDIATE, 1, DIRECT | IMMEDIATE, sub, plId)
    elif byte == OP_DEC_R2:
        (r,), mvIpTo = readBytes([], ip.pos, 1)
        movByte(r, DIRECT, (0, 1), DIRECT | IMMEDIATE, sub, plId, word=True)
    elif byte == OP_DEC_RP2:
        (r,), mvIpTo = readBytes([], ip.pos, 1)
        movByte(r, 0, (0, 1), DIRECT | IMMEDIATE, sub, plId, word=True)
    elif byte == OP_DEC_IP2:
        (mh, ml), mvIpTo = readBytes([], ip.pos, 2)
        movByte((mh, ml), IMMEDIATE, (0, 1), DIRECT | IMMEDIATE, sub, plId, word=True)
    else:
        return
    ip.pos = mvIpTo

def readBytes(b, pos, n):
    if pos[1]+1 == szBlock:
        if pos[0]+1 == szMem:
            raise IpDeadError
        pos = (pos[0]+1, 0)
    else:
        pos = (pos[0], pos[1]+1)
    b.append(mem[pos[0]][pos[1]])
    n-=1
    if n == 0:
        return b, pos
    return readBytes(b, pos, n)

def movByte(dst, dmode, src, smode, op, plId, word=False):
    if word:
        if smode & DIRECT:
            if smode & IMMEDIATE:
                s = src[0]*0x100 + src[1]
            else:
                if src+2 >= szReg:
                    raise IpDeadError
                s = regs[src]*0x100 + regs[src+1]
        else:
            if smode & IMMEDIATE:
                m = src[0]*0x100 + src[1]
            else:
                if src+2 >= szReg:
                    raise IpDeadError
                m = regs[src]*0x100 + regs[src+1]
            if m+2 >= szBlock*szMem:
                raise IpDeadError
            s = mem[m // szBlock][m % szBlock]*0x100 + mem[(m+1) // szBlock][m+1 % szBlock]
        if dmode & DIRECT: #Must be REG
            if dst+2 >= szReg:
                raise IpDeadError
            d = regs[dst]*0x100 + regs[dst+1]
            o = op(d, s, 0x10000)
            regs[dst] = o // 0x100
            regs[dst+1] = o % 0x100
        else:
            if dmode & IMMEDIATE:
                m = dst[0]*0x100 + dst[1]
            else:
                if dst+2 >= szReg:
                    raise IpDeadError
                m = regs[dst]*0x100 + regs[dst+1]
            if m+2 >= szBlock*szMem:
                raise IpDeadError
            d = mem[m // szBlock][m % szBlock]*0x100 + mem[(m+1) // szBlock][m+1 % szBlock]
            o = op(d, s, 0x10000)
            mem[m // szBlock][m % szBlock] = o // 0x100
            mem[(m+1) // szBlock][m+1 % szBlock] = o % 0x100
            for i, player in enumerate(players):
                player.mem[m // szBlock][m % szBlock].change = plId
                player.mem[(m+1) // szBlock][m+1 % szBlock].change = plId
    else:
        if smode & DIRECT:
            if smode & IMMEDIATE:
                s = src
            else:
                if src+1 >= szReg:
                    raise IpDeadError
                s = regs[src]
        else:
            if smode & IMMEDIATE:
                m = src[0]*0x100 + src[1]
            else:
                if src+2 >= szReg:
                    raise IpDeadError
                m = regs[src]*0x100 + regs[src+1]
            if m+1 >= szBlock*szMem:
                raise IpDeadError
            s = mem[m // szBlock][m % szBlock]
        if dmode & DIRECT: #Must be REG
            if dst+1 >= szReg:
                raise IpDeadError
            regs[dst] = op(regs[dst], s, 0x100)
        else:
            if dmode & IMMEDIATE:
                m = dst[0]*0x100 + dst[1]
            else:
                if dst+2 >= szReg:
                    raise IpDeadError
                m = regs[dst]*0x100 + regs[dst+1]
            if m+1 >= szBlock*szMem:
                raise IpDeadError
            mem[m // szBlock][m % szBlock] = op(mem[m // szBlock][m % szBlock], s, 0x100)
            for i, player in enumerate(players):
                player.mem[m // szBlock][m % szBlock].change = plId

def cmpByte(dst, dmode, src, smode, word=False):
    c = [None, None]
    if word:
        for i, (p, mode) in enumerate(((dst, dmode), (src, smode))):
            if mode & DIRECT:
                if mode & IMMEDIATE:
                    c[i] = p[0]*0x100 + p[1]
                else:
                    if p+2 >= szReg:
                        raise IpDeadError
                    c[i] = regs[p]*0x100 + regs[p+1]
            else:
                if mode & IMMEDIATE:
                    m = p[0]*0x100 + p[1]
                else:
                    if p+2 >= szReg:
                        raise IpDeadError
                    m = regs[p]*0x100 + regs[p+1]
                if m+2 >= szBlock*szMem:
                    raise IpDeadError
                c[i] = mem[m // szBlock][m % szBlock]*0x100 + mem[(m+1) // szBlock][m+1 % szBlock]
    else:
        for i, (p, mode) in enumerate(((dst, dmode), (src, smode))):
            if mode & DIRECT:
                if mode & IMMEDIATE:
                    c[i] = p
                else:
                    if p+1 >= szReg:
                        raise IpDeadError
                    c[i] = regs[p]
            else:
                if mode & IMMEDIATE:
                    m = p[0]*0x100 + p[1]
                else:
                    if p+2 >= szReg:
                        raise IpDeadError
                    m = regs[p]*0x100 + regs[p+1]
                if m+1 >= szBlock*szMem:
                    raise IpDeadError
                c[i] = mem[m // szBlock][m % szBlock]
    if c[0] > c[1]:
        return GREATER
    elif c[0] < c[1]:
        return LESS
    else:
        return EQUAL

def jmpByte(cmpBit, jh, jl, flags):
    j = jh*0x100 + jl - 1
    if j+1 >= szBlock*szMem:
        raise IpDeadError
    if cmpBit & flags:
        return (j // szBlock, j % szBlock)
    else:
        return None

def turn(plId):
    player = players[plId]
    plMem = player.mem
    cy, cx = 0, 0
    ax = 0
    attr = scr.inch(0,0)
    skipMvCursor = False
    while True:
        if not skipMvCursor:
            curs = player.curs
            scr.chgat(cy, cx, 2, attr)
            cy, cx = memToScr[curs]
            cx -= 3
            scr.addstr(ax, 3*maxCol+38, ' ')
            ax = memToAsm[curs[1]]
        attr = scr.inch(cy, cx)
        scr.chgat(cy, cx, 2, curses.color_pair(CURS_COLOR))
        scr.addstr(ax, 3*maxCol+38, '<')
        skipMvCursor = False
        scr.refresh()

        c = scr.getch()
        if c == curses.KEY_RIGHT:
            if curs[1]+1 == szBlock:
                if curs[0]+1 != szMem:
                    player.curs = (curs[0]+1, 0)
                    interpretBlock(player.curs[0], player)
            else:
                player.curs = (curs[0], curs[1]+1)
        elif c == curses.KEY_LEFT:
            if curs[1] == 0:
                if curs[0] != 0:
                    player.curs = (curs[0]-1, szBlock-1)
                    interpretBlock(player.curs[0], player)
            else:
                player.curs = (curs[0], curs[1]-1)
        elif c == curses.KEY_DOWN:
            if curs[1]+maxCol >= szBlock:
                if curs[0]+1 != szMem:
                    player.curs = (curs[0]+1, maxCol-szBlock+curs[1])
                    interpretBlock(player.curs[0], player)
            else:
                player.curs = (curs[0], curs[1]+maxCol)
        elif c == curses.KEY_UP:
            if curs[1]-maxCol < 0:
                if curs[0] != 0:
                    player.curs = (curs[0]-1, szBlock+curs[1]-maxCol)
                    interpretBlock(player.curs[0], player)
            else:
                player.curs = (curs[0], curs[1]-maxCol)
        elif c == KEY_ESC:
            return True
        elif c == ord('n'):
            return False
        elif c == KEY_ENTER:
            scr.addstr(cmdyx[0]+4, cmdyx[1], '> ')
            curses.echo()
            curses.curs_set(1)
            r = scr.getstr(cmdyx[0]+4, cmdyx[1]+2)
            try:
                runCmd(r, curs, plId)
            except:
                pass #TODO: Add some colourful err msg
            printMem(plId)
            printUI(plId)
            interpretBlock(player.curs[0], player)
            curses.noecho()
            curses.curs_set(0)
            scr.addstr(cmdyx[0]+4, cmdyx[1], '\n')
            scr.deleteln()
            skipMvCursor = True

def interpretBlock(blId, player):
    global memToAsm
    memToAsm = dict()
    shift = 0
    for i in range(szBlock):
        scr.addstr(3+i, maxCol*3+16, ' '*30)
    scr.move(3, maxCol*3+16)
    while True:
        if shift >= szBlock:
            return
        scr.move(scr.getyx()[0], maxCol*3+40)
        scr.addstr('%0#6x' % (blId*szBlock+shift))
        scr.move(scr.getyx()[0], maxCol*3+16)
        if player.mem[blId][shift].hidden:
            scr.addstr('??')
            memToAsm[shift] = scr.getyx()[0]
            scr.move(scr.getyx()[0]+1, maxCol*3+16)
            shift += 1
            continue
        byte = mem[blId][shift]
        if byte == OP_MOV_R_I:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=DIRECT, src=(DIRECT | IMMEDIATE))
        elif byte == OP_MOV_R_I2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_MOV_R_R:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=DIRECT, src=DIRECT)
        elif byte == OP_MOV_R_R2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=DIRECT, word=True)
        elif byte == OP_MOV_R_IP:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=DIRECT, src=IMMEDIATE)
        elif byte == OP_MOV_R_IP2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=IMMEDIATE, word=True)
        elif byte == OP_MOV_R_RP:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=DIRECT, src=0)
        elif byte == OP_MOV_R_RP2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=0, word=True)
        elif byte == OP_MOV_RP_I:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=0, src=(DIRECT | IMMEDIATE))
        elif byte == OP_MOV_RP_I2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=0, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_MOV_RP_R:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=0, src=DIRECT)
        elif byte == OP_MOV_RP_R2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=0, src=DIRECT, word=True)
        elif byte == OP_MOV_RP_IP:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=0, src=IMMEDIATE)
        elif byte == OP_MOV_RP_IP2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=0, src=IMMEDIATE, word=True)
        elif byte == OP_MOV_RP_RP:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=0, src=0)
        elif byte == OP_MOV_RP_RP2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=0, src=0, word=True)
        elif byte == OP_MOV_IP_I:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=(DIRECT | IMMEDIATE))
        elif byte == OP_MOV_IP_I2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_MOV_IP_R:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=DIRECT)
        elif byte == OP_MOV_IP_R2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=DIRECT, word=True)
        elif byte == OP_MOV_IP_IP:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=IMMEDIATE)
        elif byte == OP_MOV_IP_IP2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=IMMEDIATE, word=True)
        elif byte == OP_MOV_IP_RP:
            shift = interpretByte('mov', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=0)
        elif byte == OP_MOV_IP_RP2:
            shift = interpretByte('movw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=0, word=True)
        elif byte == OP_ADD_R_I:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=DIRECT, src=(DIRECT | IMMEDIATE))
        elif byte == OP_ADD_R_I2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_ADD_R_R:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=DIRECT, src=DIRECT)
        elif byte == OP_ADD_R_R2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=DIRECT, word=True)
        elif byte == OP_ADD_R_IP:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=DIRECT, src=IMMEDIATE)
        elif byte == OP_ADD_R_IP2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=IMMEDIATE, word=True)
        elif byte == OP_ADD_R_RP:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=DIRECT, src=0)
        elif byte == OP_ADD_R_RP2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=0, word=True)
        elif byte == OP_ADD_RP_I:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=0, src=(DIRECT | IMMEDIATE))
        elif byte == OP_ADD_RP_I2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=0, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_ADD_RP_R:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=0, src=DIRECT)
        elif byte == OP_ADD_RP_R2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=0, src=DIRECT, word=True)
        elif byte == OP_ADD_RP_IP:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=0, src=IMMEDIATE)
        elif byte == OP_ADD_RP_IP2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=0, src=IMMEDIATE, word=True)
        elif byte == OP_ADD_RP_RP:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=0, src=0)
        elif byte == OP_ADD_RP_RP2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=0, src=0, word=True)
        elif byte == OP_ADD_IP_I:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=(DIRECT | IMMEDIATE))
        elif byte == OP_ADD_IP_I2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_ADD_IP_R:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=DIRECT)
        elif byte == OP_ADD_IP_R2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=DIRECT, word=True)
        elif byte == OP_ADD_IP_IP:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=IMMEDIATE)
        elif byte == OP_ADD_IP_IP2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=IMMEDIATE, word=True)
        elif byte == OP_ADD_IP_RP:
            shift = interpretByte('add', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=0)
        elif byte == OP_ADD_IP_RP2:
            shift = interpretByte('addw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=0, word=True)
        elif byte == OP_SUB_R_I:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=DIRECT, src=(DIRECT | IMMEDIATE))
        elif byte == OP_SUB_R_I2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_SUB_R_R:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=DIRECT, src=DIRECT)
        elif byte == OP_SUB_R_R2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=DIRECT, word=True)
        elif byte == OP_SUB_R_IP:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=DIRECT, src=IMMEDIATE)
        elif byte == OP_SUB_R_IP2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=IMMEDIATE, word=True)
        elif byte == OP_SUB_R_RP:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=DIRECT, src=0)
        elif byte == OP_SUB_R_RP2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=0, word=True)
        elif byte == OP_SUB_RP_I:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=0, src=(DIRECT | IMMEDIATE))
        elif byte == OP_SUB_RP_I2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=0, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_SUB_RP_R:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=0, src=DIRECT)
        elif byte == OP_SUB_RP_R2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=0, src=DIRECT, word=True)
        elif byte == OP_SUB_RP_IP:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=0, src=IMMEDIATE)
        elif byte == OP_SUB_RP_IP2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=0, src=IMMEDIATE, word=True)
        elif byte == OP_SUB_RP_RP:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=0, src=0)
        elif byte == OP_SUB_RP_RP2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=0, src=0, word=True)
        elif byte == OP_SUB_IP_I:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=(DIRECT | IMMEDIATE))
        elif byte == OP_SUB_IP_I2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_SUB_IP_R:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=DIRECT)
        elif byte == OP_SUB_IP_R2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=DIRECT, word=True)
        elif byte == OP_SUB_IP_IP:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=IMMEDIATE)
        elif byte == OP_SUB_IP_IP2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=IMMEDIATE, word=True)
        elif byte == OP_SUB_IP_RP:
            shift = interpretByte('sub', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=0)
        elif byte == OP_SUB_IP_RP2:
            shift = interpretByte('subw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=0, word=True)
        elif byte == OP_CMP_R_I:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=DIRECT, src=(DIRECT | IMMEDIATE))
        elif byte == OP_CMP_R_I2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_CMP_R_R:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=DIRECT, src=DIRECT)
        elif byte == OP_CMP_R_R2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=DIRECT, word=True)
        elif byte == OP_CMP_R_IP:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=DIRECT, src=IMMEDIATE)
        elif byte == OP_CMP_R_IP2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=IMMEDIATE, word=True)
        elif byte == OP_CMP_R_RP:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=DIRECT, src=0)
        elif byte == OP_CMP_R_RP2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=DIRECT, src=0, word=True)
        elif byte == OP_CMP_RP_I:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=0, src=(DIRECT | IMMEDIATE))
        elif byte == OP_CMP_RP_I2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=0, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_CMP_RP_R:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=0, src=DIRECT)
        elif byte == OP_CMP_RP_R2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=0, src=DIRECT, word=True)
        elif byte == OP_CMP_RP_IP:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=0, src=IMMEDIATE)
        elif byte == OP_CMP_RP_IP2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=0, src=IMMEDIATE, word=True)
        elif byte == OP_CMP_RP_RP:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=0, src=0)
        elif byte == OP_CMP_RP_RP2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=0, src=0, word=True)
        elif byte == OP_CMP_IP_I:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=(DIRECT | IMMEDIATE))
        elif byte == OP_CMP_IP_I2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=(DIRECT | IMMEDIATE), word=True)
        elif byte == OP_CMP_IP_R:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=DIRECT)
        elif byte == OP_CMP_IP_R2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=DIRECT, word=True)
        elif byte == OP_CMP_IP_IP:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=IMMEDIATE)
        elif byte == OP_CMP_IP_IP2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=IMMEDIATE, word=True)
        elif byte == OP_CMP_IP_RP:
            shift = interpretByte('cmp', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=0)
        elif byte == OP_CMP_IP_RP2:
            shift = interpretByte('cmpw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, src=0, word=True)
        elif byte == OP_JMP:
            shift = interpretByte('jmp', mem[blId], shift, player.mem[blId], dst=IMMEDIATE)
        elif byte == OP_JE:
            shift = interpretByte('je', mem[blId], shift, player.mem[blId], dst=IMMEDIATE)
        elif byte == OP_JL:
            shift = interpretByte('jl', mem[blId], shift, player.mem[blId], dst=IMMEDIATE)
        elif byte == OP_JG:
            shift = interpretByte('jg', mem[blId], shift, player.mem[blId], dst=IMMEDIATE)
        elif byte == OP_JNE:
            shift = interpretByte('jne', mem[blId], shift, player.mem[blId], dst=IMMEDIATE)
        elif byte == OP_JLE:
            shift = interpretByte('jle', mem[blId], shift, player.mem[blId], dst=IMMEDIATE)
        elif byte == OP_JGE:
            shift = interpretByte('jge', mem[blId], shift, player.mem[blId], dst=IMMEDIATE)
        elif byte == OP_INC_R:
            shift = interpretByte('inc', mem[blId], shift, player.mem[blId], dst=DIRECT)
        elif byte == OP_INC_RP:
            shift = interpretByte('inc', mem[blId], shift, player.mem[blId], dst=0)
        elif byte == OP_INC_IP:
            shift = interpretByte('inc', mem[blId], shift, player.mem[blId], dst=IMMEDIATE)
        elif byte == OP_INC_R2:
            shift = interpretByte('incw', mem[blId], shift, player.mem[blId], dst=DIRECT, word=True)
        elif byte == OP_INC_RP2:
            shift = interpretByte('incw', mem[blId], shift, player.mem[blId], dst=0, word=True)
        elif byte == OP_INC_IP2:
            shift = interpretByte('incw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, word=True)
        elif byte == OP_DEC_R:
            shift = interpretByte('dec', mem[blId], shift, player.mem[blId], dst=DIRECT)
        elif byte == OP_DEC_RP:
            shift = interpretByte('dec', mem[blId], shift, player.mem[blId], dst=0)
        elif byte == OP_DEC_IP:
            shift = interpretByte('dec', mem[blId], shift, player.mem[blId], dst=IMMEDIATE)
        elif byte == OP_DEC_R2:
            shift = interpretByte('decw', mem[blId], shift, player.mem[blId], dst=DIRECT, word=True)
        elif byte == OP_DEC_RP2:
            shift = interpretByte('decw', mem[blId], shift, player.mem[blId], dst=0, word=True)
        elif byte == OP_DEC_IP2:
            shift = interpretByte('decw', mem[blId], shift, player.mem[blId], dst=IMMEDIATE, word=True)
        else:
            scr.addstr('%02x' % byte)
            memToAsm[shift] = scr.getyx()[0]
            scr.move(scr.getyx()[0]+1, maxCol*3+16)
        shift += 1

def interpretByte(instr, block, shift, plBlock, dst=None, src=None, word=False):
    memToAsm[shift] = scr.getyx()[0]
    scr.addstr(instr+' ')
    if dst is None:
        scr.move(scr.getyx()[0]+1, maxCol*3+16)
        return shift
    else:
        shift += 1
        if shift == szBlock or plBlock[shift].hidden:
            scr.move(scr.getyx()[0]+1, maxCol*3+16)
            return shift-1
        d = block[shift]
        memToAsm[shift] = scr.getyx()[0]
    if not (dst & DIRECT):
        scr.addstr('*')
    if dst & IMMEDIATE:
        shift += 1
        if shift == szBlock or plBlock[shift].hidden:
            scr.move(scr.getyx()[0]+1, maxCol*3+16)
            return shift-1
        memToAsm[shift] = scr.getyx()[0]
        scr.addstr('%0#6x' % (d*0x100 + block[shift]))
    else:
        scr.addstr('r%x' % d)

    if src is None:
        scr.move(scr.getyx()[0]+1, maxCol*3+16)
        return shift
    else:
        shift += 1
        if shift == szBlock or plBlock[shift].hidden:
            scr.move(scr.getyx()[0]+1, maxCol*3+16)
            return shift-1
        memToAsm[shift] = scr.getyx()[0]
        s = block[shift]
        scr.addstr(', ')
    if not (src & DIRECT):
        scr.addstr('*')
    if src & IMMEDIATE:
        if word:
            shift += 1
            if shift == szBlock or plBlock[shift].hidden:
                scr.move(scr.getyx()[0]+1, maxCol*3+16)
                return shift-1
            memToAsm[shift] = scr.getyx()[0]
            scr.addstr('%0#6x' % (s*0x100 + block[shift]))
        else:
            scr.addstr('%0#4x' % s)
    else:
        scr.addstr('r%x' % s)
    scr.move(scr.getyx()[0]+1, maxCol*3+16)
    return shift

def runCmd(r, curs, plId):
    player = players[plId]
    cost = 1 #May be changed
    try:
        h = int(r, 16)
        if h > 0xff:
            raise NotByteError
        if player.tokens < cost:
            raise TooFewTokens
    except ValueError:
        words = r.decode().lower().replace(',', '').split()
        toWrt = [None]
        if words[0][:3] == 'mov':
            toWrt[0] = OP_MOV
        elif words[0][:3] == 'add':
            toWrt[0] = OP_ADD
        elif words[0][:3] == 'sub':
            toWrt[0] = OP_SUB
        elif words[0][:3] == 'cmp':
            toWrt[0] = OP_CMP
        if toWrt[0] is None:
            isSmall = True
            shift_word = OP_WORD_SHIFT_SMALL
            shift_indirect_dst = OP_INDIRECT_SHIFT_SMALL
            shift_immediate_dst = OP_IMMEDIATE_SHIFT_SMALL
            if words[0][:3] == 'inc':
                toWrt[0] = OP_INC
            elif words[0][:3] == 'dec':
                toWrt[0] = OP_DEC
        else:
            isSmall = False
            shift_word = OP_WORD_SHIFT
            shift_indirect_dst = OP_INDIRECT_SHIFT_DST
            shift_immediate_dst = OP_IMMEDIATE_SHIFT_DST
            shift_indirect_src = OP_INDIRECT_SHIFT_SRC
            shift_register_src = OP_REGISTER_SHIFT_SRC
        if toWrt[0] is not None:
            if words[0][3:] == 'w':
                toWrt[0] += shift_word
                isWord = True
            else:
                isWord = False
            dst = words[1]
            if dst[0] == '*':
                toWrt[0] += shift_indirect_dst
                dst = dst[1:]
            elif dst[0] != 'r':
                toWrt[0] += shift_indirect_dst
            if dst[0] != 'r':
                toWrt[0] += shift_immediate_dst
                im = int(dst, 16)
                if im > 0xffff:
                    raise NotByteError
                toWrt.append(im // 0x100)
                toWrt.append(im % 0x100)
            else:
                reg = int(dst[1], 16)
                if reg > 0xff:
                    raise NotByteError
                toWrt.append(reg)
            if not isSmall:
                src = words[2]
                if src[0] == '*':
                    toWrt[0] += shift_indirect_src
                    src = src[1:]
                if src[0] == 'r':
                    toWrt[0] += shift_register_src
                    reg = int(src[1], 16)
                    if reg > 0xff:
                        raise NotByteError
                    toWrt.append(reg)
                else:
                    im = int(src, 16)
                    if isWord:
                        if im > 0xffff:
                            raise NotByteError
                        toWrt.append(im // 0x100)
                        toWrt.append(im % 0x100)
                    else:
                        if im > 0xff:
                            raise NotByteError
                        toWrt.append(im)
        else:
            if words[0] == 'jmp':
                toWrt[0] = OP_JMP
            elif words[0] == 'je':
                toWrt[0] = OP_JE
            elif words[0] == 'jl':
                toWrt[0] = OP_JL
            elif words[0] == 'jg':
                toWrt[0] = OP_JG
            elif words[0] == 'jne':
                toWrt[0] = OP_JNE
            elif words[0] == 'jle':
                toWrt[0] = OP_JLE
            elif words[0] == 'jge':
                toWrt[0] = OP_JGE
            else:
                raise UnknownInstruction
            im = int(words[1].replace('*', ''), 16)
            if im > 0xffff:
                raise NotByteError
            toWrt.append(im // 0x100)
            toWrt.append(im % 0x100)
        l = len(toWrt)
        c = curs[0]*szBlock + curs[1]
        if c+l > szBlock*szMem:
            raise IndexError
        calculatedCost = 0
        for shift, m in enumerate(toWrt):
            if mem[(c + shift) // szBlock][(c + shift) % szBlock] != m or \
                player.mem[(c + shift) // szBlock][(c + shift) % szBlock].hidden:
                    calculatedCost += cost
        if calculatedCost > player.tokens:
            raise TooFewTokens
        player.tokens -= calculatedCost
        for shift, m in enumerate(toWrt):
            if mem[(c + shift) // szBlock][(c + shift) % szBlock] != m or \
                player.mem[(c + shift) // szBlock][(c + shift) % szBlock].hidden:
                mem[(c + shift) // szBlock][(c + shift) % szBlock] = m
                player.mem[(c + shift) // szBlock][(c + shift) % szBlock].hidden = False
                for i, pl in enumerate(players):
                    pl.mem[(c + shift) // szBlock][(c + shift) % szBlock].im = True
                    pl.mem[(c + shift) // szBlock][(c + shift) % szBlock].change = plId

    else:
        player.tokens -= cost
        mem[curs[0]][curs[1]] = h
        player.mem[curs[0]][curs[1]].hidden = False
        for i, pl in enumerate(players):
            pl.mem[curs[0]][curs[1]].im = True
            pl.mem[curs[0]][curs[1]].change = plId

def main_loop():
    while True:
        for i, player in enumerate(players):
            printMem(i)
            printUI(i)
            interpretBlock(player.curs[0], player)
            if turn(i):
                return
            for block in player.mem:
                block.hidden = True
                for byte in block:
                    byte.reset()
            player.tokens = nTokens
            run(i)

def init():
    global mem
    global blPrivs
    global players
    global ips
    global regs
    global scr
    mem = [[0]*szBlock for i in range(szMem)]
    blPrivs = [NORMAL]*szMem
    players = [Player(name='%x' % i) for i in range(2)]
    ips = [Ip((0,0x0), 0), Ip((0,0x5), 1)]
    regs = [0]*szReg

    for ip in ips:
        for i, pl in enumerate(players):
            if i == ip.owner:
                pl.mem[ip.pos[0]][ip.pos[1]].my_ip = True
            else:
                pl.mem[ip.pos[0]][ip.pos[1]].o_ip = True
        plMem = players[ip.owner].mem
        plMem[ip.pos[0]].hidden = False
        if ip.pos[1]+ipFov >= szBlock:
            for i in range(ip.pos[1], szBlock):
                plMem[ip.pos[0]][i].hidden = False
        else:
            for i in range(ip.pos[1], ip.pos[1]+ipFov):
                plMem[ip.pos[0]][i].hidden = False

    scr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    scr.keypad(1)
    curses.start_color()
    curses.use_default_colors()
    for i in range(curses.COLORS):
        curses.init_pair(i+1, i, -1)
    curses.init_pair(255, 0, 255)

def clean_exit():
    curses.echo()
    curses.nocbreak()
    curses.curs_set(1)
    scr.keypad(0)
    curses.endwin()


def main():
    init()
    main_loop()
    clean_exit()

main()

