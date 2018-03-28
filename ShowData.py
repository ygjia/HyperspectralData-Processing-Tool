# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re

def showData(fileName):
    fd = open(fileName, 'rb')

    hdrFileName = fileName[:-4]+".hdr"
    print(hdrFileName)
    w,x,y,z,dt = readInfo(hdrFileName)
    # '''图片的维数'''
    # x = 250
    # y = 320
    # z = 256

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

    # plt.figure("Hough变换识别ROI区域")
    # for i in circles[:]:
    #     cv2.circle(gray, (i[0], i[1]), i[2], (255, 0, 0), 2)
    #     cv2.circle(gray, (i[0], i[1]), 2, (255, 0, 0), 4)
    #
    # plt.xticks([])
    # plt.yticks([])
    # plt.savefig('file.png', bbox_inches='tight', pad_inches=0)
    #
    # spectrum = [im[circles[i][1], :, circles[i][0]] for i in np.arange(circles.shape[0])]
    #
    # plt.figure("圆心处对应的光谱曲线")
    # for i in np.arange(circles.shape[0]):
    #     plt.subplot(2, 3, i + 1);
    #     plt.title(circles[i])
    #     plt.plot(spectrum[i])

#    plt.show()

    return im

def readInfo(fileName):
    #fileName = 'Data/HSI23_refl0.raw.hdr'
    #flleName1 = 'Data/FLFemale_01.bil.hdr'

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

# a,b,c,d = readInfo('Data/HSI23_refl0.raw.hdr')
