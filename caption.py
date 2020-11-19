import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import math

fonts = ["font_Hershey_Simplex", "font_Hershey_Plain", "font_Hershey_Duplex",
         "font_Hershey_Complex", "font_Hershey_Triplex", "font_Hershey_Complex_Small",
         "font_Hershey_Script_Simplex", "font_Hershey_Script_Complex"]

def openImage(image):
    imageBGR = cv2.imread(os.path.join("images", image))
    imageRGB = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2RGB)
    imageHSV = cv2.cvtColor(imageBGR, cv2.COLOR_BGR2HSV)
    return imageRGB, imageHSV


def createTextCanvas(text, image, fontIndex, x, y):
    # getTextSize(text, Font, Scale, Thickness)
    font = fonts[fontIndex].upper()
    (width, height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 2, 2)
    if image.shape[1] < height or image.shape[0] < width:
        return -1
    else:
        blankImage = 0 * np.ones(shape=[height+ baseline, width, 3], dtype=np.uint8)
        # cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
        cv2.putText(blankImage,
                    text,
                    (1, x),
                    cv2.FONT_HERSHEY_COMPLEX,
                    2,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA)
        return blankImage, width, height


def writeCaption(imageRGB, imageHSV, textImage, x, y, width, height):
    imagePatch = imageRGB[x:x+height, y:y+width, :]
    imageInverse = cv2.bitwise_not(imageHSV)
    # plt.imshow(imageInverse)
    # plt.show()
    indices = np.where(np.all(textImage == 255, axis=-1))
    # print indices
    coordinates = [*zip(indices[0], indices[1])]
    for i in coordinates:
        imageRGB[i[0], i[1], :] = imageInverse[i[0], i[1], :]
    plt.imshow(imageRGB)
    plt.show()

x = 50
y = 100
rgb, hsv = openImage('image3.png')
textImage, width, height = createTextCanvas("Ayman", rgb, 0, x, y)
writeCaption(rgb, hsv, textImage, x, y, width, height)
# plt.imshow(textImage)
# plt.show()
# blankImage = 0 * np.ones(shape=[255, 255, 3], dtype=np.uint8)
# imagePatchRGB = imageRGB[200:200+255, 200:200+255, :]
# imagePatch = imageHSV[150:100+255, 150:100+255, :]
# cv2.putText(blankImage, 'Hello', (10, 140), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
#
# indices = np.where(np.all(blankImage == 255, axis=-1))
# # print indices
# coordinates = [*zip(indices[0], indices[1])]
# # for i in coordinates:
# #     blankImage[i[0], i[1], :] = imagePatch[i[0], i[1], :]
# #     imagePatch[i[0], i[1], :] = imagePatch[i[0], i[1], :] + 50
# # plt.imshow(blankImage)
# hueLayer = imageRGB[:, :, 0]
# saturationLayer = imageRGB[:, :, 1]
# valueLayer = imageRGB[:, :, 2]
# f, (ax1, ax2, ax3) =  plt.subplots(1, 3, figsize=(20, 10))
# ax1.set_title("Hue Channel ")
# ax1.imshow(hueLayer)
# ax2.set_title("Saturation Channel ")
# ax2.imshow(saturationLayer)
# ax3.set_title("value Channel ")
# ax3.imshow(valueLayer)
# for i in coordinates:
#     blankImage[i[0], i[1], :] = imagePatch[i[0], i[1], 0]
#     imagePatchRGB[i[0], i[1], :] = imagePatchRGB[i[0], i[1], 2]
#     imagePatchRGB[i[0], i[1], :] = imageHSV[i[0], i[1], 0]
#     # if imageHSV[i[0], i[1], 2] > 128:
#     #     imagePatchRGB[i[0], i[1], :] = 255 - imageHSV[i[0], i[1], 2]
#     # else:
#     #     imagePatchRGB[i[0], i[1], :] = 0 + imageHSV[i[0], i[1], 2]
# # plt.imshow(imagePatchRGB)
# plt.show()
# cv2.imwrite(os.path.join("image", "output.png"), imagePatchRGB)
# size = cv2.getTextSize("Hello",cv2.FONT_HERSHEY_COMPLEX,2,3)
# print(size)

