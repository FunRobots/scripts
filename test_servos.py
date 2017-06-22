#!/usr/bin/env python3

TEST_HEAD_FOLDER='test_head_folder'

import rospy
import os

if os.path.exists(TEST_HEAD_FOLDER) is False:
    os.mkdir(TEST_HEAD_FOLDER)
    
try:
    import cv2
except:
    os.insert(1, '/usr/local/lib/python3.5/dist-packages')
    import cv2


from motion.head.head_publisher import HeadPublisher
from motion.candy_dispenser.candy_dispenser_controller import Dispenser

import serial
TIMEOUT = 10
import time


def menu():
    print('1. head h_angle = v_angle = 90')
    print('2. head set horizontal angle')
    print('3. head set vertical angle')
    print('4. head move horizontal angle')
    print('5. head move vertical angle')
    print('6. dispenser rotate angle')
    print('7. dispenser totate until give candy')
    print('8. exit')

def im_cap_and_save(name):
    time.sleep(1)
    ret, frame = cap.read()
    if ret is True:
        cv2.imwrite(TEST_HEAD_FOLDER + '/' + name, frame)

if __name__ == '__main__':
    rospy.init_node('test_head')
    cap = cv2.VideoCapture(0)

    hp = HeadPublisher()
    dispenser = Dispenser(SERVO_CHANNEL=4)
    ser = serial.Serial('/dev/ttyACM0', 9600)
    
    while True:
        menu()
        ans = input('>')
        point = int(ans)
        if point == 8:
            break
        elif point == 1:
            hp.set_h_angle(90)
            hp.set_v_angle(90)
            im_cap_and_save('9090.png')
        elif point == 7: #rotate dispenser servo until give candy
            start = time.time()
            dispenser.run()
            while time.time() - start < TIMEOUT:
                if ser.read(4) == b'true': #if candy dispensing sensor sent true
                    print('candy!')
                    break
            dispenser.stop()
            print('candy timeout!')
        else:
            angle = float(input('\t input angle: '))
            if point == 2:
                hp.set_h_angle(angle)
                im_cap_and_save('set_h_' + str(angle) + '.png')
            elif point == 3:
                hp.set_v_angle(angle)
                im_cap_and_save('set_v_' + str(angle) + '.png')
            elif point == 4:
                hp.move_h_angle(angle)
                im_cap_and_save('shift_h_' + str(angle) + '.png')
            elif point == 5:
                hp.move_v_angle(angle)
                im_cap_and_save('shift_v_' + str(angle) + '.png')
            elif point == 6:
                dispenser.set_angle(angle)
            else:
                print('invalid input')
