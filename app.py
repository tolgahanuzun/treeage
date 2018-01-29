import cv2
import numpy as np
import pyimgur


CLIENT_ID = "ccc"

def treeage(imageurl):
    img = cv2.imread(imageurl, 0)
    img = cv2.medianBlur(img, 1)
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    cimg = cv2.cvtColor(th2, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(th2, cv2.HOUGH_GRADIENT, 50, 2000)
    circles = np.uint16(np.around(circles))

    # center point
    for i in circles[0, :]:
        cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

    draw1 = cimg[0:circles[0][0][1], 0:circles[0][0][0]]
    draw1 = cv2.flip(draw1, 1)
    draw1 = cv2.flip(draw1, 0)

    draw2 = cimg[circles[0][0][1]:, 0:circles[0][0][0]]
    draw2 = cv2.flip(draw2, 1)

    draw3 = cimg[0:circles[0][0][1], circles[0][0][0]:]
    draw3 = cv2.flip(draw3, 0)

    draw4 = cimg[circles[0][0][1]:, circles[0][0][0]:]

    draws = [draw1, draw2, draw3, draw4]
    counter = 0

    for draw in draws:
        height, width = draw.shape[:2]

        ages = height
        rate = width/height
        if height > width:
            ages = width
            rate = height/width

        temp1 = None
        temp2 = None

        for x in range(ages):
            try:
                if draw[x, int(x*rate)][0] == 0 and not temp1 == 0 and not temp2 == 0:
                    counter = counter + 1
                    draw[x, int(x*rate)] = [0, 0, 255]

                temp1 = draw[x, int(x*rate)][0]
                temp2 = draw[x-1, int(x*rate)-1][0]
            except:
                pass
        for x in range(ages):
            try:
                draw[x, int(x*rate)] = [0, 0, 255]
            except:
                pass

    agename = '{}-age.jpg'.format(imageurl.split('.')[0])
    cv2.imwrite(agename, cimg)

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(agename, title="Uploaded with PyImgur")
    print(uploaded_image.title)

    return int(counter/4), uploaded_image.link
