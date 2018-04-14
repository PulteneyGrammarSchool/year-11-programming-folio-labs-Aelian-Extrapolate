import random
import pygame
import math
import time
import socket
import re
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
titfont = pygame.font.SysFont('Comic Sans MS', 40)

s= ''
phase = 0
TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

colours = {"blood3":(0x8e, 0x09, 0x26, 0x50), "white":(0xff, 0xff, 0xff, 0x70), "blood2":(0x51, 0x02, 0x13, 0x50), "blood1":(0x72, 0x09, 0x20, 0x50), "pink":(0xe8, 0x8b, 0xbf),"dsilver":(0x84, 0x7b, 0xaa),"silver":(0xb9, 0xb1, 0xd8, 0x100),"dblue":(0x3a, 0x2b, 0x75),"red":(0xd1, 0x21, 0x3e, 0x70),"dgreen":(0x3d, 0xa0, 0x3d),"black":(0x00, 0x00, 0x00),"purple":(0xb8, 0x37, 0xcc),"green":(0x56, 0xd3, 0x56)}

pygame.init()
size = (600,400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Catch the Face")
surface = pygame.Surface((size), pygame.SRCALPHA, 32)
clock = pygame.time.Clock()
frames = 60
done = False

select = 0
select2 = 0
c_pos2 = [0,0]
c_vel2 = [0.0,0.0]
toggle = False
veins = []
r = 20
f_pos =[size[0]/2,size[1]/2]
scale = 10
g = 0.1
c_pos =[size[0]/2,0]
c_vel=[0.0,0.0]
w = 50
h = 5
dead = False
flip = 0

back = pygame.image.load('background.png').convert()
scream = pygame.mixer.Sound('scream.ogg')
class Blood():
    def __init__(self,pos):
        self.pos = [pos[0], pos[1]]
        self.vel = [random.randint(-15,15),random.randint(-15,15)]
        self.acc = [0.0, 0.0]
        self.rad = random.randint(4,10)
        self.colour = "blood"+str(random.randint(1,3))

    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] -= self.vel[0]*self.acc[0]
        self.vel[1] -= self.vel[1]*self.acc[1]
        self.acc[0] += g
        self.acc[1] += g
        if self.acc[0]>=1:
            self.acc[0]=1
        if self.acc[1]>=1:
            self.acc[1]=1

    def pretty(self, screen):
        #print(self.pos)
        #pygame.draw.ellipse(screen, (0,255,0,10), [self.pos[0]-self.rad,self.pos[1]-self.rad,2*self.rad,2*self.rad], 0)

        pygame.draw.ellipse(screen, colours[self.colour], [self.pos[0]-self.rad,self.pos[1]-self.rad,2*self.rad,2*self.rad], 0)

    def static(self,curr):
        if self.vel[0] == 0.0 and self.vel[1] == 0.0:
            return curr
        return False

def serve():
    global s, phase
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', TCP_PORT))
    s.listen(1)
    s, addr = s.accept()
    phase = 0.2

def client():
    global s, phase
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    phase = 0.3

def rend_fonts(screen, pos, pos2):
    global select, select2
    if phase == 0:
        title = titfont.render("Catch the Face", True, colours['blood3'] )
        title_size = titfont.size("Catch the Face")
        screen.blit(title, [size[0]/2 - title_size[0]/2, size[1]/4 - title_size[1]])

        host_size = myfont.size("Host")
        colour = 'blood3'
        l = size[0]/2 - host_size[0]/2
        r = l + host_size[0]
        t = 4*size[1]/9 - host_size[1]
        b = t + host_size[1]
        if l < pos[0] and pos[0]<r and t < pos[1] and pos[1]< b:
            colour = 'red'
            select = 1
        else:
            select = 0
        host = myfont.render( "Host", True, colours[colour] )
        screen.blit(host, [size[0]/2 - host_size[0]/2, 4*size[1]/9 - host_size[1]])

        conn_size = myfont.size("Connect")
        colour = 'blood3'
        l = size[0]/2 - conn_size[0]/2
        r = l + conn_size[0]
        t = 2*size[1]/3 - conn_size[1]
        b = t + conn_size[1]
        if l < pos[0] and pos[0]<r and t < pos[1] and pos[1]< b:
            colour = 'red'
            select = 2
        elif select != 1:
            select = 0
        conn = myfont.render("Connect", True, colours[colour] )
        screen.blit(conn, [size[0]/2 - conn_size[0]/2, 2*size[1]/3 - host_size[1]])

    elif phase == 0.1:
        title = titfont.render("Connecting...", True, colours['blood3'] )
        title_size = titfont.size("Connecting...")
        screen.blit(title, [size[0]/2 - title_size[0]/2, size[1]/4 - title_size[1]])

    elif phase == 0.2 or phase == 0.3:
        title = titfont.render("Choose Role", True, colours['blood3'] )
        title_size = titfont.size("Choose Role")
        screen.blit(title, [size[0]/2 - title_size[0]/2, size[1]/4 - title_size[1]])

        ghost_size = myfont.size("Ghost")
        colour = 'blood3'
        l = size[0]/2 - ghost_size[0]/2
        r = l + ghost_size[0]
        t = 4*size[1]/9 - ghost_size[1]
        b = t + ghost_size[1]
        if l < pos[0] and pos[0]<r and t < pos[1] and pos[1]< b:
            colour = 'red'
            select2 = 1
        else:
            select2 = 0
        ghost = myfont.render("Ghost", True, colours[colour] )
        screen.blit(ghost, [size[0]/2 - ghost_size[0]/2, 4*size[1]/9 - ghost_size[1]])

        catcher_size = myfont.size("Catcher")
        colour = 'blood3'
        l = size[0]/2 - catcher_size[0]/2
        r = l + catcher_size[0]
        t = 2*size[1]/3 - catcher_size[1]
        b = t + catcher_size[1]
        if l < pos[0] and pos[0]<r and t < pos[1] and pos[1]< b:
            colour = 'red'
            select2 = 2
        elif select2 != 1:
            select2 = 0
        catcher = myfont.render("Catcher", True, colours[colour] )
        screen.blit(catcher, [size[0]/2 - catcher_size[0]/2, 2*size[1]/3 - catcher_size[1]])


