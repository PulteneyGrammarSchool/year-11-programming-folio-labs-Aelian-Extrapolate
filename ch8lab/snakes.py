import pygame
import math
import random
colours = {"pink":(0xe8, 0x8b, 0xbf),"dsilver":(0x84, 0x7b, 0xaa),"silver":(0xb9, 0xb1, 0xd8),"dblue":(0x3a, 0x2b, 0x75),"red":(0xd1, 0x21, 0x3e),"dgreen":(0x3d, 0xa0, 0x3d),"black":(0x00, 0x00, 0x00), "white":(0xff,0xff,0xff),"purple":(0xb8, 0x37, 0xcc),"green":(0x56, 0xd3, 0x56)}
pygame.init()
size = (600,400)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("infini-snakes")
done = False
clock = pygame.time.Clock()
click_time = 0
frames = 60
s = random.choice([1,5,7])
ls = {1:90, 3:30, 5:15, 7:7}
t = 0.0
l = ls[s]
d = 6
r = 20
shape = ["sin", 1, "sin", 2]

def keydown(key):
    print("a")

def keyup(key):
    print("b")

def mousedown(curs):
    global click_time
    click_time = pygame.time.get_ticks()

def mouseup(curs):
    global click_time
    if pygame.time.get_ticks()-click_time <= 300:
        print ("gah")

def d_face(a, b):
    global r
    pygame.draw.ellipse(screen, colours["white"], [a-r, b-r, 2*r, 2*r], 0)
    pygame.draw.ellipse(screen, colours["dsilver"], [a-r, b-r, 2*r, 2*r], 1)
    pygame.draw.rect(screen, colours["black"], [a- r/2, b- r/3, r/3, r/4], 0)
    pygame.draw.rect(screen, colours["black"], [a+ r/4, b- r/3, r/3, r/4], 0)
    pygame.draw.polygon(screen, colours["red"], [[a-3*r/7, b+r/4], [a-r/5, b+3*r/5], [a+r/5, b+3*r/5], [a+3*r/7, b+r/4], [a, b+2*r/5]], 0)

def get_pos(off, i):
    aa = off[0]*math.pi/off[1]+t+2*math.pi/((frames/2+5)*d)*i
    ab =off[0]*math.pi/off[1]+t+2*math.pi/((frames/2+5)*d)*i
    if off[2] == "sin":
        aa = math.sin(off[3]*aa)
    else:
        aa = math.cos(off[3]*aa)

    if off[4] == "sin":
        ab = math.sin(off[5]*ab)
    else:
        ab = math.cos(off[5]*ab)

    a = size[0]/2 + size[0]/3 * aa
    b = size[1]/2 +  size[1]/3 * ab
    return a, b

def draw():
    global t, l, d, r, s
    #pygame.draw.rect(screen, colours["green"], [0, 0, size[0], size[1]/20], 0)
    for i in range(l):
        for j in range(s):
            a, b = get_pos([j*2, s]+shape, i)
            pygame.draw.ellipse(screen, colours["silver"], [a-r, b-r, 2*r, 2*r], 0)
            if i == l-1:
                d_face(a,b)

    t += 2*math.pi/(frames*d)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #print("lol :P")
            done = True
        elif event.type == pygame.KEYDOWN:
            keydown(event)
        elif event.type == pygame.KEYUP:
            keyup(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousedown(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            mouseup(event)
    screen.fill(colours["dblue"])
    draw()
    pygame.display.flip()
    clock.tick(frames)


pygame.quit()
