# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re

def showData(fileName):
    fd = open(fileName, 'rb')

    hdrFileName = fileName[:-4]+".hdr"
    w,x,y,z,dt = readInfo(hdrFileName)

    if(dt == 2):
        f = np.fromfile(fd, dtype=np.int16, count=x * y * z)
        '''按照BIL格式文件来reshape'''
        im = f.reshape((x, z, y))
        temp = np.max(im)-np.min(im)
        fd.close()
        gray = np.uint8(im[:, 197, :]*255/temp)

    if(dt == 4):
        f = np.fromfile(fd, dtype=np.float32, count=x * y * z)
        '''按照BIL格式文件来reshape'''
        im = f.reshape((x, z, y))
        fd.close()
        gray = np.uint8(im[:, 197, :] * 255)

    circle = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1,
                              30, param1=100, param2=25, minRadius=10, maxRadius=70)

    circles = circle[0, :, :];
    circles = np.uint16(np.around(circles))

    return im

def readInfo(fileName):

    hdrFile = open(fileName)
    text = hdrFile.read()

    '''读取波段'''
    wave = re.search("wavelength *= *\{.*\}",text,re.S).group()
    waveList = re.findall("[0-9]*\.[0-9]*",wave)

    '''读取维度'''
    x = re.search("lines *= *([0-9]*)",text ).group(1)
    y = re.search("samples *= *([0-9]*)",text).group(1)
    z = re.search("bands *= *([0-9]*)",text).group(1)
    '''data type'''
    dataType = re.search("data type *= *([0-9]*)",text).group(1)

    hdrFile.close()

    return waveList , int(x) , int(y) , int(z),int(dataType)

