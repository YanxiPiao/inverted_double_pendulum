'''balancing an inverted double pendulum'''

from math import *


# specs
mass_pen1=131 # pendulum 1 mass [g]
len1=10#213 # link 1 length [mm]
mass_pen2=145 # 110g bearing +35 pendulum 2 mass [g]
len2=10 # 11.35 # link 2 length [mm]
x=0.0
y=0.0
cmx=0 # center of mass on x axis. 0 for -x, 1 for +x

# let theta3 be the angle of the end effector to y-axis
# input: imu reading for theta1, servo angle for theta2;
# output: angle for the end effector to y-axis
def get_theta3(theta1,theta2):
    global x,y,cmx
    q1=90+theta1
    q2=theta2-90
    x=len1*cos(radians(q1))+len2*cos(radians(q1+q2))
    y=len1*sin(radians(q1))+len2*sin(radians(q1+q2))
    if x==0:
        x+=0.001
    angle=degrees(atan(y/x))
    #print('angle',angle)
    if angle<0:
        angle=(angle+90)*(-1)
        cmx=0
    else:
        angle=90-angle
        cmx=1
    #print('q1,q2',q1,q2)
    #print('x,y',x,y)
    #print('right angle', angle)
    #print('dir', cmx)
    return angle

# calculate torque for the system
def get_torque (theta1 , theta3):
    if theta1 < 0:
        t1 = mass_pen1*len1*sin(radians(theta1))
    else:
        t1 = mass_pen1 * len1 * sin(radians(theta1))
    t2=mass_pen2*get_dist(x,y)*sin(radians(theta3))
    #print(t1,t2,theta3)
    return t1+t2

def get_dist(x,y):
    return sqrt((x*x)+(y*y))

def get_theta2(torque,theta1):
    t1 = mass_pen1 * len1 * sin(radians(theta1))



    return 0
i=0
j=-90
while j<90:
    while i<180:
        test = get_torque(j, get_theta3(j, i))
        if abs(test)<0.2:
            #print('theta1:%d theta2: %f torque: %f' %(j,i,test))
            print(i)

        i+=0.01
    i=0
    j+=1

'''while i<180:
    test = get_torque(0, get_theta3(0, i))
    if abs(test)<1:
        print('the pairrrrrrrrrrrs:',1,i,test)

    i+=0.01
'''