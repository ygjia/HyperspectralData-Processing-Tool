from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtGui import QImage,QCursor,QIcon,QPixmap
import os,xlwt
from src.ShowData import *

ROIByManualLeftUp = []
ROIByManualRightDown = []

class Tab2(object):
    def __init__(self, MainWindow):
        self.window = MainWindow

    def OnCilickedTab2Butto1(self):
        self.window.dirPath = QFileDialog.getExistingDirectory()
        if(self.window.dirPath):
            rawFiles = [i for i in os.listdir(self.window.dirPath) if os.path.splitext(i)[1] == ".raw"]
            bilFiles = [i for i in os.listdir(self.window.dirPath) if os.path.splitext(i)[1] == ".bil"]

            if(rawFiles):
                self.window.listWidget.addItems(rawFiles)

            if (bilFiles):
                pass

    def OnChangedTab2listWidget(self):
        fileName = self.window.listWidget.currentItem().text()
        fileUrl = self.window.dirPath+"/"+fileName
        hdrFileName = fileUrl[:-4]+".hdr"
        self.window.w, self.window.l, self.window.s, self.window.b,self.window.dt = readInfo(hdrFileName)
        self.window.image = showData(fileUrl)
        if fileUrl:
            scene = self.ConventToQImageWithHough(197)
            self.window.graphicsView_2.setScene(scene)
        self.window.comboBox_2.clear()
        self.window.comboBox_2.addItems(self.window.w)

    def OnChangedTab2ComboBox1(self):
        band = self.window.comboBox_2.currentIndex()
        scene = self.ConventToQImageWithHough(band)
        self.window.graphicsView_2.setScene(scene)

    def OnCilickedTab2Butto2(self):
        print(ROIByManualLeftUp)
        print(ROIByManualRightDown)

    def OnCilickedTab2Butto3(self):
        if(not hasattr(self.window,'w')):
            return

        band = self.window.w.index(self.window.comboBox_2.currentText())

        temp = np.max(self.window.image) - np.min(self.window.image)
        img2D = np.uint8((self.window.image[:, band, :] / temp) * 255)

        if (self.window.lineEdit_2.text().__len__() is 0):
            maxR = 70
        else:
            maxR = int(self.window.lineEdit_2.text())

        if (self.window.lineEdit.text().__len__() is 0):
            minR = 10
        else:
            minR = int(self.window.lineEdit.text())

        if (self.window.comboBox_3.currentText() == "矩形"):
            circle = cv2.HoughCircles(img2D, cv2.HOUGH_GRADIENT, 1,
                                      30, param1=100, param2=25, minRadius=minR, maxRadius=maxR)
            if (not circle is None):
                circles = circle[0, :, :];
                circles = np.uint16(np.around(circles))
                excelFile = xlwt.Workbook(encoding='utf-8')
                booksheet = excelFile.add_sheet('Spectrum', cell_overwrite_ok=True)
                for a,b in enumerate(circles[:]):
                    data = self.window.image[b[1]-b[2]:b[1]+b[2],:,b[0]-b[2]:b[0]+b[2]]
                    data = np.average(data,axis=0)
                    data = np.average(data,axis=1)
                    for k, j in enumerate(data):
                        booksheet.write(k,a,str(j))
                fileName = self.window.listWidget.currentItem().text()
                fileName = 'Rectangle_' + fileName + '.xls'
                excelFile.save(fileName)
        else:
            circle = cv2.HoughCircles(img2D, cv2.HOUGH_GRADIENT, 1,
                                      30, param1=100, param2=25, minRadius=minR, maxRadius=maxR)
            if (not circle is None):
                circles = circle[0, :, :];
                circles = np.uint16(np.around(circles))
                excelFile = xlwt.Workbook(encoding='utf-8')
                booksheet = excelFile.add_sheet('Spectrum', cell_overwrite_ok=True)
                for a, b in enumerate(circles[:]):
                    data = self.window.image[b[1],:,b[0]]
                    for i in np.arange(-1*b[2],b[2],1):
                        for j in np.arange(-1*b[2],b[2],1):
                            if(i**2 + j**2 < b[2]**2 and i**2 + j**2 != 0):
                                data = np.c_[data,self.window.image[b[1]+i,:,b[0]+j]]
                    data = np.average(data, axis=1)
                    for k, j in enumerate(data):
                        booksheet.write(k, a, str(j))
                fileName = self.window.listWidget.currentItem().text()
                fileName = 'Circle_'+fileName + '.xls'
                excelFile.save(fileName)

    def OnCilickedTab2Butto4(self):
        if (not hasattr(self.window, 'w')):
            return

        band = self.window.w.index(self.window.comboBox_2.currentText())
        temp = np.max(self.window.image) - np.min(self.window.image)
        img2D = np.uint8((self.window.image[:, band, :] / temp) * 255)

        if (self.window.comboBox_3.currentText() == "矩形"):
                excelFile = xlwt.Workbook(encoding='utf-8')
                booksheet = excelFile.add_sheet('Spectrum', cell_overwrite_ok=True)
                Len = len(ROIByManualLeftUp)
                for i in np.arange(0,Len,1):
                    sx = int(ROIByManualLeftUp[i].x())
                    sy = int(ROIByManualLeftUp[i].y())
                    ex = int(ROIByManualRightDown[i].x())
                    ey = int(ROIByManualRightDown[i].y())

                    data = self.window.image[sy:ey,:,sx:ex]
                    data = np.average(data, axis=0)
                    data = np.average(data, axis=1)
                    plt.plot(data)

                    for k, j in enumerate(data):
                        booksheet.write(k, i, str(j))
                fileName = self.window.listWidget.currentItem().text()
                fileName = 'Rectangle_' + fileName + '.xls'
                excelFile.save(fileName)
                plt.show()
        else:

                excelFile = xlwt.Workbook(encoding='utf-8')
                booksheet = excelFile.add_sheet('Spectrum', cell_overwrite_ok=True)
                Len = len(ROIByManualLeftUp)
                for i in np.arange(0, Len, 1):
                    sx = int(ROIByManualLeftUp[i].x())
                    sy = int(ROIByManualLeftUp[i].y())
                    ex = int(ROIByManualRightDown[i].x())
                    ey = int(ROIByManualRightDown[i].y())
                    m=min(ex-sx,ey-sy)
                    cx = int((sx+ex)/2)
                    cy = int((sy+ey)/2)
                    data = self.window.image[cy, :,cx]
                    for i in np.arange(-1 * m, m, 1):
                        for j in np.arange(-1 * m, m, 1):
                            if (i ** 2 + j ** 2 < m ** 2 and i ** 2 + j ** 2 != 0):
                                data = np.c_[data, self.window.image[cy + i, :, cx + j]]
                    data = np.average(data, axis=1)
                    plt.plot(data)
                    for k, j in enumerate(data):
                        booksheet.write(k, i, str(j))

                fileName = self.window.listWidget.currentItem().text()
                fileName = 'Circle_' + fileName + '.xls'
                excelFile.save(fileName)

                plt.show()
        ROIByManualLeftUp.clear()
        ROIByManualRightDown.clear()

    def ConventToQImage(self, band):
        temp = np.max(self.window.image) - np.min(self.window.image)
        img2D = np.uint8((self.window.image[:,band,:]/temp)*255)
        height, width = img2D.shape
        bytesPerComponent = 1
        bytesPerLine = bytesPerComponent * width
        Qimg = QImage(img2D, width, height, bytesPerLine, QImage.Format_Grayscale8)

        scene = self.window.MyGraphicsScene()
        scene.addPixmap(QPixmap(Qimg))

        return scene

    def ConventToQImageWithHough(self, band):
        temp = np.max(self.window.image) - np.min(self.window.image)
        img2D = np.uint8((self.window.image[:, band, :] / temp) * 255)

        if (self.window.lineEdit_2.text().__len__() is 0):
            maxR = 70
        else:
            maxR = int(self.window.lineEdit_2.text())

        if (self.window.lineEdit.text().__len__() is 0):
            minR = 10
        else:
            minR = int(self.window.lineEdit.text())

        if (self.window.comboBox_3.currentText() == "圆形"):
            circle = cv2.HoughCircles(img2D, cv2.HOUGH_GRADIENT, 1,
                                      30, param1=100, param2=25, minRadius=minR, maxRadius=maxR)
            if (not circle is None):
                circles = circle[0, :, :];
                circles = np.uint16(np.around(circles))
                for i in circles[:]:
                    cv2.circle(img2D, (i[0], i[1]), i[2], (255, 0, 0), 2)
                    cv2.circle(img2D, (i[0], i[1]), 2, (255, 0, 0), 4)
        else:
            circle = cv2.HoughCircles(img2D, cv2.HOUGH_GRADIENT, 1,
                                      30, param1=100, param2=25, minRadius=minR, maxRadius=maxR)
            if (not circle is None):
                circles = circle[0, :, :];
                circles = np.uint16(np.around(circles))
                for i in circles[:]:
                    cv2.rectangle(img2D, (i[0] - i[2], i[1] - i[2]), (i[0] + i[2], i[1] + i[2]), (255, 0, 0), 2)

        height, width = img2D.shape
        bytesPerComponent = 1
        bytesPerLine = bytesPerComponent * width
        Qimg = QImage(img2D, width, height, bytesPerLine, QImage.Format_Grayscale8)

        self.window.scene.addPixmap(QPixmap(Qimg))
        return self.window.scene