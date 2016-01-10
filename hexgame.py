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

szMem = 12
szBlock = 64
szReg = 8
ipFov = 8
nSteps = 1
nTokens= 8

maxCol = 16

class NotByteError(Exception):
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


def turn(plId):
    player = players[plId]
    plMem = player.mem
    cy, cx = 0, 0
    attr = scr.inch(0,0)
    skipMvCursor = False
    while True:
        if not skipMvCursor:
            curs = player.curs
            scr.chgat(cy, cx, 2, attr)
            cy, cx = memToScr[curs]
            cx -= 3
        attr = scr.inch(cy, cx)
        scr.chgat(cy, cx, 2, curses.color_pair(CURS_COLOR))
        skipMvCursor = False
        scr.refresh()

        c = scr.getch()
        if c == curses.KEY_RIGHT:
            if curs[1]+1 == szBlock:
                if curs[0]+1 != szMem:
                    player.curs = (curs[0]+1, 0)
            else:
                player.curs = (curs[0], curs[1]+1)
        elif c == curses.KEY_LEFT:
            if curs[1] == 0:
                if curs[0] != 0:
                    player.curs = (curs[0]-1, szBlock-1)
            else:
                player.curs = (curs[0], curs[1]-1)
        elif c == curses.KEY_DOWN:
            if curs[1]+maxCol >= szBlock:
                if curs[0]+1 != szMem:
                    player.curs = (curs[0]+1, maxCol-szBlock+curs[1])
            else:
                player.curs = (curs[0], curs[1]+maxCol)
        elif c == curses.KEY_UP:
            if curs[1]-maxCol < 0:
                if curs[0] != 0:
                    player.curs = (curs[0]-1, szBlock+curs[1]-maxCol)
            else:
                player.curs = (curs[0], curs[1]-maxCol)
        elif c == KEY_ESC:
            return True
        elif c == ord('n'):
            return False
        elif c == KEY_ENTER:
            scr.addstr(cmdyx[0], cmdyx[1], '> ')
            curses.echo()
            r = scr.getstr(cmdyx[0], cmdyx[1]+2)
            try:
                runCmd(r, curs, plId)
            except:
                pass #TODO: Add some colourful err msg
            printMem(plId)
            printUI(plId)
            curses.noecho()
            scr.addstr(cmdyx[0], cmdyx[1], '\n')
            scr.deleteln()
            skipMvCursor = True

def runCmd(r, curs, plId):
    player = players[plId]
    try:
        h = int(r, 16)
        if h > 0xff:
            raise NotByteError
        cost = 1 #May be changed
        if player.tokens < cost:
            raise TooFewTokens
    except ValueError:
        pass #TODO: Interpret ASM instructions
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
            if turn(i):
                return
            for block in player.mem:
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

