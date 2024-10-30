import sys

import torch
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, \
    QMessageBox, QFileDialog
from PyQt5.QtGui import QImage, QPixmap, QIcon
import cv2
from qframelesswindow import FramelessWindow, StandardTitleBar
from worker import Worker
from main_interface import MainInterface


class MainWindow(FramelessWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.worker = Worker()


        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 40, 20, 20)
        self.mainInterface = MainInterface(parent=self, worker=self.worker)
        self.layout.addWidget(self.mainInterface)
        self.current_results = None
        self.init_window()

    def init_window(self):
        self.resize(1080, 784)
        self.setTitleBar(StandardTitleBar(self))
        self.titleBar.raise_()
        self.setWindowIcon(QIcon('logo.png'))
        self.setWindowTitle("钢板表面缺陷检测")

        # 居中布局
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
