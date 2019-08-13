from src.ui.MainWindow import *
from src.ShowData import *
import scipy.io as sio
from scipy.signal import savgol_filter
from src import Classifier

import sys
import os
import pandas as pd

from PyQt5.QtGui import QImage,QCursor,QIcon,QPixmap
from PyQt5.QtCore import Qt,QRectF
from PyQt5.QtWidgets import *

import matplotlib.pyplot as plt
import numpy as np
from src.Tab1 import Tab1
from src.Tab2 import Tab2

class MyWindow(QMainWindow,Ui_Hyperspectral):
    def __init__(self,parent = None):
        super(MyWindow,self).__init__(parent)
        self.setupUi(self)
        self.action_4.triggered.connect(self.about)

        '''Tab1 Init'''
        self.Tab1 = Tab1(MainWindow = self)

        ''' Tab2 Init '''
        self.Tab2 = Tab2(MainWindow = self)

        self.scene = self.MyGraphicsScene()

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

    class MyGraphicsScene(QGraphicsScene):
        def mousePressEvent(self, event):
            self.pressPos = event.scenePos()
            self.Rec = QRectF(self.pressPos, self.pressPos)
            self.RecItem = QGraphicsRectItem(self.Rec)
            self.RecItem.setVisible(True)
            self.addItem(self.RecItem)

        def mouseMoveEvent(self, event):
            self.movePos = event.scenePos()
            self.removeItem(self.RecItem)
            self.RecItem.setRect(QRectF(self.pressPos, self.movePos))
            self.addItem(self.RecItem)

        def mouseReleaseEvent(self, event):
            pass

    class MenuLabel(QLabel):
        def __init__(self,myWindow):
            QLabel.__init__(self)
            self.win = myWindow
            self.createContextMenu()
            self.point = None

        def mousePressEvent(self, ev: QtGui.QMouseEvent):
            self.point = ev.pos()

        def createContextMenu(self):
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.showContextMenu)
            self.contextMenu = QMenu(self)
            self.action = self.contextMenu.addAction(QIcon('img/line.png'), u'显示光谱曲线')
            self.action.triggered.connect(self.win.Tab1.showSpectrum)
            self.action1 = self.contextMenu.addAction(QIcon('img/line.png'), u'在现有图中显示光谱曲线')
            self.action1.triggered.connect(self.win.Tab1.showSpectrumInCurrentFigure)
            self.action2 = self.contextMenu.addAction(QIcon('img/save.png'), u'保存图片')
            self.action2.triggered.connect(self.win.Tab1.saveImage)
            self.action3 = self.contextMenu.addAction(QIcon('img/excel.png'), u'保存该点光谱至Excel')
            self.action3.triggered.connect(self.win.Tab1.saveSpectrumToExcel)
            self.action4 = self.contextMenu.addAction(QIcon('img/CSV.png'), u'保存该点光谱至CSV')
            self.action4.triggered.connect(self.win.Tab1.saveSpectrumToCSV)

        def showContextMenu(self):
            self.contextMenu.exec_(QCursor.pos())

    # def ConventToQImage(self, band):
    #     return self.Tab2.ConventToQImage()
    #
    # def ConventToQImageWithHough(self, band):
    #     return self.Tab2.ConventToQImageWithHough(band=band)

    def ShowBond(self):
        self.Tab1.ShowBond()

    def OnClickedTab1Button(self):
        self.Tab1.OnClickedTab1Button()

    def OnCilickedTab2Butto1(self):
        self.Tab2.OnCilickedTab2Butto1()

    def OnChangedTab2listWidget(self):
        self.Tab2.OnChangedTab2listWidget()

    def OnChangedTab2ComboBox1(self):
        self.Tab2.OnChangedTab2ComboBox1()


    def OnCilickedTab2Butto2(self):
        self.Tab2.OnCilickedTab2Butto2()

    def OnCilickedTab2Butto3(self):
        self.Tab2.OnCilickedTab2Butto3()

    def OnCilickedTab2Butto4(self):
        self.Tab2.OnCilickedTab2Butto4()

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
            accLDA,self.matLDA = Classifier.LDA(fileURL, iterNum, kflod)

            text = 'LDA,{0}折交叉验证,迭代{1}次,准确率为:{2}'.format(kflod,iterNum,accLDA)
            self.textEdit.append(text)

            accSVM,self.matSVM = Classifier.SVM(fileURL, iterNum, kflod)
            text = 'SVM,{0}折交叉验证,迭代{1}次,准确率为:{2}'.format(kflod, iterNum, accSVM)
            self.textEdit.append(text)

            accKNN,self.matKNN = Classifier.KNN(fileURL, iterNum, kflod)
            text = 'KNN,{0}折交叉验证,迭代{1}次,准确率为:{2}'.format(kflod, iterNum, accKNN)
            self.textEdit.append(text)

            accDT,self.matDT = Classifier.DT(fileURL, iterNum, kflod)
            text = 'DecisionTree,{0}折交叉验证,迭代{1}次,准确率为:{2}'.format(kflod, iterNum, accDT)
            self.textEdit.append(text)

            accSDE,self.matSDE = Classifier.SDE(fileURL, kflod, numLearn, numWave)
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

        if (not matFiles):
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
