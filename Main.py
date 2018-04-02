from MainWindow import *
from ShowData import *
import scipy.io as sio
import Classifier

import sys
import os,re
import pandas as pd

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import xlwt
import matplotlib.pyplot as plt
import numpy as np


def showSpectrumInCurrentFigure():

    p1 = QCursor.pos()
    p2 = Window.lab.mapToGlobal(Window.lab.pos())
    p = p1 - p2

    gw = Window.graphicsView.width()
    gh = Window.graphicsView.height()
    sw = Window.graphicsView.scene().width()
    sh = Window.graphicsView.scene().height()

    _w = (gw-sw)/2
    _h = (gh-sh)/2

    if(p.x()- _w > 0 and p.x() - _w < sw and p.y()-_h> 0 and p.y()- _h<sh):
        x = int(p.x() - _w)
        y = int(p.y() - _h)

        a = float(Window.w[0])
        b = float(Window.w[-1])
        c = int(Window.b)

        Window.waveData.append(Window.image[y, :, x])

        plt.close()
        plt.figure("Spectral curve")
        for i,j in enumerate(Window.waveData):
            plt.plot(np.linspace(a,b,c),j)
        plt.xticks(np.linspace(a,b,c/20))
        plt.axvline(float(Window.w[Window.comboBox.currentIndex()]))
        plt.plot(Window.w[Window.comboBox.currentIndex()],
                 Window.image[y, :, x][Window.comboBox.currentIndex()],'o')
        #plt.legend(["Spectral curve","Current spectral band"])
        plt.show()

    else:
        msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
        msg_box.exec_()

def showSpectrum():
    p1 = QCursor.pos()
    p2 = Window.lab.mapToGlobal(Window.lab.pos())
    p = p1 - p2

    gw = Window.graphicsView.width()
    gh = Window.graphicsView.height()
    sw = Window.graphicsView.scene().width()
    sh = Window.graphicsView.scene().height()

    _w = (gw - sw) / 2
    _h = (gh - sh) / 2

    if (p.x() - _w > 0 and p.x() - _w < sw and p.y() - _h > 0 and p.y() - _h < sh):
        x = int(p.x() - _w)
        y = int(p.y() - _h)

        a = float(Window.w[0])
        b = float(Window.w[-1])
        c = int(Window.b)
        Window.waveData.clear()
        Window.waveData.append(Window.image[y, :, x])

        plt.close()
        plt.figure("Spectral curve")
        for i, j in enumerate(Window.waveData):
            plt.plot(np.linspace(a, b, c), j)
        plt.xticks(np.linspace(a, b, c / 20))
        plt.axvline(float(Window.w[Window.comboBox.currentIndex()]))
        plt.plot(Window.w[Window.comboBox.currentIndex()],
                 Window.image[y, :, x][Window.comboBox.currentIndex()], 'o')
        # plt.legend(["Spectral curve","Current spectral band"])
        plt.show()

    else:
        msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
        msg_box.exec_()

def saveImage():
    savePath = QFileDialog.getSaveFileName()
    band = Window.comboBox.currentIndex()
    img2D = np.uint8(Window.image[:,band,:] * 255)
    height, width = img2D.shape
    bytesPerComponent = 1
    bytesPerLine = bytesPerComponent * width
    Qimg = QImage(img2D, width, height, bytesPerLine, QImage.Format_Grayscale8)
    Qimg.save(savePath[0])

def saveSpectrumToCSV():
    p1 = QCursor.pos()
    p2 = Window.lab.mapToGlobal(Window.lab.pos())
    p = p1 - p2

    gw = Window.graphicsView.width()
    gh = Window.graphicsView.height()
    sw = Window.graphicsView.scene().width()
    sh = Window.graphicsView.scene().height()

    _w = (gw - sw) / 2
    _h = (gh - sh) / 2

    if (p.x() - _w > 0 and p.x() - _w < sw and p.y() - _h > 0 and p.y() - _h < sh):
        x = int(p.x() - _w)
        y = int(p.y() - _h)
        a = float(Window.w[0])
        b = float(Window.w[-1])
        c = int(Window.b)
        wave = Window.w
        data = Window.image[y, :, x]

        dataFrame = pd.DataFrame({'Wave':wave ,'Data':data})
        fileName = Window.label.text()
        fileName = fileName[5:] + '.csv'
        dataFrame.to_csv(fileName, index=False ,sep=',')

    else:
        msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
        msg_box.exec_()

