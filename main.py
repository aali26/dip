
import argparse
import video

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

if __name__ == '__main__':
    parserHandler = argparse.ArgumentParser(description='Adding Caption to videos')
    parserHandler.add_argument('-t',
                               '--text_caption',
                               type=str,
                               help="The text to be inserted")
    parserHandler.add_argument('-hsv',
                               '--hsv_inverse',
                               type=str2bool,
                               default=True,
                               help="The inverse of HSV Color fast in some situations")
    parserHandler.add_argument('-c',
                               '--contrast_method',
                               type=str2bool,
                               default=False,
                               help="Calculated contrast slower but more robust")
    parserHandler.add_argument('-cl',
                               '--contrast_level',
                               type=float,
                               default=7.5,
                               help="The level of contrast between 1 to 21")
    parserHandler.add_argument('-v',
                               '--video',
                               type=str,
                               help="The input video file")
    parserHandler.add_argument('-x',
                               '--x_coordinate',
                               default=0,
                               type=int,
                               help="X Coordinate value")
    parserHandler.add_argument('-y',
                               '--y_coordinate',
                               default=0,
                               type=int,
                               help="Y coordinate value")
    parserHandler.add_argument('-fs',
                               '--font_size',
                               default=2,
                               type=int,
                               help="You may use 1 for small, 2 for medium, or 3 for large")
    parserHandler.add_argument('-ff',
                               '--font_family',
                               default=0,
                               type=int,
                               help="You may use the number from 0 to 7 for the supported fonts")
    parserHandler.add_argument('-p',
                               '--pause_video',
                               default=False,
                               type=str2bool,
                               help="you may pass True to pause the video or False for having the text in all frames")
    parserHandler.add_argument('-st',
                               '--start_time',
                               type=str,
                               help="the starting time must be in the format of hh:mm:ss")
    parserHandler.add_argument('-et',
                               '--end_time',
                               type=str,
                               help="the ending time must be in the format of hh:mm:ss")
    args = parserHandler.parse_args()
    if args.video is not None \
            and args.start_time is not None \
            and args.end_time is not None \
            and args.text_caption is not None:
        video.createCaption(args)
        # videoInfo = video.getVideoInfo(args.video,
        #                                args.start_time,
        #                                args.end_time,
        #                                args.pause_video,
        #                                args.text_caption)
        # videoInfo = video.generateFrames(videoInfo, args.start_time, args.end_time, args.pause_video)
        # video.createVideo('out.avi', videoInfo)
    else:
        print("one of the main parameters have not been set please use --help")