def d_face(screen, c, r):
    a = c[0]
    b = c[1]
    pygame.draw.ellipse(screen, colours["white"], [a-r, b-r, 2*r, 2*r], 0)
    pygame.draw.ellipse(screen, colours["dsilver"], [a-r, b-r, 2*r, 2*r], 1)
    if not dead:
        pygame.draw.rect(screen, colours["black"], [a- r/2, b- r/3, r/3, r/4], 0)
        pygame.draw.rect(screen, colours["black"], [a+ r/6, b- r/3, r/3, r/4], 0)
    else:
        pygame.draw.line(screen, colours["black"], [a-r/2,b-r/3], [a-r/6, b-r/12],2)
        pygame.draw.line(screen, colours["black"], [a-r/6,b-r/3], [a-r/2, b-r/12],2)

        pygame.draw.line(screen, colours["black"], [a+r/2,b-r/3], [a+r/6, b-r/12],2)
        pygame.draw.line(screen, colours["black"], [a+r/6,b-r/3], [a+r/2, b-r/12],2)
    pygame.draw.polygon(screen, colours["red"], [[a-3*r/7, b+r/4], [a-r/5, b+3*r/5], [a+r/5, b+3*r/5], [a+3*r/7, b+r/4], [a, b+2*r/5]], 0)

def d_catcher(screen, c):
    x = c[0]
    y = c[1]
    pygame.draw.rect(screen, colours["red"], [x- (w/2), y, w, h], 0)


def draw(screen, pos, pos2):
    global f_pos, r, c_vel , w, toggle, flip
    if phase == 0.0:
        rend_fonts(screen, pos, pos)
    elif phase == 0.1:
        rend_fonts(screen, pos, pos)
        if toggle:
            if select == 1:
                serve()
            else:
                client()
        toggle = True
    elif phase == 0.2:
        rend_fonts(screen, pos , pos2)
    elif phase == 0.3:
        rend_fonts(screen, pos, pos2)
    elif phase >= 1.0:
        screen.blit(back, [0,0])
        d_face(screen, f_pos,r)
        d_catcher(screen, c_pos)
        if not dead:
            if select == 1:
                f_pos[0] += (pos[0]-f_pos[0])/scale
                f_pos[1] += (pos[1]-f_pos[1])/scale

                c_pos[0] += c_vel[0]
                c_pos[1] += c_vel[1]
                c_vel[1] += g

                if c_pos[0]-w/2 < 0 or c_pos[0] +w/2>size[0]:
                    c_pos[0]-= c_vel[0]
                    c_vel[0]*= -1
                    flip = 1
                else:
                    flip = 0
                if c_pos[1] > size[1]-h:
                    c_vel[1] *= -1
                    w += (size[0]-w )/size[0]*10
                    c_vel[1] += g

        else:
            for i in veins:
                i.update()
                i.pretty(screen)



