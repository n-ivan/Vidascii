'''
    vidascii.py
    born 2020-03-18
    n-ivan
    v2
    converts an video into ascii art
'''


import cv2
from PIL import Image
import numpy as np
import os
from imgify import make_ascii_png
import argparse
import moviepy.editor

def getAverageL(image):
    """
    Given PIL Image, return average value of greyscale value
    """
    im = np.array(image)
    w,h = im.shape
    return np.average(im.reshape(w*h))

def convertImageToAscii(image, cols):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images 
    """

    # grey scale level values from: 
    # http://paulbourke.net/dataformats/asciiart/

    gscale = '@%#*+=-:. '

    W, H = image.size[0],image.size[1]
    print("input image dims: %d x %d" % (W, H))
    w = W/cols
    h = w/0.43
    rows = int(H/h)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))
    
    if cols>W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    aimg = []

    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)
        # correct last tile
        if j == rows-1:
            y2 = H
        # append an empty string
        aimg.append("")
        for i in range(cols):
            # crop image to tile
            x1 = int(i*w)
            x2 = ((i+1)*w)
            # correct last tile
            if i == cols-1:
                x2 = W
            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance of cropped tile (it should be an integer)
            avg = getAverageL(img)
            # look up ascii char by generating a string index based on avg
            gsval = gscale[int((avg*9)/255)]
            # append ascii char to string
            aimg[j] += gsval

    txt = ""
    for row in aimg:
        txt += row+'\n'
    return txt

def getFrame(vidcap, sec, count, cols):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames, image = vidcap.read()
    if hasFrames:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image).convert('L')
        make_ascii_png(convertImageToAscii(img, cols), f"frames/f{count}")
    return hasFrames

def vidToAsciiFrames(vidName, frameRate, cols):
    sec = 0
    count=1
    if (os.path.exists('frames') == False):
        os.mkdir('frames')
    frameRate = (1 / frameRate)
    vidcap = cv2.VideoCapture(vidName)
    success = getFrame(vidcap, sec, count, cols)
    while success:
        count += 1
        sec += frameRate
        sec = round(sec, 2)
        success = getFrame(vidcap, sec, count, cols)
    return count

def vidascii(vidName, frameRate, cols):
    count = vidToAsciiFrames(vidName, frameRate, cols)
    frames = []
    outVidName = vidName.split(".")[0]+"ascii.mp4"
    audio = moviepy.editor.VideoFileClip(vidName).audio
    imglst = [f"frames/f{i}.png" for i in range(1, count)]
    vid = moviepy.editor.ImageSequenceClip(imglst, fps=frameRate)
    vidAUD = vid.set_audio(audio.set_duration(vid.duration))
    vidAUD.write_videofile(outVidName, audio_codec='aac')
    for i in range(1, count):
        os.remove(f"frames/f{i}.png")
    os.rmdir('frames')

def main():
    descStr = "This program converts a video into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    parser.add_argument('--file', dest='vidFile', required=True)
    parser.add_argument('--cols', dest='cols', required=True)
    parser.add_argument('--fps', dest='frameRate', required=True)

    args = parser.parse_args()

    vidFile = args.vidFile
    cols = int(args.cols)
    frameRate = int(args.frameRate)
    print("starting conversion")
    vidascii(vidFile, frameRate, cols)

if __name__ == '__main__':
    main()
