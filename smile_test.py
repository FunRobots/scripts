import rospy
from sensor_msgs.msg import Image
import sys
sys.path.insert(1, '/usr/local/lib/python3.5/dist-packages')

import cv2
import ros_numpy

if __name__ == '__main__':
    rospy.init_node('smile_test')

    photo_folder = 'photos'

    pub = rospy.Publisher('/vision_camera_capture/image', Image, queue_size=1)
    
    while True:
        ans = input('image name: ')
        try:
            frame = cv2.imread(photo_folder + '/' + ans)
            img = ros_numpy.msgify(Image, frame, encoding='rgb8')
            pub.publish(img)
        except Exception as e:
            print('photo not found or ', str(e))