def saveSpectrumToExcel():
    p1 = QCursor.pos()
    p2 = Window.lab.mapToGlobal(Window.lab.pos())
    p = p1 - p2

    gw = Window.graphicsView.width()
    gh = Window.graphicsView.height()
    sw = Window.graphicsView.scene().width()
    sh = Window.graphicsView.scene().height()

    _w = (gw - sw) / 2
    _h = (gh - sh) / 2

    if (p.x() - _w > 0 and p.x() - _w < sw and p.y() - _h > 0 and p.y() - _h < sh):
        x = int(p.x() - _w)
        y = int(p.y() - _h)
        a = float(Window.w[0])
        b = float(Window.w[-1])
        c = int(Window.b)
        wave = Window.w
        data = Window.image[y, :, x]

        excelFile = xlwt.Workbook(encoding='utf-8')
        booksheet = excelFile.add_sheet('Spectrum', cell_overwrite_ok=True)

        booksheet.write(0, 0, "Wave")
        for i, j in enumerate(wave):
            booksheet.write(i + 1, 0, str(j))

        booksheet.write(0, 1, 'Data')
        for l, m in enumerate(data):
            booksheet.write(l + 1, 1, str(m))
        fileName = Window.label.text()
        fileName = fileName[5:] + '.xls'
        excelFile.save(fileName)

    else:
        msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
        msg_box.exec_()

class MenuLabel(QLabel):
    def __init__(self, parent=None):
        super(MenuLabel, self).__init__(parent)
        self.createContextMenu()

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        self.contextMenu = QMenu(self)


        self.action = self.contextMenu.addAction(QIcon('img/line.png'),u'显示光谱曲线')
        self.action.triggered.connect(showSpectrum)
        self.action1 = self.contextMenu.addAction(QIcon('img/line.png'), u'在现有图中显示光谱曲线')
        self.action1.triggered.connect(showSpectrumInCurrentFigure)
        self.action2 = self.contextMenu.addAction(QIcon('img/save.png'), u'保存图片')
        self.action2.triggered.connect(saveImage)
        self.action3 = self.contextMenu.addAction(QIcon('img/excel.png'), u'保存该点光谱至Excel')
        self.action3.triggered.connect(saveSpectrumToExcel)
        self.action4 = self.contextMenu.addAction(QIcon('img/CSV.png'), u'保存该点光谱至CSV')
        self.action4.triggered.connect(saveSpectrumToCSV)

    def showContextMenu(self):
        self.contextMenu.exec_(QCursor.pos())


