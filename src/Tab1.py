import matplotlib.pyplot as plt
import numpy as np
import xlwt
from PyQt5.QtWidgets import QMessageBox,QFileDialog
from PyQt5.QtGui import QImage,QCursor,QIcon,QPixmap
import pandas as pd
# from PyQt5.QtWidgets import *

class Tab1(object):
    def __init__(self,MainWindow):
        self.window= MainWindow
        
    def showSpectrum(self):
        p = self.window.lab.point

        gw = self.window.graphicsView.width()
        gh = self.window.graphicsView.height()
        sw = self.window.graphicsView.scene().width()
        sh = self.window.graphicsView.scene().height()

        _w = (gw - sw) / 2
        _h = (gh - sh) / 2

        if (p.x() - _w > 0 and p.x() - _w < sw and p.y() - _h > 0 and p.y() - _h < sh):
            x = int(p.x() - _w)
            y = int(p.y() - _h)

            a = float(self.window.w[0])
            b = float(self.window.w[-1])
            c = int(self.window.b)
            self.window.waveData.clear()
            self.window.waveData.append(self.window.image[y, :, x])
            plt.close()

            plt.figure("Spectral curve")
            for i, j in enumerate(self.window.waveData):
                plt.plot(np.linspace(a, b, c), j)
            plt.axvline(float(self.window.w[self.window.comboBox.currentIndex()]))
            plt.plot(float(self.window.w[self.window.comboBox.currentIndex()]),
                     self.window.image[y, :, x][self.window.comboBox.currentIndex()], 'o')
            plt.xticks(np.linspace(a, b, c / 20))
            # plt.legend(["Spectral curve","Current spectral band"])
            plt.show()

        else:
            msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
            msg_box.exec_()

    def showSpectrumInCurrentFigure(self):

        p = self.window.lab.point

        gw = self.window.graphicsView.width()
        gh = self.window.graphicsView.height()
        sw = self.window.graphicsView.scene().width()
        sh = self.window.graphicsView.scene().height()

        _w = (gw - sw) / 2
        _h = (gh - sh) / 2

        if (p.x() - _w > 0 and p.x() - _w < sw and p.y() - _h > 0 and p.y() - _h < sh):
            x = int(p.x() - _w)
            y = int(p.y() - _h)

            a = float(self.window.w[0])
            b = float(self.window.w[-1])
            c = int(self.window.b)

            self.window.waveData.append(self.window.image[y, :, x])

            plt.close()
            plt.figure("Spectral curve")
            for i, j in enumerate(self.window.waveData):
                plt.plot(np.linspace(a, b, c), j)
            plt.xticks(np.linspace(a, b, c / 20))
            plt.axvline(float(self.window.w[self.window.comboBox.currentIndex()]))
            plt.plot(float(self.window.w[self.window.comboBox.currentIndex()]),
                     self.window.image[y, :, x][self.window.comboBox.currentIndex()], 'o')
            plt.show()
        else:
            msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
            msg_box.exec_()

    def saveSpectrumToCSV(self):
        p1 = QCursor.pos()
        p2 = self.window.lab.mapToGlobal(self.window.lab.pos())
        p = p1 - p2

        gw = self.window.graphicsView.width()
        gh = self.window.graphicsView.height()
        sw = self.window.graphicsView.scene().width()
        sh = self.window.graphicsView.scene().height()

        _w = (gw - sw) / 2
        _h = (gh - sh) / 2

        if (p.x() - _w > 0 and p.x() - _w < sw and p.y() - _h > 0 and p.y() - _h < sh):
            x = int(p.x() - _w)
            y = int(p.y() - _h)
            a = float(self.window.w[0])
            b = float(self.window.w[-1])
            c = int(self.window.b)
            wave = self.window.w
            data = self.window.image[y, :, x]

            dataFrame = pd.DataFrame({'Wave': wave, 'Data': data})
            fileName = self.window.label.text()
            fileName = fileName[5:] + '.csv'
            dataFrame.to_csv(fileName, index=False, sep=',')

        else:
            msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
            msg_box.exec_()

    def saveSpectrumToExcel(self):
        p1 = QCursor.pos()
        p2 = self.window.lab.mapToGlobal(self.window.lab.pos())
        p = p1 - p2

        gw = self.window.graphicsView.width()
        gh = self.window.graphicsView.height()
        sw = self.window.graphicsView.scene().width()
        sh = self.window.graphicsView.scene().height()

        _w = (gw - sw) / 2
        _h = (gh - sh) / 2

        if (p.x() - _w > 0 and p.x() - _w < sw and p.y() - _h > 0 and p.y() - _h < sh):
            x = int(p.x() - _w)
            y = int(p.y() - _h)
            a = float(self.window.w[0])
            b = float(self.window.w[-1])
            c = int(self.window.b)
            wave = self.window.w
            data = self.window.image[y, :, x]

            excelFile = xlwt.Workbook(encoding='utf-8')
            booksheet = excelFile.add_sheet('Spectrum', cell_overwrite_ok=True)

            booksheet.write(0, 0, "Wave")
            for i, j in enumerate(wave):
                booksheet.write(i + 1, 0, str(j))

            booksheet.write(0, 1, 'Data')
            for l, m in enumerate(data):
                booksheet.write(l + 1, 1, str(m))
            fileName = self.window.label.text()
            fileName = fileName[5:] + '.xls'
            excelFile.save(fileName)

        else:
            msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
            msg_box.exec_()

    def saveImage(self):
        savePath = QFileDialog.getSaveFileName()
        band = self.window.comboBox.currentIndex()
        img2D = np.uint8(self.window.image[:, band, :] * 255)
        height, width = img2D.shape
        bytesPerComponent = 1
        bytesPerLine = bytesPerComponent * width
        Qimg = QImage(img2D, width, height, bytesPerLine, QImage.Format_Grayscale8)
        Qimg.save(savePath[0])

    def saveSpectrumToCSV(self):
        p1 = QCursor.pos()
        p2 = self.window.lab.mapToGlobal(self.window.lab.pos())
        p = p1 - p2

        gw = self.window.graphicsView.width()
        gh = self.window.graphicsView.height()
        sw = self.window.graphicsView.scene().width()
        sh = self.window.graphicsView.scene().height()

        _w = (gw - sw) / 2
        _h = (gh - sh) / 2

        if (p.x() - _w > 0 and p.x() - _w < sw and p.y() - _h > 0 and p.y() - _h < sh):
            x = int(p.x() - _w)
            y = int(p.y() - _h)
            a = float(self.window.w[0])
            b = float(self.window.w[-1])
            c = int(self.window.b)
            wave = self.window.w
            data = self.window.image[y, :, x]

            dataFrame = pd.DataFrame({'Wave': wave, 'Data': data})
            fileName = self.window.label.text()
            fileName = fileName[5:] + '.csv'
            dataFrame.to_csv(fileName, index=False, sep=',')

        else:
            msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
            msg_box.exec_()

    def saveSpectrumToExcel(self):
        p1 = QCursor.pos()
        p2 = self.window.lab.mapToGlobal(self.window.lab.pos())
        p = p1 - p2

        gw = self.window.graphicsView.width()
        gh = self.window.graphicsView.height()
        sw = self.window.graphicsView.scene().width()
        sh = self.window.graphicsView.scene().height()

        _w = (gw - sw) / 2
        _h = (gh - sh) / 2

        if (p.x() - _w > 0 and p.x() - _w < sw and p.y() - _h > 0 and p.y() - _h < sh):
            x = int(p.x() - _w)
            y = int(p.y() - _h)
            a = float(self.window.w[0])
            b = float(self.window.w[-1])
            c = int(self.window.b)
            wave = self.window.w
            data = self.window.image[y, :, x]

            excelFile = xlwt.Workbook(encoding='utf-8')
            booksheet = excelFile.add_sheet('Spectrum', cell_overwrite_ok=True)

            booksheet.write(0, 0, "Wave")
            for i, j in enumerate(wave):
                booksheet.write(i + 1, 0, str(j))

            booksheet.write(0, 1, 'Data')
            for l, m in enumerate(data):
                booksheet.write(l + 1, 1, str(m))
            fileName = self.window.label.text()
            fileName = fileName[5:] + '.xls'
            excelFile.save(fileName)

        else:
            msg_box = QMessageBox(QMessageBox.Warning, "Warning", "请选择有效区域!")
            msg_box.exec_()