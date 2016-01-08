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

OP_MOV_R_I = 0x10 #TODO: Finish adding MOV/ADD WORD
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
OP_MOV_R_I2 = 0x1c
OP_MOV_RP_I2 = 0x1d
OP_MOV_IP_I2 = 0x1e
OP_ADD_R_I = 0x20
OP_ADD_R_R = 0x21
OP_ADD_R_IP = 0x22
OP_ADD_R_RP = 0x23
OP_ADD_RP_I = 0x24
OP_ADD_RP_R = 0x25
OP_ADD_RP_IP = 0x26
OP_ADD_RP_RP = 0x27
OP_ADD_IP_I = 0x28
OP_ADD_IP_R = 0x29
OP_ADD_IP_IP = 0x2a
OP_ADD_IP_RP = 0x2b
OP_ADD_R_I2 = 0x2c
OP_ADD_RP_I2 = 0x2d
OP_ADD_IP_I2 = 0x2e

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
    if byte == OP_MOV_R_I: #MOV REG, IM
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        if r+1 >= szReg:
            raise IpDeadError
        regs[r] = im
        ip.pos = mvIpTo
    elif byte == OP_MOV_R_I2: #MOV REG, IM2
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        if r+2 >= szReg:
            raise IpDeadError
        regs[r] = imh
        regs[r+1] = iml
        ip.pos = mvIpTo
    elif byte == OP_MOV_R_R: #MOV REG, REG
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        if r1+1 >= szReg or r2+1 >= szReg:
            raise IpDeadError
        regs[r1] = regs[r2]
        ip.pos = mvIpTo
    elif byte == OP_MOV_R_IP: #MOV REG, [IM]
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        m = mh*0x100+ml
        if r+1 >= szReg or m+1 >= szMem*szBlock:
            raise IpDeadError
        regs[r] = mem[m // szBlock][m % szBlock]
        ip.pos = mvIpTo
    elif byte == OP_MOV_R_RP: #MOV REG, [REG]
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        if r1+1 >= szReg or r2+2 >= szReg:
            raise IpDeadError
        m = regs[r2]*0x100+regs[r2+1]
        if m+1 >= szMem*szBlock:
            raise IpDeadError
        regs[r1] = mem[m // szBlock][m % szBlock]
        ip.pos = mvIpTo
    elif byte == OP_MOV_RP_I: #MOV [REG], IM
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        if r+2 >= szReg:
            raise IpDeadError
        md = regs[r]*0x100+regs[r+1]
        if md+1 >= szMem*szBlock:
            raise IpDeadError
        mem[md // szBlock][md % szBlock] = im
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[md // szBlock][md % szBlock].change = plId
    elif byte == OP_MOV_RP_I2: #MOV [REG], IM2
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        if r+1 >= szReg:
            raise IpDeadError
        md = regs[r]*0x100+regs[r+1]
        if md+2 >= szMem*szBlock:
            raise IpDeadError
        mem[md // szBlock][md % szBlock] = imh
        mem[(md+1) // szBlock][md+1 % szBlock] = iml
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[md // szBlock][md % szBlock].change = plId
            player.mem[(md+1) // szBlock][md+1 % szBlock].change = plId
    elif byte == OP_MOV_RP_R: #MOV [REG], REG
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        if r1+2 >= szReg or r2+1 >= szReg:
            raise IpDeadError
        md = regs[r1]*0x100+regs[r1+1]
        if md+1 >= szMem*szBlock:
            raise IpDeadError
        mem[md // szBlock][md % szBlock] = regs[r2]
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[md // szBlock][md % szBlock].change = plId
    elif byte == OP_MOV_RP_IP: #MOV [REG], [IM]
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        m = mh*0x100+ml
        if r+2 >= szReg or m+1 >= szMem*szBlock:
            raise IpDeadError
        md = regs[r]*0x100+regs[r+1]
        if md+1 >= szMem*szBlock:
            raise IpDeadError
        mem[md // szBlock][md % szBlock] = mem[m // szBlock][m % szBlock]
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[md // szBlock][md % szBlock].change = plId
    elif byte == OP_MOV_RP_RP: #MOV [REG], [REG]
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        if r1+2 >= szReg or r2+2 >= szReg:
            raise IpDeadError
        md1 = regs[r1]*0x100+regs[r1+1]
        md2 = regs[r2]*0x100+regs[r2+1]
        if md1+1 >= szMem*szBlock or md2+1 >= szMem*szBlock:
            raise IpDeadError
        mem[md1 // szBlock][md1 % szBlock] = mem[md2 // szBlock][md2 % szBlock]
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[md1 // szBlock][md1 % szBlock].change = plId
    elif byte == OP_MOV_IP_I: #MOV [IM], IM
        (mh, ml, im), mvIpTo = readBytes([], ip.pos, 3)
        m = mh*0x100+ml
        if m+1 >= szMem*szBlock:
            raise IpDeadError
        mem[m // szBlock][m % szBlock] = im
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[m // szBlock][m % szBlock].change = plId
    elif byte == OP_MOV_IP_I2: #MOV [IM], IM2
        (mh, ml, imh, iml), mvIpTo = readBytes([], ip.pos, 4)
        m = mh*0x100+ml
        if m+2 >= szMem*szBlock:
            raise IpDeadError
        mem[m // szBlock][m % szBlock] = imh
        mem[(m+1) // szBlock][m+1 % szBlock] = iml
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[m // szBlock][m % szBlock].change = plId
            player.mem[(m+1) // szBlock][m+1 % szBlock].change = plId
    elif byte == OP_MOV_IP_R: #MOV [IM], REG
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        m = mh*0x100+ml
        if r+1 >= szReg or m+1 >= szMem*szBlock:
            raise IpDeadError
        mem[m // szBlock][m % szBlock] = regs[r]
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[m // szBlock][m % szBlock].change = plId
    elif byte == OP_MOV_IP_IP: #MOV [IM], [IM]
        (mh1, ml1, mh2, ml2), mvIpTo = readBytes([], ip.pos, 4)
        m1 = mh1*0x100+ml1
        m2 = mh2*0x100+ml2
        if m1+1 >= szMem*szBlock or m2+1 >= szMem*szBlock:
            raise IpDeadError
        mem[m1 // szBlock][m1 % szBlock] = mem[m2 // szBlock][m2 % szBlock]
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[m1 // szBlock][m1 % szBlock].change = plId
    elif byte == OP_MOV_IP_RP: #MOV [IM], [REG]
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        m = mh*0x100+ml
        if r+2 >= szReg or m+1 >= szMem*szBlock:
            raise IpDeadError
        md = regs[r]*0x100+regs[r+1]
        if md+1 >= szMem*szBlock:
            raise IpDeadError
        mem[m // szBlock][m % szBlock] = mem[md // szBlock][md % szBlock]
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[m // szBlock][m % szBlock].change = plId
    elif byte == OP_ADD_R_I: #ADD REG, IM
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        if r+1 >= szReg:
            raise IpDeadError
        regs[r] = (regs[r] + im) % 0xff
        ip.pos = mvIpTo
    elif byte == OP_ADD_R_I2: #ADD REG, IM2
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        if r+2 >= szReg:
            raise IpDeadError
        im = imh*0x100+iml
        rs = regs[r]*0x100+regs[r+1]
        s = (rs + im) % 0xffff
        regs[r] = s // 0x100
        regs[r+1] = s % 0x100
        ip.pos = mvIpTo
    elif byte == OP_ADD_R_R: #ADD REG, REG
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        if r1+1 >= szReg or r2+1 >= szReg:
            raise IpDeadError
        regs[r1] = (regs[r1] + regs[r2]) % 0xff
        ip.pos = mvIpTo
    elif byte == OP_ADD_R_IP: #ADD REG, [IM]
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        m = mh*0x100+ml
        if r+1 >= szReg or m+1 >= szMem*szBlock:
            raise IpDeadError
        regs[r] = (regs[r] + mem[m // szBlock][m % szBlock]) % 0xff
        ip.pos = mvIpTo
    elif byte == OP_ADD_R_RP: #ADD REG, [REG]
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        if r1+1 >= szReg or r2+2 >= szReg:
            raise IpDeadError
        m = regs[r2]*0x100+regs[r2+1]
        if m+1 >= szMem*szBlock:
            raise IpDeadError
        regs[r1] = (regs[r1] + mem[m // szBlock][m % szBlock]) % 0xff
        ip.pos = mvIpTo
    elif byte == OP_ADD_RP_I: #ADD [REG], IM
        (r, im), mvIpTo = readBytes([], ip.pos, 2)
        if r+2 >= szReg:
            raise IpDeadError
        md = regs[r]*0x100+regs[r+1]
        if md+1 >= szMem*szBlock:
            raise IpDeadError
        mem[md // szBlock][md % szBlock] = (mem[md // szBlock][md % szBlock] + im) % 0xff
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[md // szBlock][md % szBlock].change = plId
    elif byte == OP_ADD_RP_I2: #ADD [REG], IM2
        (r, imh, iml), mvIpTo = readBytes([], ip.pos, 3)
        if r+1 >= szReg:
            raise IpDeadError
        md = regs[r]*0x100+regs[r+1]
        if md+2 >= szMem*szBlock:
            raise IpDeadError
        im = imh*0x100 + iml
        ms = mem[md // szBlock][md % szBlock]*0x100 + mem[(md+1) // szBlock][md+1 % szBlock]
        s = (im + ms) % 0xffff
        mem[md // szBlock][md % szBlock] = s // 0x100
        mem[(md+1) // szBlock][md+1 % szBlock] = s % 0x100
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[md // szBlock][md % szBlock].change = plId
            player.mem[(md+1) // szBlock][md+1 % szBlock].change = plId
    elif byte == OP_ADD_RP_R: #ADD [REG], REG
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        if r1+2 >= szReg or r2+1 >= szReg:
            raise IpDeadError
        md = regs[r1]*0x100+regs[r1+1]
        if md+1 >= szMem*szBlock:
            raise IpDeadError
        mem[md // szBlock][md % szBlock] = (mem[md // szBlock][md % szBlock] + regs[r2]) % 0xff
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[md // szBlock][md % szBlock].change = plId
    elif byte == OP_ADD_RP_IP: #ADD [REG], [IM]
        (r, mh, ml), mvIpTo = readBytes([], ip.pos, 3)
        m = mh*0x100+ml
        if r+2 >= szReg or m+1 >= szMem*szBlock:
            raise IpDeadError
        md = regs[r]*0x100+regs[r+1]
        if md+1 >= szMem*szBlock:
            raise IpDeadError
        mem[md // szBlock][md % szBlock] = (mem[md // szBlock][md % szBlock] + mem[m // szBlock][m % szBlock]) % 0xff
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[md // szBlock][md % szBlock].change = plId
    elif byte == OP_ADD_RP_RP: #ADD [REG], [REG]
        (r1, r2), mvIpTo = readBytes([], ip.pos, 2)
        if r1+2 >= szReg or r2+2 >= szReg:
            raise IpDeadError
        md1 = regs[r1]*0x100+regs[r1+1]
        md2 = regs[r2]*0x100+regs[r2+1]
        if md1+1 >= szMem*szBlock or md2+1 >= szMem*szBlock:
            raise IpDeadError
        mem[md1 // szBlock][md1 % szBlock] = (mem[md1 // szBlock][md1 % szBlock] + mem[md2 // szBlock][md2 % szBlock]) % 0xff
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[md1 // szBlock][md1 % szBlock].change = plId
    elif byte == OP_ADD_IP_I: #ADD [IM], IM
        (mh, ml, im), mvIpTo = readBytes([], ip.pos, 3)
        m = mh*0x100+ml
        if m+1 >= szMem*szBlock:
            raise IpDeadError
        mem[m // szBlock][m % szBlock] = (mem[m // szBlock][m % szBlock] + im) % 0xff
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[m // szBlock][m % szBlock].change = plId
    elif byte == OP_ADD_IP_I2: #ADD [IM], IM2
        (mh, ml, imh, iml), mvIpTo = readBytes([], ip.pos, 4)
        m = mh*0x100+ml
        if m+2 >= szMem*szBlock:
            raise IpDeadError
        im = imh*0x100 + iml
        md = mem[m // szBlock][m % szBlock]*0x100 + mem[(m+1) // szBlock][m+1 % szBlock]
        s = (im + md) % 0xffff
        mem[m // szBlock][m % szBlock] = s // 0x100
        mem[(m+1) // szBlock][m+1 % szBlock] = s % 0x100
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[m // szBlock][m % szBlock].change = plId
            player.mem[(m+1) // szBlock][m+1 % szBlock].change = plId
    elif byte == OP_ADD_IP_R: #ADD [IM], REG
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        m = mh*0x100+ml
        if r+1 >= szReg or m+1 >= szMem*szBlock:
            raise IpDeadError
        mem[m // szBlock][m % szBlock] = (mem[m // szBlock][m % szBlock] + regs[r]) % 0xff
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[m // szBlock][m % szBlock].change = plId
    elif byte == OP_ADD_IP_IP: #ADD [IM], [IM]
        (mh1, ml1, mh2, ml2), mvIpTo = readBytes([], ip.pos, 4)
        m1 = mh1*0x100+ml1
        m2 = mh2*0x100+ml2
        if m1+1 >= szMem*szBlock or m2+1 >= szMem*szBlock:
            raise IpDeadError
        mem[m1 // szBlock][m1 % szBlock] = (mem[m1 // szBlock][m1 % szBlock] + mem[m2 // szBlock][m2 % szBlock]) % 0xff
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[m1 // szBlock][m1 % szBlock].change = plId
    elif byte == OP_ADD_IP_RP: #ADD [IM], [REG]
        (mh, ml, r), mvIpTo = readBytes([], ip.pos, 3)
        m = mh*0x100+ml
        if r+2 >= szReg or m+1 >= szMem*szBlock:
            raise IpDeadError
        md = regs[r]*0x100+regs[r+1]
        if md+1 >= szMem*szBlock:
            raise IpDeadError
        mem[m // szBlock][m % szBlock] = (mem[m // szBlock][m % szBlock] + mem[md // szBlock][md % szBlock]) % 0xff
        ip.pos = mvIpTo
        for i, player in enumerate(players):
            player.mem[m // szBlock][m % szBlock].change = plId
    else:
        pass

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

