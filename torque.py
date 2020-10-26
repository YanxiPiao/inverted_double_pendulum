'''balancing an inverted double pendulum'''

from math import *

# specs
mass_pen1=131 # pendulum 1 mass [g]
len1=213 # link 1 length [mm]
mass_pen2=145 # 110g bearing +35 pendulum 2 mass [g]
len2=11.35 # link 2 length [mm]
x=0.0 # x position of the end effector
y=0.0 # y position of the end effector

# let theta3 be the angle of the end effector to y-axis
# input: imu reading for theta1, servo angle for theta2;
# output: angle for the end effector to y-axis
def get_theta3(theta1,theta2):
    global x,y
    q1=90+theta1
    q2=theta2-90
    x=len1*cos(radians(q1))+len2*cos(radians(q1+q2))
    y=len1*sin(radians(q1))+len2*sin(radians(q1+q2))
    if x==0:
        x+=0.001
    angle=degrees(atan(y/x))
    if angle<0:
        angle=(angle+90)*(-1)
    else:
        angle=90-angle
    return angle

# calculate torque for the system
def get_torque (theta1 , theta3):
    t1 = mass_pen1*len1*sin(radians(theta1))
    t2 = mass_pen2*get_dist(x,y)*sin(radians(theta3))
    return t1+t2

def get_dist(x,y):
    return sqrt((x*x)+(y*y))

# this function generates the theta1 and theta2 pairs that will make the system torque zero with 0.2 error
# the points are used to generate a function of theta2 from theta1 input.
def get_theta2():
    i = 0
    j = -90
    while j < 90:
        while i < 180:
            torque = get_torque(j, get_theta3(j, i))
            if abs(torque) < 0.2:
                print('theta1:%d theta2: %f torque: %f' % (j, i, torque))
            i += 0.01
        i = 0
        j += 1

get_theta2()
