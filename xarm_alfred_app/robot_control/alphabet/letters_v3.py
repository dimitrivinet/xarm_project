#!/usr/bin/env python3

import queue
import time

from numpy import add
from copy import deepcopy

is_down = True

command_queue = queue.Queue()

R_THRESH = -439.877
L_THRESH = -611.823


SPEED = 15 # min: 1 max: 20 default: 5


def start(arm):
    arm.set_tool_position(z=-5, wait=True, speed=10, mvacc=100)

def Invalid(arm):
    print("invalid")


def space(arm):
    return [[0, 6, 0, 0, 0, 0, 0, True]]


def move(arm):
    # start(arm)
    last_pos = deepcopy(arm.position) + [0, 0]
    # last_pos[2] 
    while True:
        time.sleep(0.05)
        if not command_queue.empty():
            path = command_queue.get(block = False)
            # print(f'Working on {path}')

            if len(path) == 8:               

                # if last_pos[0] + 10 > R_THRESH and abs(path[2]) != 5 :
                #     last_pos[1] = L_THRESH
                #     last_pos[0] -= 15

                last_pos = list(add(last_pos[:6], path[:6])) + [0, 0]
                last_pos[6] = path[6]
                last_pos[7] = path[7]

                # print(last_pos)

                # ret = arm.set_position(*last_pos[:6], radius=last_pos[6], is_radian=False, wait=last_pos[7], speed=speed, mvacc=10*speed, relative=False)
                ret = arm.set_position(*last_pos[:6], radius=last_pos[6], is_radian=False, wait=False, speed=SPEED, mvacc=10*SPEED, relative=False)
                if ret < 0:
                    print('set_position, ret={}'.format(ret))
                    return -1

            else:
                pass

            # print(f'Finished {path}')
            command_queue.task_done()
        else:
            pass


