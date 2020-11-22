import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import math
from contrast.convert import Convert

def openImage(image):
    # imageBGR = cv2.imread(os.path.join("images", image))
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    return imageRGB, imageHSV

def showImage(img, img2 = None):
    if (img2.any()):
        plt.subplot(1,2,1);
        plt.imshow(img);
        plt.subplot(1,2,2);
        plt.imshow(img2);
    else:
        plt.imshow(img);
    plt.show();


def createTextCanvas(text, image, fontIndex, x, y, textProperties):
    # getTextSize(text, Font, Scale, Thickness)
    textProperties['font_family']
    if textProperties['font_family'] and int(textProperties['font_family']) < 8:
        textProperties['font_family'] = int(textProperties['font_family'])
    else:
        textProperties['font_family'] = 0
    if textProperties['font_size'] == 1:
        scale = 2
        thickness = 2
    elif textProperties['font_size'] == 2:
        scale = 2
        thickness = 3
    else:
        scale = 2
        thickness = 3
    (width, height), baseline = cv2.getTextSize(text, textProperties['font_family'], scale, thickness)
    if image.shape[1] < height or image.shape[0] < width:
        return -1
    else:
        blankImage = np.zeros(shape=image.shape, dtype=np.uint8)
        # cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
        cv2.putText(
            blankImage,
            text,
            (x, height + y),
            textProperties['font_family'],
            scale,
            (255, 255, 255),
            thickness,
            cv2.LINE_AA,
            False
        );
        return blankImage, width, height

def writeCaption(imageRGB, imageHSV, textImage, x, y, width, height):
    imagePatch = imageRGB[x:x+height, y:y+width, :]
    imageInverse = cv2.bitwise_not(imageHSV)

    indices = np.where(np.all(textImage == 255, axis=-1))
    # print indices
    coordinates = [*zip(indices[0], indices[1])]
    for i in coordinates:
        imageRGB[i[0], i[1], :] = imageInverse[i[0], i[1], :]
    return imageRGB

def writeContrastCaption(imageRGB, imageContrast, textImage, x, y, width, height):
    imageInverse = imageContrast
    indices = np.where(np.all(textImage == 255, axis=-1))
    coordinates = [*zip(indices[0], indices[1])]
    for i in coordinates:
        imageRGB[i[0], i[1], :] = imageInverse[i[0], i[1], :]
    return imageRGB;


def testContrast(image_name, text, x, y, textProperties, contrast = 15.0):
    rgb, hsv = openImage(image_name)
    textImage, width, height = createTextCanvas(text, rgb, 0, x, y, textProperties)
    newImageRGB = Convert().image(rgb.copy(), contrast)
    # showImage(newImageRGB);
    writtenImage = writeContrastCaption(rgb, newImageRGB, textImage, x, y, width, height)
    return writtenImage;

def testHSV(image_name, text, x, y, textProperties):
    rgb, hsv = openImage(image_name)
    textImage, width, height = createTextCanvas(text, rgb, 0, x, y, textProperties)
    # showImage(hsv);
    writtenImage = writeCaption(rgb, hsv, textImage, x, y, width, height)
    return writtenImage;