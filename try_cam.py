#!/usr/bin/env python3

import cv2

if __name__ == '__main__':
	cap = cv2.VideoCapture(0)
	ret, frame = cap.read()
	cv2.imwrite('test.jpg', frame)
	print(ret)
