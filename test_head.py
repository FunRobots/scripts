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

import time


def menu():
    print('1. h_angle = v_angle = 90')
    print('2. set horizontal angle')
    print('3. set vertical angle')
    print('4. shift horizontal angle')
    print('5. shift vertical angle')
    print('6. exit')

def im_cap_and_save(name):
    time.sleep(1)
    ret, frame = cap.read()
    if ret is True:
        cv2.imwrite(TEST_HEAD_FOLDER + '/' + name, frame)

if __name__ == '__main__':
    rospy.init_node('test_head')
    cap = cv2.VideoCapture(0)

    hp = HeadPublisher()

    while True:
        menu()
        ans = input('>')
        point = int(ans)
        if point == 6:
            break
        elif point == 1:
            hp.set_h_angle(90)
            hp.set_v_angle(90)
            im_cap_and_save('9090.png')
        else:
            angle = float(input('\t input angle'))
            if point == 2:
                hp.set_h_angle(angle)
                im_cap_and_save('set_h_' + str(angle) + '.png')
            elif point == 3:
                hp.set_v_angle(angle)
                im_cap_and_save('set_v_' + str(angle) + '.png')
            elif point == 4:
                hp.shift_h_angle(angle)
                im_cap_and_save('shift_h_' + str(angle) + '.png')
            elif point == 5:
                hp.shift_v_angle(angle)
                im_cap_and_save('shift_v_' + str(angle) + '.png')
            else:
                print('invalid input')
