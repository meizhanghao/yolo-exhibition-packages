import sys

import cv2
from IPython.external.qt_for_kernel import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog
from qfluentwidgets import CardWidget, BodyLabel, DisplayLabel, TitleLabel


class MainInterface(QFrame):
    def __init__(self, parent=None, worker=None):
        super(MainInterface, self).__init__(parent)
        self.worker = worker
        # 水平布局，用于放置左右两个 QLabel
        self.layout = QVBoxLayout(self)

        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        font.setBold(True)
        # font.setWeight(75)

        hbox_video_labels = QHBoxLayout()
        label1 = QLabel('钢板表面缺陷检测')
        # hbox_video_labels.setAlignment(Qt.AlignJustify)
        label1.setFont(font)
        label1.setFixedSize(160, 30)
        hbox_video_labels.addWidget(label1)

        self.layout.addLayout(hbox_video_labels)

        # cardWidget1 = CardWidget()
        # self.layout.addWidget(cardWidget1)

        cardWidget2 = CardWidget()
        self.layout.addWidget(cardWidget2)

        hbox_video = QHBoxLayout()
        cardWidget2.setLayout(hbox_video)


        # 创建两个 QLabel 分别显示左右图像
        self.label1 = QLabel()
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setMinimumSize(580, 450)  # 设置大小
        self.label1.setStyleSheet('border:3px solid #6950a1;')  # 添加边框并设置背景颜色为黑色

        self.label2 = QLabel()
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setMinimumSize(580, 450)  # 设置大小
        self.label2.setStyleSheet('border:3px solid #6950a1;')  # 添加边框并设置背景颜色为黑色

        hbox_video.addWidget(self.label1)  # 左侧显示原始图像
        hbox_video.addWidget(self.label2)  # 右侧显示检测后的图像

        hbox_buttons = QHBoxLayout()
        hbox_buttons.setAlignment(Qt.AlignRight)
        # self.layout.addLayout(hbox_buttons)
        hbox_video_labels.addStretch(1)
        hbox_video_labels.addLayout(hbox_buttons)

        # 添加模型选择按钮
        self.load_model_button = QPushButton("📁模型选择")
        self.load_model_button.clicked.connect(self.load_model)
        self.load_model_button.setFixedSize(120, 30)
        hbox_buttons.addWidget(self.load_model_button)

        # 添加图片检测按钮
        self.image_detect_button = QPushButton("💾图片检测")
        self.image_detect_button.clicked.connect(self.handler_open_image)
        self.image_detect_button.setEnabled(False)
        self.image_detect_button.setFixedSize(120, 30)
        hbox_buttons.addWidget(self.image_detect_button)

        # 添加视频检测按钮
        self.video_detect_button = QPushButton("🎬视频检测")
        self.video_detect_button.clicked.connect(self.handler_open_video)
        self.video_detect_button.setEnabled(False)
        self.video_detect_button.setFixedSize(120, 30)
        hbox_buttons.addWidget(self.video_detect_button)

        # 添加显示检测物体按钮
        self.display_objects_button = QPushButton("🔍显示检测物体")
        self.display_objects_button.clicked.connect(self.show_detected_objects)
        self.display_objects_button.setEnabled(False)
        self.display_objects_button.setFixedSize(120, 30)
        hbox_buttons.addWidget(self.display_objects_button)

        # 添加退出按钮
        self.exit_button = QPushButton("❌退出")
        self.exit_button.clicked.connect(self.exit_application)
        self.exit_button.setFixedSize(120, 30)
        # hbox_buttons.addWidget(self.exit_button)

        action_buttons = QHBoxLayout()
        action_buttons.setAlignment(Qt.AlignRight)
        # 添加开始检测
        self.detect_button = QPushButton('📺开始检测')
        self.detect_button.clicked.connect(self.detect_application)
        self.detect_button.setFixedSize(120, 30)
        action_buttons.addWidget(self.detect_button)

        self.layout.addLayout(action_buttons)

        self.initWidget()
        self.add_event_listener()

    def add_event_listener(self):
        self.worker.send_img.connect(lambda x: self.show_image(x, self.label2))
        self.worker.send_raw.connect(lambda x: self.show_image(x, self.label2))

    @staticmethod
    def show_image(img_src, label):
        try:
            frame = cv2.cvtColor(img_src, cv2.COLOR_BGR2RGB)
            img = QImage(frame.data, frame.shape[1], frame.shape[0], frame.shape[2] * frame.shape[1],
                         QImage.Format_RGB888)

            label.setPixmap(QPixmap.fromImage(img))
            label.setScaledContents(True)

        except Exception as e:
            print(repr(e))

    def initWidget(self):
        self.layout.setContentsMargins(0, 0, 0, 0)

    def load_model(self):
        if self.worker.load_model():
            self.image_detect_button.setEnabled(True)
            self.video_detect_button.setEnabled(True)
            self.display_objects_button.setEnabled(True)

    def handler_open_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "图片文件 (*.jpg *.jpeg *.png)")
        if not image_path:
            print('沒有找到文件')
        self.worker.set_source(image_path)

    def open_file(self, args):
        image_path, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", args)
        if not image_path:
            print('沒有找到文件')
        self.worker.set_source(image_path)

    def handler_open_video(self):
        video_path, _ = QFileDialog.getOpenFileName(self, 'Video/image', '', "Pic File(*.mp4 *.mkv *.avi *.flv "
                                                                             "*.jpg *.png)")
        if not video_path:
            print('沒有找到文件')
        self.worker.set_source(video_path)

    def show_detected_objects(self):
        if self.current_results:
            print(self.current_results)

    def detect_application(self):
        if not self.worker.isRunning():
            self.worker.start()

    def exit_application(self):
        # 终止程序运行
        sys.exit()
