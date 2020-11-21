import os
import cv2

def getVideoInfo(video):
    videoInfo = {
        'width': None,
        'height': None,
        'frame_rate': None,
        'frame_count': None,
        'frames': []
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

def createVideo(videoPath, videoInfo):
    videoHandler = cv2.VideoWriter(os.path.join(videoPath),
                                   cv2.VideoWriter_fourcc(*'XVID'),
                                   videoInfo['frame_rate'],
                                   (videoInfo['width'],
                                    videoInfo['height']))
    for frame in videoInfo['frames']:
        videoHandler.write(frame)
    videoHandler.release()


videoInfo = getVideoInfo('01_01.mpg')
# print(videoInfo, len(videoInfo['frames']))
createVideo("output.avi", videoInfo)