#
# This is a demo program showing CameraServer usage with OpenCV to do image
# processing. The image is acquired from the USB camera, then a rectangle
# is put on the image and sent to the dashboard. OpenCV has many methods
# for different types of processing.
#
# NOTE: This code runs in its own process, so we cannot access the robot here,
#       nor can we create/use/see wpilib objects
#
# To try this code out locally (if you have robotpy-cscore installed), you
# can execute `python3 -m cscore vision.py:main`
#
# Checkout camera feed 1 at http://roborio-2423-frc.local:1181
# Checkout camera feed 2 at http://roborio-2423-frc.local:1182
# Checkout camera feed 3 at http://roborio-2423-frc.local:1183 to get filtered gear image
#

import cv2
import numpy as np

from cscore import CameraServer
from cscore import UsbCamera

from networktables import NetworkTable
from networktables.util import ntproperty



THRESHOLD = 200
MIN_AREA = 300


def large_contour_filter(contours):

    filtered_contours = []
    for cnt in contours:
        x1, y1, w1, h1 = cv2.boundingRect(cnt)
        area = cv2.contourArea(cnt)
        #print(area)
        if area > MIN_AREA:
            filtered_contours.append(cnt)
            #print(area)

    return filtered_contours


def square_contour_filter(contours):
    square_contours = []
    for cnt in contours:
        epsilon = 0.06 * cv2.arcLength(cnt, True)  # 7% arc length... removes sides in the shapes to detects rectangles
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        #print(len(approx))
        if len(approx) == 4:
            square_contours.append(cnt)

    return square_contours


def pair_filter(contours):

    best_pairs = None, None
    best_pair_score = 0

    for i in range(0, len(contours) - 1):
        for j in range(i + 1, len(contours)):

            cnt1 = contours[i]
            cnt2 = contours[j]

            x1, y1, w1, h1 = cv2.boundingRect(cnt1)
            x2, y2, w2, h2 = cv2.boundingRect(cnt2)

            if abs(x1 - x2) > 20 and (y1 - y2) < 40 and .5 < w1 / w2 < 2 and .8 < h1 / h2 < 1.2:
                print('(', len(contours), i, j, ') (', x1,y1,w1,h1,') (', x2, y2, w2, h2, ')')
                score = max(y1, y2)
                if score > best_pair_score:
                    best_pairs = (cnt1, cnt2)
                    best_pair_score = score


    return best_pairs


def detect_tape(image):

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, THRESHOLD, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  # dilates then erodes, removes dots inside rectangles
    #edged = cv2.Canny(closing, 30, 200)
    #cv2.imshow('edged', edged)

    _, contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    large_contours = large_contour_filter(contours)
    square_contours = square_contour_filter(large_contours)
    cnt1, cnt2 = pair_filter(square_contours)

    cv2.drawContours(image, contours, -1, (0, 0, 255), 2)

    if cnt1 is not None:
        cv2.drawContours(image, [cnt1, cnt2], -1, (0, 255, 0), 3)

    return cnt1, cnt2






def main():

  

  targetFound = ntproperty('/SmartDashboard/camera/targetFound', False)
  targetWidth = ntproperty('/SmartDashboard/camera/targetWidth', 0)
  targetDistanceFromCenter = ntproperty('/SmartDashboard/camera/targetDistanceFromCenter', 0)
  targetFinderEnabled = ntproperty('/SmartDashboard/camera/targetFinderEnabled', False)



  cs = CameraServer.getInstance()
  cs.enableLogging()

  gearCamera = cs.startAutomaticCapture(dev=0) # which camera is this?
  camera2 = cs.startAutomaticCapture(dev=1) # which camera is this?
  gearCamera.setResolution(320 * 2, 240 * 2)
  camera2.setResolution(320, 240)

  # Get a CvSink. This will capture images from the camera
  gearCvSink = cs.getVideo(camera=gearCamera)


  # (optional) Setup a CvSource. This will send images back to the Dashboard
  outputStream = cs.putVideo("Rectangle", 320, 240)

  # Allocating new images is very expensive, always try to preallocate
  img = np.zeros(shape=(240, 320, 3), dtype=np.uint8)

  while True:
    # Tell the CvSink to grab a frame from the camera and put it
    # in the source image.  If there is an error notify the output.
    time, gearImg = gearCvSink.grabFrame(img)
    if time == 0:
      # Send the output the error.
      outputStream.notifyError(gearCvSink.getError())
      # skip the rest of the current iteration
      continue


    if targetFinderEnabled == False:
        continue

    cnt1, cnt2 = detect_tape(gearImg)

    if cnt1 is None:
      targetFound = False
    else:
      imgWidth, imgHeight = gearImg.shape[:2]

      x1, y1, w1, h1 = cv2.boundingRect(cnt1)
      x2, y2, w2, h2 = cv2.boundingRect(cnt2)

      left = min(x1, x2)
      right = max(x1 + w1, x2 + w2)
      targetWidth = right - left
      targetDistanceFromCenter = (left + right / 2) - imgWidth / 2
      targetFound = True


    # Give the output stream a new image to display
    outputStream.putFrame(gearImg)
