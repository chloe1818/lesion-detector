import cv2
import numpy as np
import math

# Load Image
#once image segmentation is finalized, files will be imported in
img2 = cv2.imread("circle.jpeg", cv2.IMREAD_COLOR)
img = cv2.imread('circle.jpeg', cv2.IMREAD_GRAYSCALE)

# Draw objects boundaries
_, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY)
contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#Create font
font = cv2.FONT_HERSHEY_SIMPLEX

#Extra variables
xcenter = 0
ycenter = 0
distance = []
flag = 1

#Determine center of the image
for cnt in contours:
    #cv2.polylines(img, [cnt], True, (255, 0, 0), 2)

    (x, y), radius = cv2.minEnclosingCircle(cnt)
    center = (int(x), int(y))
    radius = int(radius)
    xcenter  = int(x)
    ycenter = int(y)

    cv2.circle(img2, (int(x), int(y)), 5, (0,0,255), -1)
    #print(x,y)
    #print(center)
    #print(radius)

#Draw contour coordinates
for cnt in contours:

    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)

    # draws boundary of contours.
    cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)

    # Used to flatted the array containing
    # the co-ordinates of the vertices.
    n = approx.ravel()
    i = 0

    for j in n:
        if (i % 2 == 0):
            x = n[i]
            y = n[i + 1]

            # String containing the co-ordinates.
            string = str(x) + " " + str(y)

            if (i == 0):
                # text on topmost co-ordinate.
                cv2.putText(img2, "Arrow tip", (x, y),
                            font, 0.5, (255, 0, 0))

            else:
                # text on remaining co-ordinates.
                cv2.putText(img2, string, (x, y),
                            font, 0.5, (0, 255, 0))

                finalx = abs(x-xcenter)
                finaly = abs(y-ycenter)
                distance.append(math.sqrt(finalx*finalx+finaly*finaly))
                print(distance)

        i = i + 1

#Deterrmine its symmetricity
for x in distance:
  if (abs(x-distance[0])>5):
      flag = 0

if (flag==0):
    print("asymmetrical")
else:
    print("symmetrical")

#Show image
cv2.imshow("Image", img2)
cv2.waitKey(0)
