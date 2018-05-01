from MainWindow import *
from ShowData import *
import scipy.io as sio
from scipy.signal import savgol_filter
import Classifier

import sys
import os,re
import pandas as pd

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt,QRectF,QPointF,QPoint

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

class MyGraphicsScene(QGraphicsScene):

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
        self.pressPos = event.scenePos()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        self.movePos = event.scenePos()

        pen = QPen()
        pen.setColor(QColor(255, 0, 0))
        bru = QBrush()
        self.addLine(self.pressPos.x(),self.pressPos.y(),self.movePos.x(),self.pressPos.y(), pen)
        self.addLine(self.pressPos.x(),self.pressPos.y(),self.pressPos.x(),self.movePos.y(), pen)



    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent'):
        self.relessPos= event.scenePos()
        rec = QRectF(QPointF(self.pressPos), self.relessPos)
        pen = QPen()
        pen.setColor(QColor(255, 0, 0))
        bru = QBrush()
        self.addRect(rec, pen, bru)

class MyWindow(QMainWindow,Ui_Hyperspectral):
    def __init__(self,parent = None):
        super(MyWindow,self).__init__(parent)
        self.setupUi(self)

        self.action_4.triggered.connect(self.about)
        ''' Tab2 Init '''
        self.lineEdit.setText("10")
        self.lineEdit_2.setText("70")
        self.lineEdit_3.setText("5")
        self.lineEdit_4.setText("5")
        self.lineEdit_5.setText("128")
        self.lineEdit_6.setText("30")
        list = ['1','2','3','4','5','6']
        for i in range(1,31,1):
            if(i%2):
                self.comboBox_6.addItems([str(i)])
                self.comboBox_5.addItems([str(i)])
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

        scene = MyGraphicsScene()
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
        pen = QPen()
        pen.setColor(QColor(255, 0, 0))
        self.graphicsView_2.scene().addRect(0, 0, 200, 200, pen, QBrush())


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
                iterNum = int(self.lineEdit_3.text())


            self.textEdit.clear()
            accLDA,self.matLDA = Classifier.LDA(fileURL,iterNum,kflod)

            text = 'LDA,{0}折交叉验证,迭代{1}次,准确率为:{2}'.format(kflod,iterNum,accLDA)
            self.textEdit.append(text)

            accSVM,self.matSVM = Classifier.SVM(fileURL,iterNum,kflod)
            text = 'SVM,{0}折交叉验证,迭代{1}次,准确率为:{2}'.format(kflod, iterNum, accSVM)
            self.textEdit.append(text)

            accKNN,self.matKNN = Classifier.KNN(fileURL,iterNum,kflod)
            text = 'KNN,{0}折交叉验证,迭代{1}次,准确率为:{2}'.format(kflod, iterNum, accKNN)
            self.textEdit.append(text)

            accDT,self.matDT = Classifier.DT(fileURL,iterNum,kflod)
            text = 'DecisionTree,{0}折交叉验证,迭代{1}次,准确率为:{2}'.format(kflod, iterNum, accDT)
            self.textEdit.append(text)

            accSDE,self.matSDE = Classifier.SDE(fileURL,kflod,numLearn,numWave)
            text = 'SDE,{0}折交叉验证,{1}个弱学习器,子空间维数为{2}时,准确率为:{3}'.format(kflod, numLearn,numWave,accSDE)
            self.textEdit.append(text)

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
        for i in self.matSDE:
            self.textEdit.append(str(i))

    def ReadMatTab2(self):
        self.Tab4DirPath = QFileDialog.getExistingDirectory()
        if (not self.Tab4DirPath):
            return
        matFiles = [i for i in os.listdir(self.Tab4DirPath) if os.path.splitext(i)[1] == ".mat"]

        if(not matFiles):
            return
        else:
            self.listWidget_3.addItems(matFiles)

    def MovingFliter(self):
        fileName = self.listWidget_3.currentItem().text()
        num = int(self.comboBox_6.currentText())

        if(fileName):
            variableName = "afterSGSmooth"
            matUrl = os.path.join(self.Tab4DirPath,fileName)
            mat = sio.loadmat(matUrl)
            data = mat[variableName]
            newData = data[:256, :].T
            moving  = pd.rolling_mean(newData,num)
            plt.figure("Moving")
            plt.subplot(121)
            for i in newData:
                plt.plot(i)
            plt.title("BeforeSmooth")

            plt.subplot(122)
            for i in moving:
                plt.plot(i)
            plt.title("AfterSmooth")
            plt.show()
            newMatName = fileName[:-4]+"_AfterMovingSmooth.mat"
            sio.savemat(os.path.join(self.Tab4DirPath,newMatName),{"Data": moving})
            self.listWidget_4.addItems([newMatName])

    def SGFliter(self):
        fileName = self.listWidget_3.currentItem().text()
        num = int(self.comboBox_5.currentText())
        poly = int(self.comboBox_4.currentText())
        if (fileName):
            variableName = "Data"
            matUrl = os.path.join(self.Tab4DirPath, fileName)
            mat = sio.loadmat(matUrl)
            data = mat[variableName]
            newData = data[:256, :].T

            plt.figure("Savitzky-Golay")
            plt.subplot(121)
            for i in newData:
                plt.plot(i)
            plt.title("BeforeSmooth")

            plt.subplot(122)
            sg = savgol_filter(newData,num,poly)
            for i in sg:
                plt.plot(i)
            plt.title("AfterSmooth")
            plt.show()
            newMatName = fileName[:-4] + "_AfterSGSmooth.mat"
            sio.savemat(os.path.join(self.Tab4DirPath, newMatName), {"Data": sg})
            self.listWidget_4.addItems([newMatName])

    def about(self):
        msg_box = QMessageBox(QMessageBox.Information,"关于本软件",
                              "<p align='center'>陕西省大学生科技创新项目</p>"
                              "<p align='center'>基于高光谱图像的苹果表面农残检测研究成果</p>"
                              "<p align='right'> 西北农林科技大学信息工程学院</p>"
                              "<p align='right'> 贾亚光,邵夏天</p>"

                              )
        msg_box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = MyWindow()
    Window.show()
    sys.exit(app.exec_())