class MyWindow(QMainWindow,Ui_Hyperspectral):
    def __init__(self,parent = None):
        super(MyWindow,self).__init__(parent)

        self.setupUi(self)
        ''' Tab2 Init '''
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.lineEdit_4.clear()
        self.lineEdit_5.clear()
        self.lineEdit_6.clear()
        list = ['1','2','3','4','5','6','7','8','9','10']
        self.comboBox_6.addItems(list)
        self.comboBox_5.addItems(list)
        self.comboBox_4.addItems(list)

        self.comboBox_3.addItems(["圆形"])
        self.comboBox_3.addItems(["矩形"])
        self.statusbar.showMessage("西北农林科技大学   Powerby PyQt")

    def ConventToQImage(self, band):
        temp = np.max(self.image) - np.min(self.image)
        img2D = np.uint8((self.image[:,band,:]/temp)*255)
        height, width = img2D.shape
        bytesPerComponent = 1
        bytesPerLine = bytesPerComponent * width
        Qimg = QImage(img2D, width, height, bytesPerLine, QImage.Format_Grayscale8)

        scene = QGraphicsScene()
        scene.addPixmap(QPixmap(Qimg))

        return scene

    def ConventToQImageWithHough(self, band):
        temp = np.max(self.image) - np.min(self.image)
        img2D = np.uint8((self.image[:,band,:]/temp)*255)

        if(self.lineEdit_2.text().__len__() is 0):
            maxR = 70
        else:
            maxR = int(self.lineEdit_2.text())

        if (self.lineEdit.text().__len__() is 0):
            minR = 10
        else:
            minR = int(self.lineEdit.text())

        if(self.comboBox_3.currentText() == "圆形"):
            circle = cv2.HoughCircles(img2D, cv2.HOUGH_GRADIENT, 1,
                                      30, param1=100, param2=25, minRadius=minR, maxRadius=maxR)
            if(not circle is None):
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
                    cv2.rectangle(img2D,(i[0]-i[2],i[1]-i[2]),(i[0]+i[2],i[1]+i[2]),(255,0,0),2)

        height, width = img2D.shape
        bytesPerComponent = 1
        bytesPerLine = bytesPerComponent * width
        Qimg = QImage(img2D, width, height, bytesPerLine, QImage.Format_Grayscale8)

        scene = QGraphicsScene()
        scene.addPixmap(QPixmap(Qimg))

        return scene

    def ShowBond(self):
        band = self.comboBox.currentIndex()
        scene = self.ConventToQImage(band)
        self.graphicsView.setScene(scene)
        self.lcdNumber.display(self.w[band])

    def OnClickedTab1Button(self):
        filePath = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())

        if(not filePath[0]):
            return

        filename = re.search("\/+([^\/]*$)", filePath[0]).group(1)
        self.waveData = []
        self.w,self.l,self.s,self.b,self.dt= readInfo(filePath[0]+".hdr")
        self.image = showData(filePath[0])

        if filePath:
            scene = self.ConventToQImage(197)
            self.graphicsView.setScene(scene)

        self.comboBox.addItems(self.w)
        self.label.setText("文件名称: "+filename)
        self.label_2.setText("Lines: " + str(self.l))
        self.label_3.setText("Samples:  " + str(self.s))
        self.label_4.setText("Bands: " + str(self.b))
        self.label_6.setText("波段范围: " + self.w[0]+"~"+self.w[-1])
        self.lcdNumber.setDigitCount(8)
        self.lcdNumber.display(self.w[197])

        self.lab = MenuLabel()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
        vbox.addWidget(self.lab)

        self.graphicsView.setLayout(vbox)

    def OnCilickedTab2Butto1(self):
        self.dirPath = QFileDialog.getExistingDirectory()
        if(self.dirPath):
            rawFiles = [i for i in os.listdir(self.dirPath) if os.path.splitext(i)[1] == ".raw"]
            bilFiles = [i for i in os.listdir(self.dirPath) if os.path.splitext(i)[1] == ".bil"]

            if(rawFiles):
                self.listWidget.addItems(rawFiles)

            if (bilFiles):
                pass

    def OnChangedTab2listWidget(self):
        fileName = self.listWidget.currentItem().text()
        fileUrl = self.dirPath+"/"+fileName
        hdrFileName = fileUrl[:-4]+".hdr"
        self.w, self.l, self.s, self.b,self.dt = readInfo(hdrFileName)
        self.image = showData(fileUrl)
        if fileUrl:
            scene = self.ConventToQImageWithHough(197)
            self.graphicsView_2.setScene(scene)
        self.comboBox_2.clear()
        self.comboBox_2.addItems(self.w)

    def OnChangedTab2ComboBox1(self):
        band = self.comboBox_2.currentIndex()
        scene = self.ConventToQImageWithHough(band)
        self.graphicsView_2.setScene(scene)


    def OnCilickedTab2Butto2(self):
        pass


    def OnCilickedTab2Butto3(self):
        if(not hasattr(self,'w')):
            return

        band = self.w.index(self.comboBox_2.currentText())

        temp = np.max(self.image) - np.min(self.image)
        img2D = np.uint8((self.image[:, band, :] / temp) * 255)

        if (self.lineEdit_2.text().__len__() is 0):
            maxR = 70
        else:
            maxR = int(self.lineEdit_2.text())

        if (self.lineEdit.text().__len__() is 0):
            minR = 10
        else:
            minR = int(self.lineEdit.text())

        if (self.comboBox_3.currentText() == "矩形"):
            circle = cv2.HoughCircles(img2D, cv2.HOUGH_GRADIENT, 1,
                                      30, param1=100, param2=25, minRadius=minR, maxRadius=maxR)
            if (not circle is None):
                circles = circle[0, :, :];
                circles = np.uint16(np.around(circles))
                excelFile = xlwt.Workbook(encoding='utf-8')
                booksheet = excelFile.add_sheet('Spectrum', cell_overwrite_ok=True)
                for a,b in enumerate(circles[:]):
                    data = self.image[b[1]-b[2]:b[1]+b[2],:,b[0]-b[2]:b[0]+b[2]]
                    data = np.average(data,axis=0)
                    data = np.average(data,axis=1)
                    for k, j in enumerate(data):
                        booksheet.write(k,a,str(j))
                fileName = self.listWidget.currentItem().text()
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
                    data = self.image[b[1],:,b[0]]
                    for i in np.arange(-1*b[2],b[2],1):
                        for j in np.arange(-1*b[2],b[2],1):
                            if(i**2 + j**2 < b[2]**2 and i**2 + j**2 != 0):
                                data = np.c_[data,self.image[b[1]+i,:,b[0]+j]]
                    data = np.average(data, axis=1)
                    for k, j in enumerate(data):
                        booksheet.write(k, a, str(j))
                fileName = self.listWidget.currentItem().text()
                fileName = 'Circle_'+fileName + '.xls'
                excelFile.save(fileName)


    def OnCilickedTab2Butto4(self):
        pass

    def ReadDirTab4(self):
        self.Tab4DirPath = QFileDialog.getExistingDirectory()
        if(not self.Tab4DirPath):
            return
        matFiles = [i for i in os.listdir(self.Tab4DirPath) if os.path.splitext(i)[1] == ".mat"]
        csvFiles = [i for i in os.listdir(self.Tab4DirPath) if os.path.splitext(i)[1] == ".csv"]
        xlsFiles = [i for i in os.listdir(self.Tab4DirPath) if os.path.splitext(i)[1] == ".xls"]

        if (matFiles):
            self.listWidget_2.addItems(matFiles)

        if (csvFiles):
            self.listWidget_2.addItems(csvFiles)

        if (xlsFiles):
            self.listWidget_2.addItems(xlsFiles)

    def ClearListTab4(self):
        self.listWidget_2.clear()

    def ShowResultsTab4(self):
        if(not self.listWidget_2.currentItem()):
            return

        fileName = self.listWidget_2.currentItem().text()
        fileURL = self.Tab4DirPath + '/'+fileName
        if(os.path.splitext(fileName)[1] == ".mat"):
            if (self.lineEdit_4.text().__len__() is 0):
                kflod = 5
            else:
                kflod = int(self.lineEdit_4.text())

            if (self.lineEdit_5.text().__len__() is 0):
                numWave = 128
            else:
                numWave = int(self.lineEdit_5.text())

            if (self.lineEdit_6.text().__len__() is 0):
                numLearn = 30
            else:
                numLearn = int(self.lineEdit_6.text())

            if (self.lineEdit_3.text().__len__() is 0):
                iterNum = 5
            else:
                numLearn = int(self.lineEdit_3.text())


            self.textEdit.clear()
            accLDA,self.matLDA = Classifier.LDA(fileURL,iterNum,kflod)
            text = "LDA," + str(kflod) +"折交叉验证,迭代" +str(iterNum)+"次,准确率为:" + str(accLDA)
            self.textEdit.append(text)

            accSVM,self.matSVM = Classifier.SVM(fileURL,iterNum,kflod)
            text = "SVM," + str(kflod) + "折交叉验证,迭代" + str(iterNum) + "次,准确率为:" + str(accSVM)
            self.textEdit.append(text)

            accKNN,self.matKNN = Classifier.KNN(fileURL,iterNum,kflod)
            text = "KNN," + str(kflod) + "折交叉验证,迭代" + str(iterNum) + "次,准确率为:" + str(accKNN)
            self.textEdit.append(text)

            accDT,self.matDT = Classifier.DT(fileURL,iterNum,kflod)
            text = "DecisionTree," + str(kflod) + "折交叉验证,迭代" + str(iterNum) + "次,准确率为:" + str(accDT)
            self.textEdit.append(text)

            # accSDE,self.matSDE = Classifier.SDE(fileURL,kflod,numLearn,numWave)
            # text = "SDE," + str(kflod) + "折交叉验证," + str(numLearn) + "个弱学习器,子空间维数为"+str(numWave)+"时,准确率为:" + str(accSDE)
            # self.textEdit.append(text)

        if(os.path.splitext(fileName)[1] == ".xls"):
            pass
        if (os.path.splitext(fileName)[1] == ".csv"):
            pass

    def MatrixTab4(self):
        if(not hasattr(self,'matLDA')):
            return

        self.textEdit.append("confusion_matrix:LDA")
        for i in self.matLDA:
            self.textEdit.append(str(i))
        self.textEdit.append("confusion_matrix:SVM")
        for i in self.matSVM:
            self.textEdit.append(str(i))
        self.textEdit.append("confusion_matrix:KNN")
        for i in self.matKNN:
            self.textEdit.append(str(i))
        self.textEdit.append("confusion_matrix:DecisionTree")
        for i in self.matDT:
            self.textEdit.append(str(i))
        self.textEdit.append("confusion_matrix:SDE")
        # for i in self.matSDE:
        #     self.textEdit.append(str(i))

    def ReadMatTab2(self):
        self.Tab4DirPath = QFileDialog.getExistingDirectory()
        if (not self.Tab4DirPath):
            return
        matFiles = [i for i in os.listdir(self.Tab4DirPath) if os.path.splitext(i)[1] == ".mat"]
        if(not matFiles):
            return
        variableName = "afterSGSmooth"
        mat = sio.loadmat(matFiles)
        data = mat[variableName]
        newData = data[:256, :].T
        label = data[256, :].T


    def MovingFliter(self):
        pass

    def SGFliter(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MyWindow()
    Window.show()
    sys.exit(app.exec_())