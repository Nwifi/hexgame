#!/usr/bin/python
import curses

NORMAL = 0
KERNEL = -1

MY_IP_COLOR = 2
O_IP_COLOR = 6
B_IP_COLOR = 12
O_CHANGE_COLOR = 24
CURS_COLOR = 255

KEY_ESC = 27
KEY_ENTER = 10

szMem = 12
szBlock = 64
szReg = 4
ipFov = 8
nSteps = 16
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
    scr.addstr('\tREGS: ')
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
    scr.addstr('IPs=%02x\t' % len([None for ip in ips if ip.owner == plId]))

def run(plId):
    player = players[plId]
    plMem = player.mem
    for ip in (i for i in ips if i.owner == plId):
        try:
            for i in range(nSteps):
                if ip.pos[1]+1 == szBlock:
                    if ip.pos[0]+1 == szMem:
                        raise IpDeadError
                    else:
                        ip.pos = (ip.pos[0]+1, 0)
                else:
                    ip.pos = (ip.pos[0], ip.pos[1]+1)
                runByte(plId, ip)
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
    if byte == 0x10: #MOV REG, IM
        if ip.pos[1]+1 == szBlock:
            if ip.pos[0]+1 == szMem:
                raise IpDeadError
            r = mem[ip.pos[0]+1][0]
            im = mem[ip.pos[0]+1][1]
            mvIpTo = (ip.pos[0]+1, 1)
        elif ip.pos[1]+2 == szBlock:
            if ip.pos[0]+1 == szMem:
                raise IpDeadError
            r = mem[ip.pos[0]][ip.pos[1]+1]
            im = mem[ip.pos[0]+1][0]
            mvIpTo = (ip.pos[0]+1, 0)
        else:
            r = mem[ip.pos[0]][ip.pos[1]+1]
            im = mem[ip.pos[0]][ip.pos[1]+2]
            mvIpTo = (ip.pos[0], ip.pos[1]+2)
        if r+1 >= szReg:
            raise IpDeadError
        regs[r] = im
        ip.pos = mvIpTo
    else:
        pass

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
            else:
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
        pass #TODO
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

