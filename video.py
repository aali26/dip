import os
import cv2
from datetime import datetime
import numpy as np
import caption

def getVideoInfo(video):
    videoInfo = {
        'width': None,
        'height': None,
        'frame_rate': None,
        'frame_count': None,
        'frames': [],
        'dst_frames': []
    }
    videoHandler = cv2.VideoCapture(os.path.join(video))
    if videoHandler.isOpened():
        videoInfo['width'] = int(videoHandler.get(cv2.CAP_PROP_FRAME_WIDTH))
        videoInfo['height'] = int(videoHandler.get(cv2.CAP_PROP_FRAME_HEIGHT))
        videoInfo['frame_rate'] = int(videoHandler.get(cv2.CAP_PROP_FPS))
        videoInfo['frame_count'] = int(videoHandler.get(cv2.CAP_PROP_FRAME_COUNT))
        while True:
            ret, frame = videoHandler.read()
            if ret is False:
                break
            else:
                videoInfo['frames'].append(frame)

        videoHandler.release()
        return videoInfo

def createCaption(args):
    print(args)
    videoInfo = getVideoInfo(args.video)
    videoHandler = cv2.VideoWriter(os.path.join("out.avi"),
                                       cv2.VideoWriter_fourcc(*'XVID'),
                                       videoInfo['frame_rate'],
                                       (videoInfo['width'],
                                        videoInfo['height']))
    timeDelta = datetime.strptime(args.end_time, '%H:%M:%S') - datetime.strptime(args.start_time, '%H:%M:%S')
    startFrame = int(datetime.strptime(args.start_time, '%H:%M:%S').hour * 3600) + \
                 int(datetime.strptime(args.start_time, '%H:%M:%S').minute * 60) + \
                 int(datetime.strptime(args.start_time, '%H:%M:%S').second)
    baseFrame = int(videoInfo['frame_rate'] * startFrame)
    endFrame = int(videoInfo['frame_rate'] * timeDelta.seconds) + baseFrame
    textProperties = {
        'font_family': args.font_family,
        'font_size': args.font_size
    }
    if args.pause_video:
        afterArray = videoInfo['frames'][baseFrame:]
        for i in range(0, endFrame):
            if i >= baseFrame:
                if args.hsv_inverse:
                    videoHandler.write(
                        caption.testHSV(
                            videoInfo['frames'][baseFrame],
                            args.text_caption,
                            args.x_coordinate,
                            args.y_coordinate,
                            textProperties
                        ))
                else:
                    videoHandler.write(
                        caption.testContrast(
                            videoInfo['frames'][baseFrame],
                            args.text_caption,
                            args.x_coordinate,
                            args.y_coordinate,
                            args.contrast_level,
                            textProperties
                        ))

            else:
                videoHandler.write(videoInfo['frames'][i])
        for i in range(len(afterArray)):
            videoHandler.write(videoInfo['frames'][baseFrame+i])
    else:
        for i in range(len(videoInfo['frames'])):
            if i >= baseFrame and i <= endFrame:
                if args.hsv_inverse:
                    videoHandler.write(
                        caption.testHSV(
                            videoInfo['frames'][i],
                            args.text_caption,
                            args.x_coordinate,
                            args.y_coordinate,
                            textProperties
                        ))
                else:
                    videoHandler.write(
                        caption.testContrast(
                            videoInfo['frames'][i],
                            args.text_caption,
                            args.x_coordinate,
                            args.y_coordinate,
                            args.contrast_level,
                            textProperties
                        ))
            else:
                videoHandler.write(videoInfo['frames'][i])
    videoHandler.release()