import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import math
from contrast.convert import Convert

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
    (width, height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX, 2, 3)
    if image.shape[1] < height or image.shape[0] < width:
        return -1
    else:
        blankImage = np.zeros(shape=image.shape, dtype=np.uint8)
        # cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
        cv2.putText(
            blankImage,
            text,
            (x, height + y),
            cv2.FONT_HERSHEY_COMPLEX,
            2,
            (255, 255, 255),
            3,
            cv2.LINE_AA,
            False
        );
        return blankImage, width, height

def convertImageToContrast(imageRGB, contrast=4.5):
    # get all unique colors
    colors = np.unique(imageRGB.reshape(-1, imageRGB.shape[2]),axis=0)
    print(len(colors), " unique colors");
    # get contrasts of all colors
    new_colors = [];
    for color in colors:
        contrast_color = Convert().transform(color / 256, contrast)
        new_colors.append((np.array(contrast_color) * 256).astype("uint8"));

    # convert each pixel of current image to use the new colors
    red, green, blue = imageRGB[:,:,0], imageRGB[:,:,1], imageRGB[:,:,2]
    for i in range(0, len(colors)):
        color = colors[i];
        mask = (red == color[0]) & (green == color[1]) & (blue == color[2])
        imageRGB[:,:,:3][mask] = new_colors[i]

    return imageRGB;


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

def testContrast():
    x = 20
    y = 20
    rgb, hsv = openImage('Capture.png')
    textImage, width, height = createTextCanvas("Ayman", rgb, 0, x, y)
    newImageRGB = convertImageToContrast(rgb.copy(), 4.5)
    plt.imshow(newImageRGB)
    plt.show()
    writtenImage = writeContrastCaption(rgb, newImageRGB, textImage, x, y, width, height)
    plt.imshow(writtenImage)
    plt.show()

def testHSV():
    x = 20
    y = 20
    rgb, hsv = openImage('Capture.png')
    textImage, width, height = createTextCanvas("Ayman", rgb, 0, x, y)
    writtenImage = writeCaption(rgb, hsv, textImage, x, y, width, height)
    plt.imshow(writtenImage)
    plt.show()

testHSV();
testContrast();

# frame = np.ones([400,400,3])*255
# lbls = ['standUp', 'front', 'lookU', 'lookF', 'lookDF', 'HandOnHipR']

# offset = 35
# x,y = 50,50
# for idx,lbl in enumerate(lbls):
#     print(x,y+offset*idx)
#     cv2.putText(frame, str(lbl), (x,y+offset*idx), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

# plt.imshow(frame)
# plt.show()

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
# print(Convert().transform([0,0,1.0], 4.5))