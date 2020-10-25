'''balancing an inverted double pendulum'''

import math

# specs
mass_pen1=131 # pendulum 1 mass [g]
len1=213 # link 1 length [mm]
mass_pen2=145 # 110g bearing +35 pendulum 2 mass [g]
len2=11.35 # link 2 length [mm]
x=0.0
y=0.0

# let theta3 be the angle of the end effector to y-axis
def get_theta3(theta1,theta2):
    global x,y
    q1=90+theta1
    q2=theta2-90
    x=len1*math.cos(q1)+len2*math.cos(q1+q2)
    y=len1*math.sin(q1)+len2*math.cos(q1+q2)
    angle=90-math.atan(y/x)
    return angle

# calculate torque for the system
def get_torque(theta1,theta3):
    t1=mass_pen1*len1*math.sin(theta1)
    t2=mass_pen2*get_dist(x,y)*math.sin(theta3)
    return t1+t2

def get_dist(x,y):
    return math.sqrt((x*x)+(y*y))

def get_theta2(torque):
    return 0

