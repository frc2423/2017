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


def main():
  cs = CameraServer.getInstance()
  cs.enableLogging()

  gearCamera = cs.startAutomaticCapture(dev=0) # which camera is this?
  camera2 = cs.startAutomaticCapture(dev=1) # which camera is this?
  gearCamera.setResolution(320, 240)
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

    # Put a rectangle on the image
    #cv2.rectangle(gearImg, (100, 100), (300, 300), (255, 255, 255), 5)
    gray_image = cv2.cvtColor(gearImg, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, 250, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)  # dilates then erodes, removes dots inside rectangles
    _, contours, _ = cv2.findContours(closing, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # look for squarish contours
    square_contours = []
    for cnt in contours:
      epsilon = 0.07 * cv2.arcLength(cnt, True) # 7% arc length... removes sides in the shapes to detects rectangles
      approx = cv2.approxPolyDP(cnt, epsilon, True)
      if len(approx) == 4:
        square_contours.append(cnt)

    # look for shapes that are close to each other and are similar size
    contours_with_pairs_indexes = []
    for i in range(0, len(square_contours) - 1):
      for j in range(i + 1, len(square_contours)):
        # Don't bother checking if both of them have already been added to the filter
        if i in contours_with_pairs_indexes and j in contours_with_pairs_indexes:
          continue

        cnt1 = square_contours[i]
        cnt2 = square_contours[j]

        x1, y1, w1, h1 = cv2.boundingRect(cnt1)
        x2, y2, w2, h2 = cv2.boundingRect(cnt2)

        if .5 < w1/w2 < 2 and .8 < h1/h2 < 1.2:
          if i not in contours_with_pairs_indexes:
            contours_with_pairs_indexes.append(i)
          if j not in contours_with_pairs_indexes:
            contours_with_pairs_indexes.append(j)

    contours_with_pairs = [square_contours[index] for index in contours_with_pairs_indexes]

    cv2.drawContours(gearImg, contours, -1, (0, 0, 255), 2)
    cv2.drawContours(gearImg, square_contours, -1, (0, 255, 0), 3)

    # Give the output stream a new image to display
    outputStream.putFrame(gearImg)