def A(arm):

    paths = [
        [10, 5, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, -5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 5, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [5, -7.5, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [-5, 5.5, 0, 0, 0, 0, 0, False],
    ]

    return paths


def B(arm):

    paths = [  # [x, y, z, roll, pitch, yaw,radius, is_rad, wait]
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 5, 0, 0, 0, 0, 5, False],
        [-5, 0, 0, 0, 0, 0, 5, False],
        [0, -6, 0, 0, 0, 0, 5, False],
        [0, 6, 0, 0, 0, 0, 5, False],
        [-5, 0, 0, 0, 0, 0, 5, False],
        [0, -6, 0, 0, 0, 0, 5, False],
        [0, 9, -5, 0, 0, 0, 0, False],
    ]

    return paths

def C(arm):

    paths = [
        [7, 8, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [3, 0, 0, 0, 0, 0, 10, False],
        [0, -8, 0, 0, 0, 0, 10, False],
        [-10, 0, 0, 0, 0, 0, 10, False],
        [0, 8, 0, 0, 0, 0, 10, False],
        [3, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [-3, 0, 0, 0, 0, 0, 0, False],
        [0, 3, 0, 0, 0, 0, 0, False],
    ]

    return paths


def D(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 7, 0, 0, 0, 0, 7, False],
        [-10, 0, 0, 0, 0, 0, 7, False],
        [0, -7, 0, 0, 0, 0, 0, False],
        [0, 10, -5, 0, 0, 0, 0, False],
    ]
    
    return paths



def E(arm):
    paths = [
        [10, 7, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, -7, 0, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 7, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [5, -7, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [-5, 5, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def F(arm):
    paths = [
        [10, 7, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, -7, 0, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [5, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [-5, 5, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def G(arm):
    
    paths = [
        [7, 7, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [3, 0, 0, 0, 0, 0, 20, False],
        [0, -7, 0, 0, 0, 0, 20, False],
        [-10, 0, 0, 0, 0, 0, 20, False],
        [0, 7, 0, 0, 0, 0, 0, False],
        [4, 0, 0, 0, 0, 0, 0, False],
        [0, -4, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [-4, 7, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def H(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [5, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [5, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 3, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def I(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 4, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, -2, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, -2, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 4, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 3, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def J(arm):
    paths = [
        [10, 6, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 3, False],
        [0, -6, 0, 0, 0, 0, 0, False],
        [0, 9, -5, 0, 0, 0, 0, False],
    ]
    
    return paths



def K(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 5, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-5, -5, 0, 0, 0, 0, 0, False],
        [-5, 5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 3, 0, 0, 0, 0, 0, False],        
    ]
    
    return paths



def L(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 6, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 3, 0, 0, 0, 0, 0, True]
    ]
    
    return paths



def M(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-5, 5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [5, 5, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-5, -5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [5, 5, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 3, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def N(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 6, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 3, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def O(arm):

    paths = [
        [0, 5, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, -5, 0, 0, 0, 0, 10, False],
        [10, 0, 0, 0, 0, 0, 10, False],
        [0, 10, 0, 0, 0, 0, 10, False],
        [-10, 0, 0, 0, 0, 0, 10, False],
        [0, -5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 8, 0, 0, 0, 0, 0, False],
    ]

    return paths



def P(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 5, 0, 0, 0, 0, 3, False],
        [-5, 0, 0, 0, 0, 0, 3, False],
        [0, -5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [-5, 8, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def Q(arm):
    
    paths = [
        [0, 5, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, -5, 0, 0, 0, 0, 10, False],
        [10, 0, 0, 0, 0, 0, 10, False],
        [0, 10, 0, 0, 0, 0, 10, False],
        [-10, 0, 0, 0, 0, 0, 10, False],
        [0, -5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [5, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],  
        [-8, 5, 0, 0, 0, 0, 0, False],    
        [0, 0, -5, 0, 0, 0, 0, False],       
        [3, 3, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def R(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 5, 0, 0, 0, 0, 3, False],
        [-5, 0, 0, 0, 0, 0, 3, False],
        [0, -5, 0, 0, 0, 0, -1, False],
        [0, 0, 0, 0, 0, 0, 0, False],
        [-5, 5, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 3, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def S(arm):
    paths = [
        [10, 6, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, -6, 0, 0, 0, 0, 5, False],
        [-5, 0, 0, 0, 0, 0, 5, False],
        [0, 6, 0, 0, 0, 0, 5, False],
        [-5, 0, 0, 0, 0, 0, 5, False],
        [0, -6, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 9, 0, 0, 0, 0, 0, False],
    ]
    
    return paths


def T(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [0, 8, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, -4, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 7, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def U(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 0, 0, 0, 0, 0, 3, False],
        [0, 6, 0, 0, 0, 0, 3, False],
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [-10, 3, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def V(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 4, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 4, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, -4, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 7, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def W(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 3, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [5, 3, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-5, -3, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [5, 3, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-5, 3, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 3, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, -3, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 6, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def X(arm):
    paths = [
        [10, 7, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, -7, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-10, 7, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 3, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def Y(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-4, 4, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [4, 4, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False],
        [-4, -4, 0, 0, 0, 0, 0, False],
        [-6, 0, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 7, 0, 0, 0, 0, 0, False],
    ]
    
    return paths



def Z(arm):
    paths = [
        [10, 0, 0, 0, 0, 0, 0, False],
        [0, 0, 5, 0, 0, 0, 0, False], 
        [0, 8, 0, 0, 0, 0, 0, False],
        [-10, -8, 0, 0, 0, 0, 0, False],
        [0, 8, 0, 0, 0, 0, 0, False],
        [0, 0, -5, 0, 0, 0, 0, False],
        [0, 3, 0, 0, 0, 0, 0, False],
    ]

    return paths


# arm.set_tool_position(x=, y=, wait=True)
# [0, 0, 0, 0, 0, 0, 0, False],
