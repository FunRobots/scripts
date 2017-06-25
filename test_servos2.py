#!/usr/bin/env python3

TEST_HEAD_FOLDER='test_servo_folder'

import rospy
import os

if os.path.exists(TEST_HEAD_FOLDER) is False:
    os.mkdir(TEST_HEAD_FOLDER)

import sys
try:
    import cv2
except:
    sys.path.insert(1, '/usr/local/lib/python3.5/dist-packages')
    import cv2


import getch

from motion.head.head_publisher import HeadPublisher
from motion.eyes.eyes_publisher import EyesPublisher
from motion.eyebrows.eyebrows_publisher import EyebrowsPublisher

from motion.candy_dispenser.candy_dispenser_controller import Dispenser

import serial
TIMEOUT = 5
import time

import ros_numpy
from sensor_msgs.msg import Image

hp = HeadPublisher()
ep = EyesPublisher()
ebp = EyebrowsPublisher()

if not ['/vision_camera_capture/image', 'sensor_msgs/Image'] in rospy.get_published_topics():
    cap = cv2.VideoCapture(0)

def im_cap_and_save(name):
    if 'cap' in globals():
        global cap
    
        time.sleep(1)
        ret, frame = cap.read()
        if ret is True:
            cv2.imwrite(TEST_HEAD_FOLDER + '/' + name, frame)

    else:

        def callback_photo(data: Image):
            try:
                cv2.imwrite(TEST_HEAD_FOLDER + '/' + name, ros_numpy.numpify(data))
            except Exception as e:
                print('image saving error: ', str(e))
                
          
        get_im_sub = rospy.Subscriber('/vision_face_tracking/face_image', Image, lock_recognize.callback)
        time.sleep(1)
        get_im_sub.unregister()
        


def control_head():
    global hp
    
    clear = os.system('clear')
    
    step = 5
    h_angle = 90
    v_angle = 90
    
    if rospy.has_param('/head/h_angle') and rospy.has_param('/head/v_angle'):
        h_angle = rospy.get_param('/head/h_angle')
        v_angle = rospy.get_param('/head/v_angle')
    
    ans = ''
    while ans != 'q':
        print('h_angle: {0}, v_angle: {1}'.format(h_angle, v_angle))
        print('WASD - control head, q - exit')
        ans = getch.getch()

        if ans == 'w':
            hp.move_v_angle(-step)
        elif ans == 's':
            hp.move_v_angle(step)
        elif ans == 'l':
            hp.move_h_angle(step)
        elif ans == 'r':
            hp.move_h_angle(-step)
        else:
            pass

        im_cap_and_save('head({0} {1})'.format(str(h_angle) + '.png', str(v_angle)))
        clear = os.system('clear')
        


def control_eyes():
    global ep
    
    clear = os.system('clear')
    
    x = 0
    y = 0
    
    if rospy.has_param('/eyes/x') and rospy.has_param('/eyes/y'):
        x = rospy.get_param('/eyes/x')
        y = rospy.get_param('/eyes/y')
    
    ans = ''
    while ans != 'q':
        print('x: {0}, y: {1}'.format(x, y))
        print('WASD - control eyes, c - center eyes, q - exit')
        ans = getch.getch()

        if ans == 'w':
            ep.move_up()
        elif ans == 's':
            ep.move_down()
        elif ans == 'l':
            ep.move_left()
        elif ans == 'r':
            ep.move_right()
        elif ans == 'c':
            ep.move_center()
        else:
            pass

        clear = os.system('clear')



def control_eyebrows():
    global ebp

    clear = os.system('clear')
    
    step = 5
    l_angle = 98
    r_angle = 75
    
    if rospy.has_param('/eyebrows/l_angle') and rospy.has_param('/eyebrows/r_angle'):
        l_angle = rospy.get_param('/eyebrows/l_angle')
        r_angle = rospy.get_param('/eyebrows/r_angle')
    
    ans = ''
    while ans != 'q':
        print('l_angle: {0}, r_angle: {1}'.format(l_angle, r_angle))
        print('WS - control eyebrows, c - center eyebrows, q - exit')
        ans = getch.getch()

        if ans == 'w':
            ebp.move_up()
        elif ans == 's':
            ebp.move_down()
        else:
            pass

        clear = os.system('clear')


def menu():
    print('1. head')
    print('2. eyes')
    print('3. eyebrows')
    print('4. take candy')
    print('5. exit')

    
if __name__ == '__main__':
    global TIMEOUT
    rospy.init_node('test_head')

    
    dispenser = Dispenser(SERVO_CHANNEL=4)
    ser = serial.Serial('/dev/ttyACM0', 9600)
    
    while True:
        menu()
        ans = input('>')
        point = int(ans)
        if point == 5:
            break
        elif point == 1:
            control_head()
        elif point == 2:
            control_eyes()
        elif point == 3:
            control_eyebrows()
        elif point == 4: #rotate dispenser servo until give candy
            start = time.time()
            dispenser.run()
            while time.time() - start < TIMEOUT:
                if ser.read(4) == b'true': #if candy dispensing sensor sent true
                    print('candy!')
                    break
            dispenser.stop()
            print('candy timeout!')
        else:
            print('invalid input')
