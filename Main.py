from MainWindow import *
from ShowData import *

import sys
import os,re
import pandas as pd

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
import xlwt
import matplotlib.pyplot as plt

def showSpectrum():
    p1 = QCursor.pos()
    p2 = Window.lab.mapToGlobal(Window.lab.pos())
    p = p1 - p2

    gw = ui.graphicsView.width()
    gh = ui.graphicsView.height()
    sw = ui.graphicsView.scene().width()
    sh = ui.graphicsView.scene().height()

    _w = (gw-sw)/2
    _h = (gh-sh)/2

    if(p.x()- _w > 0 and p.x() - _w < sw and p.y()-_h> 0 and p.y()- _h<sh):
        x = int(p.x() - _w)
        y = int(p.y() - _h)
        plt.figure("Spectral curve")
        a = float(Window.w[0])
        b = float(Window.w[-1])
        c = int(Window.b)

        plt.plot(np.linspace(a,b,c),Window.image[y, :, x])
        plt.xticks(np.linspace(a,b,c/20))
        plt.plot(Window.w[ui.comboBox.currentIndex()],
                 Window.image[y, :, x][ui.comboBox.currentIndex()],'o')
        plt.legend(["Spectral curve","Current spectral band"])
        plt.show()
    else:
        msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
        msg_box.exec_()

def saveImage():
    savePath = QFileDialog.getSaveFileName()
    band = ui.comboBox.currentIndex()
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
        self.action2 = self.contextMenu.addAction(QIcon('img/save.png'), u'保存图片')
        self.action2.triggered.connect(saveImage)
        self.action3 = self.contextMenu.addAction(QIcon('img/excel.png'), u'保存该点光谱至Excel')
        self.action3.triggered.connect(saveSpectrumToExcel)
        self.action4 = self.contextMenu.addAction(QIcon('img/CSV.png'), u'保存该点光谱至CSV')
        self.action4.triggered.connect(saveSpectrumToCSV)

    def showContextMenu(self):
        self.contextMenu.exec_(QCursor.pos())


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        ui.setupUi(self)
        ui.statusbar.showMessage("西北农林科技大学   Powerby PyQt")


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
        minR = 10
        maxR = 70
        if(self.lineEdit_2.text() is None):
            print("None")
        else:
            print(self.lineEdit_2.text())

        if (self.lineEdit.text() is None):
            print("None")
        else:
            print(self.lineEdit.text())
        circle = cv2.HoughCircles(img2D, cv2.HOUGH_GRADIENT, 1,
                                  30, param1=100, param2=25, minRadius=minR, maxRadius=maxR)
        if(not circle is None):
            circles = circle[0, :, :];
            circles = np.uint16(np.around(circles))
            for i in circles[:]:
                cv2.circle(img2D, (i[0], i[1]), i[2], (255, 0, 0), 2)
                cv2.circle(img2D, (i[0], i[1]), 2, (255, 0, 0), 4)


        height, width = img2D.shape
        bytesPerComponent = 1
        bytesPerLine = bytesPerComponent * width
        Qimg = QImage(img2D, width, height, bytesPerLine, QImage.Format_Grayscale8)

        scene = QGraphicsScene()
        scene.addPixmap(QPixmap(Qimg))

        return scene


    def ShowBond(self):
        band = ui.comboBox.currentIndex()
        scene = self.ConventToQImage(band)
        ui.graphicsView.setScene(scene)
        ui.lcdNumber.display(self.w[band])

    def OnClickedTab1Button(self):
        filePath = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd())
        filename = re.search("\/+([^\/]*$)", filePath[0]).group(1)
        self.w,self.l,self.s,self.b,self.dt= readInfo(filePath[0]+".hdr")
        self.image = showData(filePath[0])

        if filePath:
            scene = self.ConventToQImage(197)
            ui.graphicsView.setScene(scene)

        ui.comboBox.addItems(self.w)
        ui.label.setText("文件名称: "+filename)
        ui.label_2.setText("Lines: " + str(self.l))
        ui.label_3.setText("Samples:  " + str(self.s))
        ui.label_4.setText("Bands: " + str(self.b))
        ui.label_6.setText("波段范围: " + self.w[0]+"~"+self.w[-1])
        ui.lcdNumber.setDigitCount(8)
        ui.lcdNumber.display(self.w[197])

        self.lab = MenuLabel()
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0,0,0,0)
        vbox.addWidget(self.lab)

        ui.graphicsView.setLayout(vbox)

    def OnCilickedTab2Butto1(self):
        self.dirPath = QFileDialog.getExistingDirectory()
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
        pass

    def OnCilickedTab2Butto4(self):
        pass



if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = Ui_Hyperspectral()
    Window = MyWindow()

    Window.show()
    sys.exit(app.exec_())