import pygame
import math
import random

def min3(a,b,c):
    return min(a,b,c)

def box(y,x):
    for i in range(y):
        print("*"*x)

def find(l, q):
    for i in range(len(l)):
        if l[i] == q:
            print("Found "+str(q)+" at position "+str(i))

def create_list(l):
    a = []
    for i in range(l):
        a.append(random.randint(1,6))
    return a

def count_list(l, q):
    c = 0
    for i in l:
        if q == i:
            c+=1
    return c

def average_list(l):
    s = 0.0
    for i in l:
        s += i
    return s/len(l)

def test():
    print(min3(4, 7, 5))
    print(min3(4, 5, 5))
    print(min3(4, 4, 4))
    print(min3(-2, -6, -100))
    print(min3("Z", "B", "A"))
    print("\n")
    box(7,5)  # Print a box 7 high, 5 across
    print()   # Blank line
    box(3,2)  # Print a box 3 high, 2 across
    print()   # Blank line
    box(3,10) # Print a box 3 high, 10 across
    print("\n")
    my_list = [36, 31, 79, 96, 36, 91, 77, 33, 19, 3, 34, 12, 70, 12, 54, 98, 86, 11, 17, 17]
    find(my_list, 12)
    find(my_list, 91)
    find(my_list, 80)
    print("\n")
    my_list = create_list(5)
    print(my_list)
    print()
    count = count_list([1,2,3,3,3,4,2,1],3)
    print(count)
    print()
    avg = average_list([1,2,3])
    print(avg)
    print("\n")

test()
big = create_list(10000)
small = []
for i in range(6):
    small.append(count_list(big,i+1))
    print(small[i])
print(average_list(big))
