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


def smoothing_title_box(my_image, subtitle_position_height0, subtitle_position_height1, subtitle_position_width0,
                        subtitle_position_width1, alpha=1):
    # subtitle_position_height0, subtitle_position_height1,subtitle_position_width0,subtitle_position_width1 = 130, 146, 150,550
    im_h, im_w = abs(subtitle_position_height1 - subtitle_position_height0), abs(
        subtitle_position_width1 - subtitle_position_width0)
    bl_h, bl_w = 8, 8
    # alpha is number of standard deviation from mean intensity of block (bl_h, bh_w) which we wants remove the outlayer intensities from orginal image.
    dct_after_std_all_blocks = np.zeros(my_image.shape)
    for channel in range(3):
        for row in np.arange(im_h - bl_h + 1, step=bl_h):
            for col in np.arange(im_w - bl_w + 1, step=bl_w):
                block = my_image[subtitle_position_height0 + row:subtitle_position_height0 + row + bl_h,
                        subtitle_position_width0 + col:subtitle_position_width0 + col + bl_w, channel].copy()
                block[np.logical_or((block > np.mean(block) + alpha * np.std(block)),
                                    (block < np.mean(block) - alpha * np.std(block)))] = np.mean(block)
                dct_after_std_all_blocks[subtitle_position_height0 + row:subtitle_position_height0 + row + bl_h,
                subtitle_position_width0 + col:subtitle_position_width0 + col + bl_w, channel] = cv2.dct(block)

    idct_after_std_all_blocks = np.zeros(my_image.shape)
    for channel in range(3):
        for row in np.arange(im_h - bl_h + 1, step=bl_h):
            for col in np.arange(im_w - bl_w + 1, step=bl_w):
                idct_after_std_all_blocks[subtitle_position_height0 + row: subtitle_position_height0 + row + bl_h,
                subtitle_position_width0 + col: subtitle_position_width0 + col + bl_w, channel] = cv2.idct(
                    dct_after_std_all_blocks[subtitle_position_height0 + row:subtitle_position_height0 + row + bl_h,
                    subtitle_position_width0 + col: subtitle_position_width0 + col + bl_w, channel])

    new_image = my_image.copy()
    new_image[subtitle_position_height0: subtitle_position_height1, subtitle_position_width0: subtitle_position_width1,
    :] = idct_after_std_all_blocks[subtitle_position_height0: subtitle_position_height1,
         subtitle_position_width0: subtitle_position_width1, :]
    color = [0, 0, 0]
    new_image[subtitle_position_height0: subtitle_position_height0 + 1,
    subtitle_position_width0: subtitle_position_width1, :] = color
    new_image[subtitle_position_height1 - 1: subtitle_position_height1,
    subtitle_position_width0: subtitle_position_width1, :] = color
    new_image[subtitle_position_height0: subtitle_position_height1,
    subtitle_position_width0: subtitle_position_width0 + 1, :] = color
    new_image[subtitle_position_height0: subtitle_position_height1,
    subtitle_position_width1 - 1: subtitle_position_width1, :] = color

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(my_image, cmap='gray');
    ax1.title.set_text('original')
    ax2.imshow(new_image, cmap='gray');
    ax2.title.set_text('after smooting outlayers')
    fig.suptitle('the averaging the image which has higher or lower value than {alpha} standard deviation from mean')
    plt.show()
    return new_image



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
    # textImage, width, height = createTextCanvas(text, rgb, 0, x, y, textProperties)
    # newHSV = smoothing_title_box(hsv, y, x , y + height, x + width, alpha= 1)
    # writtenImage = writeCaption(rgb, newHSV, textImage, x, y, width, height)
    textImage, width, height = createTextCanvas(text, rgb, 0, x, y, textProperties)
    # showImage(hsv);
    writtenImage = writeCaption(rgb, hsv, textImage, x, y, width, height)
    return writtenImage;

# image = 'image3.png';
# text = "ayman";
# x = 50;
# y = 50;
# hsvImage = testHSV(image, text, x, y);
# showImage(hsvImage);
# contrastImage = testContrast(image, text, x, y);
# showImage(hsvImage, contrastImage);

# size = 250
# blank_image = np.zeros((size,size,3))
# red = blank_image.copy();
# red[:,:,0] = 255
# plt.imsave("images/red.png", red);
# green = blank_image.copy();
# green[:,:,1] = 255
# plt.imsave("images/green.png", green);
# blue = blank_image.copy();
# blue[:,:,2] = 255
# plt.imsave("images/blue.png", blue);
# magenta = blank_image.copy();
# magenta[:,:,0] = 255
# magenta[:,:,2] = 255
# plt.imsave("images/magenta.png", magenta);
# cyan = blank_image.copy();
# cyan[:,:,1] = 255
# cyan[:,:,2] = 255
# plt.imsave("images/cyan.png", cyan);
# yellow = blank_image.copy();
# yellow[:,:,0] = 255
# yellow[:,:,1] = 255
# plt.imsave("images/yellow.png", yellow);
# white = blank_image.copy();
# white[:,:,0] = 255
# white[:,:,1] = 255
# white[:,:,2] = 255
# plt.imsave("images/white.png", white);
# gray = blank_image.copy();
# gray[:,:,0] = 128
# gray[:,:,1] = 128
# gray[:,:,2] = 128
# plt.imsave("images/gray.png", gray);
# black = blank_image.copy();
# plt.imsave("images/black.png", black);


# showImage(hsvImage, contrastImage);
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