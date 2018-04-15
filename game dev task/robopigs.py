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
phase = 0.0
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 2048
colours = {"blood3":(0x8e, 0x09, 0x26, 0x50), "white":(0xff, 0xff, 0xff, 0x70), "blood2":(0x51, 0x02, 0x13, 0x50), "blood1":(0x72, 0x09, 0x20, 0x50), "pink":(0xe8, 0x8b, 0xbf),"dsilver":(0x84, 0x7b, 0xaa),"silver":(0xb9, 0xb1, 0xd8, 0x100),"dblue":(0x3a, 0x2b, 0x75),"red":(0xd1, 0x21, 0x3e, 0x70),"dgreen":(0x3d, 0xa0, 0x3d),"black":(0x00, 0x00, 0x00),"purple":(0xb8, 0x37, 0xcc),"green":(0x56, 0xd3, 0x56)}

pygame.init()
size = (900,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Robo-Pigs")
surface = pygame.Surface((size), pygame.SRCALPHA, 32)
clock = pygame.time.Clock()
frames = 60
done = False
no_people = 2

class Picture(pygame.sprite.Sprite):
    def __init__(self, img, pos):
        super().__init__()
        ##print('flag1',img)
        if type(img) != list:
            self.img = pygame.image.load(img).convert()
            self.img.set_colorkey(colours["white"][0:3])
            self.rect = self.img.get_rect()
        else:
            self.img = []
            for i in img:
                i = pygame.image.load(i).convert()
                i.set_colorkey(colours["white"][0:3])
                self.img.append(i)
            self.rect =self.img[0].get_rect()

        self.offset = pos

    def move(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def add(self, pos):
        return [pos[0]+self.offset[0], pos[1]+self.offset[1]]

    def draw(self, screen, *args):
        if type(self.img) == list:
            screen.blit(self.img[args[0]], self.add(self.rect.topleft))
        else:
            screen.blit(self.img, self.add(self.rect.topleft))

class Robot():
    def __init__(self, name, health, coords, facing, img, actions):
        self.name = name
        self.health = health
        self.coords = [coords[0],coords[1]]
        self.facing = facing
        self.image = Picture(img[0],img[1])
        self.actions = actions
        self.is_drawn = True
        self.is_airborn = False
        self.is_alive = True

    def act(self, key, *args):
        org = self.actions[key].do()
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

    def is_valid(self, turn):
        no_x = 0
        validity = True
        for i in turn:
            if i == 'x':
                no_x+=1
        if x != 5-health:
            validity = False
        return validity



    def move(self, pos, rotat):
        self.coords = pos
        self.facing = rotat

    def dmg(self, amount, step):
        self.health -= amount
        self.is_alive = (self.health > 0)
        if not self.is_alive:
            self.when = step


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
                    print(temp[0])
                    for j in temp[0]:
                        print(j[:2])
                        place = board.where(j[:2])
                        image = board.effects['A'+str(j[2][0])]
                        screen.blit(image.img, image.add(place))
                    coords = temp[1]
                    print(coords)
                    facing = temp[2]
                    #print(temp[1])
            place = board.where(temp[1])
            image = self.image
            screen.blit(image.img[temp[2]], image.add(place))
            #image = board.effects['f'+str(temp[2])]
            #screen.blit(image.img, image.add(place))
        #work on drawing actions

class Action():
    def __init__(self,name, shape, move, rotat, icon):
        self.name = name
        self.shape = shape
        self.move = move
        self.turn = rotat
        self.icon = Picture(icon[0], icon[1])

    def do(self):
        return eval(str([self.shape, self.move, self.turn]))

    def draw(self, screen):
        self.icon.draw(screen)

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
                ##print(rando)
                temp_tiles[i].append(rando[0:2])
                ##print (temp_tiles[i][j])
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
            ##print (p[0],p[1])
            self.tiles[p[0]][p[1]][0].draw(screen)
            if p[0] == 0 and p[1]!= len(self.coords)-1:
                drawing.put([p[0],p[1]+1])
            if p[0] != len(self.coords)-1:
                drawing.put([p[0]+1,p[1]])
            if p == [len(self.coords)-1,len(self.coords)-1]:
                break

class Animation():
    def __init__(self, coords, imgs, board):
        self.img = Picture(imgs[0], imgs[1])
        self.curr = 0
        self.img.move(self.img.add(board.where(coords)))

    def update(self, phase):
        self.img.move(self.img.add(board.where(coords)))
        self.curr += 1
        if self.curr >= len(self.img.img):
            return True
        return False

    def draw(self, screen, board):
        self.img.draw(screen, self.curr)

    def add(self, pos):
        return self.img.add(pos)

    def move(self, pos):
        self.img.move(pos)

effects = {'f0':Picture("facing0.png",[-45,-25]), 'f1':Picture("facing1.png",[-45,-25]), 'f2':Picture("facing2.png",[-45,-25]), 'f3':Picture("facing3.png",[-45,-25]), 0:Picture("grey.png",[-45,-25]), 'A0':Picture("dmg.png", [-45, -25])}
affects = ['live[k].dmg(1, step)', 'live[k].move({0:[0,-1], 1:[1,0], 2:[0,1], 3:[-1,0]}[results[1][j][1]], live[k]F.facing)']

board = Board(size, 8, 90, 50, [[["grey.png",[-45,-25]],0,64]], effects)

actions = {"x":["Damaged", [], [0,0], 0, ["robo-pig.png",[-25,-20]]], 'H':['Hit', [[-1, -1, [0]], [0, -1, [0]], [1, -1, [0]]], [0, 0], 0, ["robo-pig.png", [-25, -20]]], "^":["Move Forward",[], [0,-1], 0, ["robo-pig.png",[-25,-20]]], "/":["Move Forward Right",[], [1,-1], 0, ["robo-pig.png",[-25,-20]]], "\\":["Move Forward Left",[], [-1,-1], 0, ["robo-pig.png",[-25,-20]]], "L":["Turn Left",[], [0,0], -1, ["robo-pig.png",[-25,-20]]], "R":["Turn Right",[], [0,0], 1, ["robo-pig.png",[-25,-20]]]}

bots = [["PigBot", 5, [5,3], 0, [["robopig0.png", "robopig1.png", "robopig2.png", "robopig3.png"],[-25,-35]], actions ],['TestBot'], ['BooBot']]
live = []#[Robot(bots[0][0],bots[0][1], bots[0][2], bots[0][3], bots[0][4], bots[0][5])]
plan = ''
player_no = 0

def client(address):
    global s
    address = address.split(':')
    if len(address)==2 and address[1] != '':
        ip, port = address
        port= int(port)
    else:
        ip = address[0]
        port = TCP_PORT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    s.sendall(str(no_people).encode('utf-8'))
    time.sleep(0.1)
    data = int(s.recv(BUFFER_SIZE).decode('utf-8'))
    return data
    '''for i in range(no_people-1):
        s.sendall('n'.encode('utf-8'))
    s.sendall('y'.encode('utf-8'))'''

def s_chosen(s, choice):
    s.sendall(str([bots[choice][0], bots[choice][1], bots[choice][2], bots[choice][3], bots[choice][4], bots[choice][5]]).encode('utf-8'))
    data = ''
    while data == '':
        data = s.recv(BUFFER_SIZE)
        data = data.decode('utf-8')
    data = eval(data)
    for bot in data:
        actions = bot[5]
        for i in actions:
            actions[i] = Action(actions[i][0], actions[i][1], actions[i][2], actions[i][3], actions[i][4])
        live.append(Robot(bot[0], bot[1], bot[2], bot[3], bot[4], actions))

def s_turn(s, plan):
    s.sendall(str(plan.split(' ')[:-1]).encode('utf-8'))
    data = ''
    while data == '':
        data = s.recv(BUFFER_SIZE)
        data = data.decode('utf-8')
    data = eval(data)
    return data

def s_dead(s, when):
    s.sendall(str(['dead', when]).encode('utf-8'))
    data = ''
    while data == '':
        data = s.recv(BUFFER_SIZE)
        data = data.decode('utf-8')
    data = eval(data)
    return data

def end(who):
    global phase
    phase = 3.0
    return [who, 0]

def s_again(s, plan):
    print (player_no, plan)
    global done
    if player_no == 0:
        s.sendall(str(plan[1]).encode('utf-8'))
    data = ''
    while data == '':
        data = s.recv(BUFFER_SIZE)
        data = data.decode('utf-8')
    if eval(data) == 0:
        plan = reset()
    else:
        done = True
    return plan

def reset():
    global live, plan, phase
    phase = 0.1
    plan = 0
    live = []
    return plan

def keydown(key, plan, s):
    global phase, player_no
    if phase == 0.0:
        if key.key == 8:#backspace
            plan = plan[:-1]
        elif key.key == 13:#enter
            phase = 0.1
            player_no = client(plan)
            plan = 0
        elif key.unicode != '':
            #print(key.key)
            plan+=key.unicode

    elif phase == 0.1:
        #if key.key == 8:#backspace
        #    plan = plan[:-1]
        if key.key == 13:#enter
            phase = 1.0
            s_chosen(s, plan)
            plan = ''
            #plan = client(s, plan)
        elif key.key == 273:#^
            plan-=1
        elif key.key == 274:#v
            plan+=1
    elif phase == 1.0:
        if key.key == 8:#backspace
            plan = plan[:-2]
        elif key.key == 13:#enter
            phase = 1.1
            if not live[player_no].is_alive:
                phase = 2.0
                plan = s_dead(s, live[player_no].when)
            else:
                plan = s_turn(s, plan)
            print (plan)
        elif key.unicode != '' and len(plan) <10 :
            #print(key.key)
            plan+=key.unicode+' '

    elif phase == 2.0:
        plan = s_turn(s, 'x x x x x ')

    elif phase == 3.0:
        #if key.key == 8:#backspace
        #    plan = plan[:-1]
        if key.key == 13:#enter
            plan = s_again(s, plan)
            #plan = client(s, plan)
        elif key.key == 275 or key.key == 276:#^
            print(plan)
            plan[1]=(plan[1]+1)%2

    return plan


def connection(screen, plan):
    title = titfont.render("Robo-Battle-Pigs", True, colours['white'])
    tit_size = titfont.size("Robo-Battle-Pigs")
    prompt = myfont.render("Enter IP Address!", True, colours['white'])
    prompt_size = myfont.size("Enter IP Address!")
    plan_text = myfont.render(plan, True, colours['white'])
    plan_size = myfont.size(plan)

    screen.blit(title, [size[0]/2 - tit_size[0]/2, size[1]/4 - tit_size[1] ])
    screen.blit(prompt, [size[0]/2 - prompt_size[0]/2,3*size[1]/8 - prompt_size[1]/2])
    screen.blit(plan_text, [size[0]/2- plan_size[0]/2,4*size[1]/8])

def choose(screen, plan):
    title = titfont.render("Robo-Battle-Pigs", True, colours['white'])
    tit_size = titfont.size("Robo-Battle-Pigs")
    screen.blit(title, [size[0]/2 - tit_size[0]/2, size[1]/4 - tit_size[1] ])
    print('yo')
    for i, bot in enumerate(bots):
        if i == 0:
            colour = 'red'
        else:
            colour = 'white'
        print('emph', i, plan)
        j = (i+plan)%len(bots)
        txt = myfont.render(bots[j][0], True, colours[colour])
        txt_size = myfont.size(bots[j][0])
        screen.blit(txt, [size[0]/2 - txt_size[0]/2,(3+i)*size[1]/8 - txt_size[1]])

def planning(screen, plan, board):
    board.draw(screen)
    for i, bot in enumerate(live):
        if i != player_no:
            bot.draw(screen, board, 'not a key')
    if plan == '':
        key = 'not a key'
        live[player_no].draw(screen, board, key)
    else:
        live[player_no].draw(screen, board, plan)

    prompt = myfont.render("Program Your Robot!", True, colours['white'])
    prompt_size = myfont.size("Program Your Robot!")
    plan_text = myfont.render(plan, True, colours['black'])
    plan_size = myfont.size(plan)
    plate_size = myfont.size('M M M M M ')
    if phase != 2.0:
        screen.blit(prompt, [size[0]/16,16*size[1]/20 - prompt_size[1]/2])
        pygame.draw.rect(screen, colours['white'], [ size[0]/16 ,17*size[1]/20 - plan_size[1]/2, plate_size[0], plate_size[1]], 0)
        screen.blit(plan_text, [size[0]/16,17*size[1]/20 - plan_size[1]/2])

def display(screen, plan, board, step, tick):
    board.draw(screen)
    if tick == 0:
        results = [[],[]]
        for i, bot in enumerate(live):
            #print(i, step)
            result= bot.act(plan[i][step])

            bot.move(result[1], result[2])

            results[0].append(result[0])
            results[1].append(result[1:])

        for j, effect in enumerate(results[0]):
            for affect in effect:
                for k, bot in enumerate(results[1]):
                    if bot[0] == affect[:-1]:
                        for i in affect[-1]:
                            eval(affects[i])
    for i, bot in enumerate(live):
        bot.draw(screen, board, 'not a key')

def finale(screen, plan):
    title = titfont.render("Robo-Battle-Pigs", True, colours['white'])
    tit_size = titfont.size("Robo-Battle-Pigs")
    prompt = myfont.render("Play Again?", True, colours['white'])
    prompt_size = myfont.size("Play Again")
    plan_text = titfont.render('Player '+str(plan[0]+1)+' Wins!', True, colours['white'])
    plan_size = titfont.size('Player '+str(plan[0]+1)+' Wins!')
    if plan[1] == 0:
        colour = ['red', 'white']
    else:
        colour = ['white', 'red']
    y = myfont.render("Y", True, colours[colour[0]])
    y_size = myfont.size("Y")
    n = myfont.render("N", True, colours[colour[1]])
    n_size = myfont.size("N")

    screen.blit(title, [size[0]/2 - tit_size[0]/2, size[1]/4 - tit_size[1] ])
    screen.blit(plan_text, [size[0]/2 - plan_size[0]/2,3*size[1]/8 - plan_size[1]/2])
    if player_no == 0:
        screen.blit(prompt, [size[0]/2- prompt_size[0]/2,4*size[1]/8])
        screen.blit(y, [3*size[0]/7- y_size[0]/2,5*size[1]/8])
        screen.blit(n, [4*size[0]/7- n_size[0]/2,5*size[1]/8])

def hud(screen, live, me):
    for i, bot in enumerate(live):
        if i == me:
            colour = 'red'
        else:
            colour = 'white'
        txt = myfont.render(bot.name, True, colours[colour])
        txt_size = myfont.size(bot.name+'  ')
        screen.blit(txt, [size[0]/16 ,(i+1)*size[1]/16 ])
        txt = myfont.render(str(bot.health), True, colours[colour])
        screen.blit(txt, [size[0]/16 +txt_size[0],(i+1)*size[1]/16 ])

tick = 0
step = 0
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            plan = keydown(event, plan, s)


    screen.fill(colours["black"])

    if phase == 0.0:
        connection(screen, plan)
    elif phase == 0.1:
        choose(screen, plan)
    elif phase == 1.0 or phase == 2.0:
        planning(screen, plan, board)
        hud(screen, live, player_no)
        tick = 0
        step = 0
    elif phase == 1.1 or phase == 2.1:
        display(screen, plan, board, step, tick)
        hud(screen, live, player_no)
        tick += 1
        #print(tick)
        if (tick+2) % (2*frames) == 0:
            #print('step', step, phase)
            tick = 0
            step += 1
    elif phase == 3.0:
        finale(screen, plan)

    if step == 4 and (tick+2)%(2*frames)> frames:
        if phase == 1.1:
            phase = 1.0
            plan = ''
        if phase == 2.1:
            phase = 2.0
            plan = ''


    pygame.display.flip()
    if phase == 3.0 and player_no != 0:
        s_again(s, plan)

    clock.tick(frames)


pygame.quit()
s.close()