def collide():
    global c_pos, w, h, f_pos, r
    cl = c_pos[0]-w/2
    cr = c_pos[0]+w/2
    ct = c_pos[1]
    cb = c_pos[1]+h
    fl = f_pos[0]-r
    fr = f_pos[0]+r
    ft = f_pos[1]-r
    fb = f_pos[1]+r
    fv = f_pos[0]
    fh = f_pos[1]
    if fl < cr and cl < fr:
        if ft < cb and ct < fb:
            if (cl < fv and fv < cr) or (ct< fh and fh < cb):
                return True
            else:
                for i in [[cl,ct],[cl,cb],[cr,cb],[cr,ct]]:
                    a = max(i[0]-f_pos[0],f_pos[0]-i[0])
                    b = max(i[1]-f_pos[1],f_pos[1]-i[1])
                    if a**2+b**2>r**2:
                        return True
    return False


def keydown(key):
    global c_vel
   #print (c_vel)
    if key[pygame.K_LEFT] or key[pygame.K_a]:
        c_vel[0]-=g

    elif c_vel[0] < 0:
        c_vel[0] +=(0-c_vel[0]) / (scale**2)
    if key[pygame.K_RIGHT] or key[pygame.K_d]:
        c_vel[0]+=g
    elif  c_vel[0] > 0:
        c_vel[0]+=(0-c_vel[0]) / (scale**2)

def keyup(key):
   #print("b")
   pass

def mousedown(curs):
    global select, phase
    if phase == 0:
        if select == 1:
            phase = 0.1
        elif select == 2:
            phase = 0.1
    if phase == 0.2:
        if select2 == 1:
            phase = 1.0
        if select2 == 2:
            phase = 1.1


def bleed():
    global f_pos
    for i in range(random.randint(30,50)):
        veins.append(Blood(f_pos))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #print("lol :P")
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousedown(event)
    if (not dead) and collide():
        print("YOU CAUSE ME ETERNAL AGONY!")
        dead = True
        scream.play()
        bleed()
    if dead:
        curr = True
        for i in veins:
            curr = i.static(curr)
        if curr:
            time.sleep(2.3)
            done = True

    if phase >= 1 and select2 == 2:
        keydown(pygame.key.get_pressed())
    pos = pygame.mouse.get_pos()

    if phase >0.1:
        if select == 1:
            #print(str(f_pos[0])+' '+str(f_pos[1])+' '+str(c_pos[0])+' '+str(c_pos[1])+' '+str(phase)+' '+str(select2)+' '+str(w)+' '+str(flip))
            s.sendall((str(f_pos[0])+' '+str(f_pos[1])+' '+str(c_pos[0])+' '+str(c_pos[1])+' '+str(phase)+' '+str(select2)+' '+str(w)+' '+str(flip)).encode('utf-8'))
            data = s.recv(BUFFER_SIZE).decode('utf-8')
            data1 = re.search(r'(-?[0-9]*\.?[0-9]*) (-?[0-9]*\.?[0-9]*)',data)# ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*)
            if data1 != None:
                if phase >= 1.0:
                    if select2 == 1:
                        c_vel[0] = float(data1.group(1))
                    elif select2 == 2:
                        pos = [float(data1.group(1)),float(data1.group(2))]
                else:
                    pos2 = [int(data1.group(1)),int(data1.group(2))]
            #c_pos2 =[float(data.group(3)),float(data.group(4))]
            #c_vel2 =[float(data.group(5)),float(data.group(6))]
            #print(pos2)
        elif select == 2:
            send = str(pos[0])+' '+str(pos[1])
            data = s.recv(BUFFER_SIZE).decode('utf-8')
            data1 = re.search(r'(-?[0-9]*\.?[0-9]*) (-?[0-9]*\.?[0-9]*) (-?[0-9]*\.?[0-9]*) (-?[0-9]*\.?[0-9]*)e?[+-]?[0-9]* (-?[0-9]*\.?[0-9]*) ([0-2]) ([0-9]*\.?[0-9]*) ([0-1])',data)# ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*) ([0-9]*\.?[0-9]*)
            if data1 != None:
                f_pos = [float(data1.group(1)),float(data1.group(2))]
                c_pos = [float(data1.group(3)),float(data1.group(4))]
                w = float(data1.group(7))
                flip = int(data1.group(8))
                if float(data1.group(5)) >= 1.0:
                    phase = 1.0
                    select2 = 3- int(data1.group(6))
                    if select2 == 2:
                        #print(str(c_vel[0])+' '+str(c_vel[1]))
                        if flip == 1:
                            c_vel[0]*= -1
                        send = str(c_vel[0])+' '+str(c_vel[1])

            s.sendall(send.encode('utf-8'))#+' '+str(c_pos2[0])+' '+str(c_pos2[1])+' '+str(c_vel2[0])+' '+str(c_vel2[1])
    else:
        pos2 = pos

    screen.fill(colours["black"])
    surface.blit(back, [0,0])
    draw(surface,pos, pos2)
    screen.blit(surface, [0,0])
    pygame.display.flip()


    clock.tick(frames)


pygame.quit()
s.close()
