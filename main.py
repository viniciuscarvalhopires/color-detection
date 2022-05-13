import argparse
import cv2
import pandas as pd
from PIL import Image
import os
import PIL
import glob

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']
img = cv2.imread(img_path)

clicked = False
r = g = b = xpos = ypos = 0

cIndex = ["color", "color_name", "hex", "R", "G", "B"]
# names -> List of column names to use
csv = pd.read_csv(r'files/colors.csv', names=cIndex, header=None)


# function to calculate minimum distance from all colors and get the most matching color
def get_colorname(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        # abs() return the absolute value of a number
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname


# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, xpos, ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)


# Display the image in the window
cv2.namedWindow('image')
# onMouse movement on image it will execute draw_function and calculate the rgb
cv2.setMouseCallback('image', draw_function)

while 1:
    cv2.imshow('image', img)
    if clicked:
        # cv2.rectangle(image, startpoint, endpoint, color, thickness) -1 thickness fills rectangle entirely
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

        # Creating text string to display (Color name and RGB Values)
        text = get_colorname(r, g, b) + 'R = ' + str(r) + ' G = ' + str(g) + ' B = ' + str(b)

        # cv2.putText(img,text,start,font(0-7), fontScale, color, thickness, lineType, (optional bottomLeft bool))
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        clicked = False

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
