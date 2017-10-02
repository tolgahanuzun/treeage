import cv2
import numpy as np
import pyimgur


CLIENT_ID = "youkey"
PATH = "./"

def treeage(imageurl):
    """
    Yas halkalari hesaplama.
    Resmin konumunu alir, imgura yukler ve geriye halka sayisiyla link doner.
    """
    img = cv2.imread(imageurl, 0)
    img = cv2.medianBlur(img, 1)
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    cimg = cv2.cvtColor(th2, cv2.COLOR_GRAY2BGR)
    circles = cv2.HoughCircles(th2, cv2.HOUGH_GRADIENT, 50, 2000)
    circles = np.uint16(np.around(circles))

    # orta noktasini buluyoruz.
    for i in circles[0, :]:
        cv2.circle(cimg, (i[0], i[1]), 2, (0, 0, 255), 3)

    #Resmi 4e boluyoruz.
    draws1 = cimg[0:circles[0][0][1], 0:circles[0][0][0]]
    draws1 = cv2.flip(draws1, 1)
    draws1 = cv2.flip(draws1, 0)

    draws2 = cimg[circles[0][0][1]:, 0:circles[0][0][0]]
    draws2 = cv2.flip(draws2, 1)

    draws3 = cimg[0:circles[0][0][1], circles[0][0][0]:]
    draws3 = cv2.flip(draws3, 0)

    draws4 = cimg[circles[0][0][1]:, circles[0][0][0]:]

    drawss = [draws1, draws2, draws3, draws4]
    sayac = 0

    for draws in drawss:
        height, width = draws.shape[:2]

        ages = height
        oran = width/height
        if height > width:
            ages = width
            oran = height/width

        temp1 = None
        temp2 = None

        for x in range(ages):
            try:
                if draws[x, int(x*oran)][0] == 0 and not temp1 == 0 and not temp2 == 0:
                    sayac = sayac+1
                    draws[x, int(x*oran)] = [0, 0, 255]

                temp1 = draws[x, int(x*oran)][0]
                temp2 = draws[x-1, int(x*oran)-1][0]
            except:
                pass
        for x in range(ages):
            try:
                draws[x, int(x*oran)] = [0, 0, 255]
            except:
                pass

    agename = '{}-age.jpg'.format(imageurl.split('.')[0])
    cv2.imwrite(agename, cimg)

    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(agename, title="Uploaded with PyImgur")
    print(uploaded_image.title)
    uploaded_image.link
    
    return int(sayac/4), uploaded_image.link

    # cv2.imshow('detected circle1',draws1)
    # cv2.imshow('detected circle2',draws2)
    # cv2.imshow('detected circle3',draws3)
    # cv2.imshow('detected circle4',draws4)

    #import ipdb; ipdb.set_trace()

    #for x in range(20):
        #draws[x,x] =[0,0,255]
    #cv2.imshow('detected circles',draws)


    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
