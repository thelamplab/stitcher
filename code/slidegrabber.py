import numpy as np
import cv2
import time
from PIL import Image
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
import sys
import os


## TO DO: build threshold in to metadata, also skiprate

writeMethod = 'pic'  # 'arr' or 'pic'
pixThresh = 0.95  # threshold for average pixel 'movement'
skipRate = 100 # how many frames to skip
scaleFactor = 0.5  # factor by which to reduce image size, eventually aim to make it a static width


def strip_bands(arr):
    lspan = True
    rspan = True
    maxx = arr.shape[1]
    for i in range(1,200):
        if lspan:
            left = arr[:,:i]
            lavg = np.mean(left)
            if lavg > 0.1:
                start = i
                lspan = False
        if rspan and i > 1:
            right = arr[:,-i:-1]
            ravg = np.mean(right)
            if ravg > 0.1:
                stop = arr.shape[1] - i
                rspan = False   
    return start, stop
    

def get_sound(duration, samp):
    start = time.time()
    myrecording = sd.rec(int(duration * samp), channels=2)
    sd.wait()
    return myrecording
        
    
def get_meta(vidfile):
    instructor = vidfile.split('_')[0]
    course = vidfile.split('_')[1]
    print(instructor, course)
    frame_stem = vidfile.split('_')[2]
    finish_time = vidfile.split('_')[3]
    duration = vidfile.split('_')[4].split('.avi')[0]
    vidcap = cv2.VideoCapture(vidfile)
    success,_ = vidcap.read()
    totalFrames = 0
    while success:
        totalFrames+=1
        success,_ = vidcap.read()
    fps = int(totalFrames)/int(duration)
    return duration, fps, finish_time, totalFrames
        
    
        
def frame_grabs(vidfile, thresh, scale, saveas, folderloc):
    print('started')
    changes = []
    instructor = vidfile.split('_')[0]
    course = vidfile.split('_')[1]
    frame_stem = vidfile.split('_')[2]
    finish_time = vidfile.split('_')[3]
    duration = vidfile.split('_')[4].split('.avi')[0]
    vidcap = cv2.VideoCapture(vidfile)
    success,arr = vidcap.read()
    lastarr = np.copy(arr)
    count = 0
    i = 0
    success = True
    while success:
        success,arr = vidcap.read()
        try:
            if i != 0 and i % 100 == 0:
                thisChange = np.corrcoef(np.vstack((arr.flat, lastarr.flat)))[0,1]
                changes.append(1-thisChange)
                if thisChange < thresh:
                    count += 1
                    print('found change on frame {}, change # {}, dissimilarity: {}'.format(i, count, np.around(1-thisChange,2)))
                    if saveas == 'pic':
                        p0, p1 = strip_bands(arr)
                        _image = cv2.cvtColor(arr[:, p0:p1], cv2.COLOR_BGR2RGB)
                        image = Image.fromarray(_image, 'RGB')
                        size = tuple(np.multiply(image.size, scale))
                        image.thumbnail(size, Image.ANTIALIAS)
                        image.save('{}/{}_{}_{}.gif'.format(folderloc, frame_stem, count, i), optimize=True, quality=95)
                    elif saveas == 'arr':
                        np.save('{}/{}_{}_{}.npy'.format(folderloc, frame_stem, count, i), arr)
                    else:
                        pass
                lastarr = np.copy(arr)
            i += 1
        except:
            pass
    fps = int(i)/int(duration)
    return np.array(changes), duration, fps, finish_time, i, frame_stem

classvid = sys.argv[1]
vid = './{}'.format(classvid)
course = classvid.split('_')[1]
theDate = classvid.split('_')[2]
outFolder = './output/{}'.format(course)
if not os.path.isdir(outFolder):
    os.mkdir(outFolder)
changes, dur, fps, fin, frames, frame_stem = frame_grabs(vid, pixThresh, scaleFactor, writeMethod, outFolder)

np.save('{}/{}_pixelchange.npy'.format(outFolder, frame_stem), np.array(changes))
with open('{}/{}_meta.txt'.format(outFolder, frame_stem), 'w') as metafile:
    metafile.write('{} {} {} {}'.format(dur, fps, fin, frames))
                      


