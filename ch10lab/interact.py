import random
import pygame
import math
import time
colours = {"blood3":(0x8e, 0x09, 0x26), "blood2":(0x51, 0x02, 0x13), "blood1":(0x72, 0x09, 0x20), "pink":(0xe8, 0x8b, 0xbf),"dsilver":(0x84, 0x7b, 0xaa),"silver":(0xb9, 0xb1, 0xd8),"dblue":(0x3a, 0x2b, 0x75),"red":(0xd1, 0x21, 0x3e),"dgreen":(0x3d, 0xa0, 0x3d),"black":(0x00, 0x00, 0x00), "white":(0xff,0xff,0xff),"purple":(0xb8, 0x37, 0xcc),"green":(0x56, 0xd3, 0x56)}
veins = []
pygame.init()
size = (600,400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("infini-snakes")
done = False
clock = pygame.time.Clock()
frames = 60
r = 40
f_pos =[size[0]/2,size[1]/2]
scale = 10
g = 0.1
c_pos =[size[0]/2,0]
c_vel=[0.0,0.0]
w = 50
h = 5
dead = False

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
        pygame.draw.ellipse(screen, colours[self.colour], [self.pos[0]-self.rad,self.pos[1]-self.rad,2*self.rad,2*self.rad], 0)

    def static(self,curr):
        if self.vel[0] == 0.0 and self.vel[1] == 0.0:
            return curr
        return False

def d_face(c, r):
    a = c[0]
    b = c[1]
    pygame.draw.ellipse(screen, colours["white"], [a-r, b-r, 2*r, 2*r], 0)
    pygame.draw.ellipse(screen, colours["dsilver"], [a-r, b-r, 2*r, 2*r], 1)
    if not dead:
        pygame.draw.rect(screen, colours["black"], [a- r/2, b- r/3, r/3, r/4], 0)
        pygame.draw.rect(screen, colours["black"], [a+ r/6, b- r/3, r/3, r/4], 0)
    else:
        pygame.draw.line(screen, colours["black"], [a-r/2,b-r/3], [a-r/6, b-r/12],5)
        pygame.draw.line(screen, colours["black"], [a-r/6,b-r/3], [a-r/2, b-r/12],5)

        pygame.draw.line(screen, colours["black"], [a+r/2,b-r/3], [a+r/6, b-r/12],5)
        pygame.draw.line(screen, colours["black"], [a+r/6,b-r/3], [a+r/2, b-r/12],5)
    pygame.draw.polygon(screen, colours["red"], [[a-3*r/7, b+r/4], [a-r/5, b+3*r/5], [a+r/5, b+3*r/5], [a+3*r/7, b+r/4], [a, b+2*r/5]], 0)

def d_catcher(c):
    x = c[0]
    y = c[1]
    pygame.draw.rect(screen, colours["red"], [x- (w/2), y, w, h], 0)


def draw(pos):
    global f_pos, r, c_vel , w
    d_face(f_pos,r)
    d_catcher(c_pos)
    if not dead:
        f_pos[0] += (pos[0]-f_pos[0])/scale
        f_pos[1] += (pos[1]-f_pos[1])/scale

        c_pos[0] += c_vel[0]
        c_pos[1] += c_vel[1]
        c_vel[1] += g

        if c_pos[0]-w/2 < 0 or c_pos[0] +w/2>size[0]:
            c_pos[0]-= c_vel[0]
            c_vel[0]*= -1
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
    if key[pygame.K_LEFT] or key[pygame.K_a]:
        c_vel[0]-=g

    elif c_vel[0] < 0:
        c_vel[0] +=(0-c_vel[0]) / (scale**2)
    if key[pygame.K_RIGHT] or key[pygame.K_d]:
        c_vel[0]+=g
    elif  c_vel[0] > 0:
        c_vel[0]+=(0-c_vel[0]) / (scale**2)

def keyup(key):
    print("b")

def mousedown(curs):
    pass

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
        bleed()
    if dead:
        curr = True
        for i in veins:
            curr = i.static(curr)
        if curr:
            time.sleep(1)
            done = True
    keydown(pygame.key.get_pressed())
    pos = pygame.mouse.get_pos()
    screen.fill(colours["dblue"])
    draw(pos)
    pygame.display.flip()
    clock.tick(frames)


pygame.quit()
