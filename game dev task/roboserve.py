import random
import pygame
import math
import time
import socket
import re
import queue
pygame.font.init()
myfont = pygame.font.SysFont('Times New Roman', 25)
titfont = pygame.font.SysFont('Comic Sans MS', 40)

s= ''
phase = 0
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 2048
colours = {"blood3":(0x8e, 0x09, 0x26, 0x50), "white":(0xff, 0xff, 0xff, 0x70), "blood2":(0x51, 0x02, 0x13, 0x50), "blood1":(0x72, 0x09, 0x20, 0x50), "pink":(0xe8, 0x8b, 0xbf),"dsilver":(0x84, 0x7b, 0xaa),"silver":(0xb9, 0xb1, 0xd8, 0x100),"dblue":(0x3a, 0x2b, 0x75),"red":(0xd1, 0x21, 0x3e, 0x70),"dgreen":(0x3d, 0xa0, 0x3d),"black":(0x00, 0x00, 0x00),"purple":(0xb8, 0x37, 0xcc),"green":(0x56, 0xd3, 0x56)}

#pygame.init()
size = (900,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Robo-Pigs")
surface = pygame.Surface((size), pygame.SRCALPHA, 32)
clock = pygame.time.Clock()
frames = 60
done = False
clients =[]
robots = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', TCP_PORT))


class Robot():
    def __init__(self, name, health, coords, facing, actions):
        self.name = name
        self.health = health
        self.coords = [coords[0],coords[1]]
        self.facing = facing
        self.actions = actions
        self.is_drawn = True
        self.is_airborn = False
        self.is_alive = True

    def act(self, key, *args):
        org = self.actions[key].do()[:]
        temp = [org[0][:],org[1][:], org[2]]
        if len(args) > 0:
            facing = args[0]
            coords= args[1]
        else:
            facing = self.facing
            coords = self.coords
        #print(key)
        #print(temp)
        #print()
        x = 0
        y = 1
        x_sign = 1
        y_sign = 1
        if facing == 1:
            x = 1
            y = 0
            x_sign = -1
        elif facing == 2:
            x_sign = -1
            y_sign = -1
        elif facing == 3:
            x = 1
            y = 0
            y_sign = -1

        for i in range(len(temp[0])):
            copy = temp[0][i][y]
            temp[0][i][0] = x_sign*temp[0][i][x] + coords[0]
            temp[0][i][1] = y_sign*copy + coords[1]

        ##print("flag1",x_sign, temp[1][x], y_sign, temp[1][y], x, y, self.coords)
        copy = temp[1][y]
        temp[1][0] = (x_sign*temp[1][x]) + coords[0]
        temp[1][1] = (y_sign*copy) + coords[1]


        temp[2] += facing
        temp[2] = temp[2]%4

        return temp #[shape, pos, facing]
        #shape  = [[x,y,effect]]

    def move(self, pos, rotat):
        self.coords = pos
        self.facing = rotat

    def dmg(self, amount):
        self.health -= amount
        self.is_alive = (self.health > 0)

    def draw(self, screen, board, plan):
        if plan == 'not a key':
            self.image.move(board.where(self.coords))
            self.image.draw(screen, self.facing)
        else:
            coords = self.coords
            facing = self.facing
            temp = ['',coords,facing]
            for i in plan.split(' '):
                if (i in self.actions):

                    temp = self.act(i, facing, coords)
                    for i in temp[0]:
                        place = board.where(i[0:2])
                        image = board.effects[temp[2]]
                        screen.blit(image.img, image.add(place))
                    coords = temp[1]
                    facing = temp[2]
                    #print(temp[1])
            place = board.where(temp[1])
            image = self.image
            screen.blit(image.img[temp[2]], image.add(place))
            #image = board.effects['f'+str(temp[2])]
            #screen.blit(image.img, image.add(place))
        #work on drawing actions

class Action():
    def __init__(self, name, shape, move, rotat):
        self.name = name
        self.shape = shape
        self.move = move
        self.turn = rotat

    def do(self):
        return [self.shape, self.move, self.turn]


class Board():
    def __init__(self, size, xy, width, height, tiles, effects):
        #tiles is a list of [Picture,effect,no_tiles of this type]
        #effects is a dict of pictures
        off = [width/2, height/2]
        temp_board = []
        temp_tiles = []
        left = size[0]/2 - (xy / 2.0)*width
        top = size[1]/2 - (xy / 2.0)*height
        totes= 0
        for i in tiles:
            totes += i[2]

        for i in range(xy):
            temp_board.append([])
            temp_tiles.append([])

            for j in range(xy):
                temp_board[i].append([left+(xy-j+i)/2.0*width, top+(1+i+j)/2.0*height])

                rando = random.randint(1,totes)
                for k in range(len(tiles)):
                    if tiles[k][2] < rando:
                        rando -= tiles[k][2]
                    else:
                        rando = tiles[k]
                        tiles[k][2] -= 1
                        totes -= 1
                #print(rando)
                temp_tiles[i].append(rando[0:2])
                #print (temp_tiles[i][j])
                temp_tiles[i][j][0] = Picture(temp_tiles[i][j][0][0],temp_tiles[i][j][0][1])
                temp_tiles[i][j][0].move(temp_board[i][j])
        self.coords = temp_board
        self.tiles = temp_tiles
        self.effects = effects

    def where(self, pos):
        x = pos[0]
        y = pos[1]
        return self.coords[x][y]

    def what(self, pos):
        x = pos[0]
        y = pos[1]
        return self.tiles[x][y][1]

    def draw(self, screen):
        drawing = queue.Queue(16)
        drawing.put([0,0])
        while True:
            p = drawing.get()
            #print (p[0],p[1])
            self.tiles[p[0]][p[1]][0].draw(screen)
            if p[0] == 0 and p[1]!= len(self.coords)-1:
                drawing.put([p[0],p[1]+1])
            if p[0] != len(self.coords)-1:
                drawing.put([p[0]+1,p[1]])
            if p == [len(self.coords)-1,len(self.coords)-1]:
                break

def reset():
    global clients, robots
    clients =[]
    robots = []
string = r'\'[A-Za-z ]*\''
integer = r'-?[0-9]*'
decimal = r'-?[0-9]*'
coord = r'\[('+decimal+r'), ('+decimal+r')\]'
shape = r'\[('+integer+r'), ('+integer+r'), ('+integer+r')\]'
action = r'\[('+string+r'), (\[(?!'+shape+r')(?:, ('+shape+r'))*\]), ('+coord+r'), ([0-9])\]'


no_players = 1

while len(clients) < no_players:
    s.listen(1)
    conn, addr = s.accept()
    clients.append([conn])
    print ('connected')
    clients[len(clients)-1][0].sendall(str(len(clients)-1).encode('utf-8'))

    data = clients[len(clients)-1][0].recv(BUFFER_SIZE)
    if len(clients) == 1:
        no_players = int(data.decode('utf-8'))

while True:
    print('Choose robots!')
    temp = []
    for i, client in enumerate(clients):
        data = ''
        while data == '':
            data = client[0].recv(BUFFER_SIZE)
            data = data.decode('utf-8')

        #name, shape, move, rotat
        print (data)
        data = eval(data)#re.search(r'\[('+string+r'), ('+integer+r'), ('+coord+r'), ('+integer+r'), (\[('+action+r')(?:, ('+action+r'))*\])\]', data)
        print (data)
        actions = data[5].copy()
        for i in actions:
            actions[i] = Action(actions[i][0], actions[i][1], actions[i][2], actions[i][3])
        temp.append([data[0], data[1], data[2], data[3], data[4], data[5]])
        robots.append(Robot(data[0], data[1], data[2], data[3], actions))


    for i, client in enumerate(clients):
        client[0].sendall(str(temp).encode('utf-8'))

    while True:
        dead= [-1,-1,-1,-1]
        turns = []
        for i, client in enumerate(clients):
            data = ''
            while data == '':
                data = client[0].recv(BUFFER_SIZE)
                data = data.decode('utf-8')
            data = eval(data)
            print (data)
            if data == []:
                data = ['x','x','x','x','x']
            elif data[0] == 'dead':
                robots[i].is_alive = False
                dead[i] = data[1]
                data = ['x','x','x','x','x']
            turns.append(data)
        for act in range(5):
            posits = []
            permiss = []
            for bot in range(len(clients)):
                #print (act, bot, turns)
                if turns[bot][act] in robots[bot].actions:
                    end = robots[bot].act(turns[bot][act])
                    permiss.append(True)
                    for i, place in enumerate(posits):
                        #print(place[1], end[1])
                        if place[1] == end[1]:
                            #print('ahah!')
                            turns[i][act]   = 'x'
                            turns[bot][act] = 'x'
                            permiss[i] = False
                            permiss[-1] = False
                            break
                else:
                    turns[bot][act] = 'x'


                posits.append(end)
            for i, yes in enumerate(permiss):
                if yes:
                    robots[i].move(posits[i][1], posits[i][2])

        no_alive = 0
        alive = []
        for i, bot in enumerate(robots):
            if bot.is_alive:
                no_alive+=1
                alive.append(i)
        if no_alive == 1:
            turns = 'end('+str(alive[0])+')'

        if no_alive == 0:
            winning = 0
            last = -1
            for i, when in enumerate(dead):
                if when > last:
                    last = when
                    winning = i
            turns = 'end('+str(winning)+')'
        for i, client in enumerate(clients):
            client[0].sendall(str(turns).encode('utf-8'))
        if no_alive <= 1:
            break
    print('a')
    data = ''
    while data == '':
        data = clients[0][0].recv(BUFFER_SIZE)

        data = data.decode('utf-8')
        print(data)

    print('test', data)
    for i, client in enumerate(clients):
        client[0].sendall(data.encode('utf-8'))
    if eval(data) == 1:
        reset()
        break

    else:
        robots = []
s.close()
