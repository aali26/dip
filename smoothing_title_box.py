from skimage import data, io, filters
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

my_image = io.imread(os.path.join("images", "image3.png"))/255.0 # image intensity need to be float
def smoothing_title_box(my_image, subtitle_position_height0, subtitle_position_height1,subtitle_position_width0,subtitle_position_width1, alpha = 1):
    # subtitle_position_height0, subtitle_position_height1,subtitle_position_width0,subtitle_position_width1 = 130, 146, 150,550
    im_h, im_w = abs(subtitle_position_height1-subtitle_position_height0) , abs(subtitle_position_width1 - subtitle_position_width0)
    bl_h, bl_w = 8, 8
    #alpha is number of standard deviation from mean intensity of block (bl_h, bh_w) which we wants remove the outlayer intensities from orginal image.   
    dct_after_std_all_blocks = np.zeros(my_image.shape)
    for channel in range(3):
        for row in np.arange(im_h - bl_h + 1, step=bl_h):
            for col in np.arange(im_w - bl_w + 1 , step = bl_w):
                block = my_image[subtitle_position_height0 + row:subtitle_position_height0 + row + bl_h, subtitle_position_width0 + col:subtitle_position_width0 + col + bl_w, channel].copy()
                block[np.logical_or((block > np.mean(block) + alpha*np.std(block)), (block < np.mean(block)-alpha*np.std(block)))] = np.mean(block)
                dct_after_std_all_blocks[subtitle_position_height0 + row :subtitle_position_height0 + row + bl_h, subtitle_position_width0 + col :subtitle_position_width0 + col + bl_w, channel] = cv2.dct(block)

    idct_after_std_all_blocks = np.zeros(my_image.shape)    
    for channel in range(3):
        for row in np.arange(im_h - bl_h + 1, step=bl_h):
          for col in np.arange(im_w - bl_w + 1 , step = bl_w):  
              idct_after_std_all_blocks[subtitle_position_height0 + row: subtitle_position_height0 + row + bl_h, subtitle_position_width0 + col : subtitle_position_width0 + col + bl_w, channel] = cv2.idct(dct_after_std_all_blocks[subtitle_position_height0 + row :subtitle_position_height0 + row + bl_h, subtitle_position_width0 + col: subtitle_position_width0 + col+bl_w, channel])          
    
    new_image = my_image.copy()
    new_image[subtitle_position_height0 : subtitle_position_height1,subtitle_position_width0 : subtitle_position_width1, :] = idct_after_std_all_blocks[subtitle_position_height0 : subtitle_position_height1,subtitle_position_width0 : subtitle_position_width1, :]
    color = [0, 0, 0]
    new_image[subtitle_position_height0 : subtitle_position_height0 + 1, subtitle_position_width0 : subtitle_position_width1 , :] = color
    new_image[subtitle_position_height1 -1 : subtitle_position_height1 , subtitle_position_width0 : subtitle_position_width1 , :] = color    
    new_image[ subtitle_position_height0 : subtitle_position_height1, subtitle_position_width0 : subtitle_position_width0 + 1 , :] = color    
    new_image[ subtitle_position_height0 : subtitle_position_height1, subtitle_position_width1 -1 : subtitle_position_width1 , :] = color    

    fig, (ax1, ax2) = plt.subplots(1,2)
    ax1.imshow(my_image, cmap='gray'); ax1.title.set_text('original')
    ax2.imshow(new_image, cmap='gray'); ax2.title.set_text('after smooting outlayers')
    fig.suptitle('the averaging the image which has higher or lower value than {alpha} standard deviation from mean')
    plt.show()
    return new_image
                
smoothing_title_box(my_image, 130, 146 , 150, 550, alpha= 1) #### the range of box need to be multipy of 8 [130, (130 + 8*2), 150: (150 + 8 * 50)] 
    

