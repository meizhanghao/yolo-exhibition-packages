import time

import cv2
import numpy as np
import torch
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
from ultralytics import YOLO
from collections import defaultdict
import os
import utils.draw_boxes as Boxes

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
np.set_printoptions(suppress=True)


class Worker(QThread):
    send_img = pyqtSignal(np.ndarray)
    send_raw = pyqtSignal(np.ndarray)

    send_msg = pyqtSignal(str)
    send_fps = pyqtSignal(str)

    def __init__(self):
        super(Worker, self).__init__()
        self.source = None
        self.model_path = None
        self.model = None

        self.jump_out = False
        self.is_continue = True

    def run(self):
        try:
            self.detect_video(video_path=self.source, save_path='')
        except Exception as e:
            self.send_msg.emit('%s' % e)

    def load_model(self):
        model_path, _ = QFileDialog.getOpenFileName(None, "选择模型文件", "", "模型文件 (*.pt)")
        if model_path:
            self.model_path = model_path
            return self.init_model(model_path)

    def init_model(self, model_path):
        if model_path:
            model = YOLO(model_path)
            self.model = model.to(device)
            return model
        return False

    def detect_image(self, images):
        model = self.init_model(self.model_path)
        results = model.predict(images)
        return results

    # def draw_boxes(self, img, results, rectangle_thickness=2, text_thickness=1):
    #     for result in results:
    #         for box in result.boxes:
    #             cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
    #                           (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)
    #             cv2.putText(img, f"{result.names[int(box.cls[0])]}",
    #                         (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
    #                         cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
    #     return img, results

    def detect_video(self, video_path, save_path):
        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # fps = cap.get(cv2.CAP_PROP_FPS)
        fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
        if fps == 0:
            fps = 20.0  # 如果无法获取帧率，则设置为默认值

        # out = cv2.VideoWriter(save_path, fourcc, fps, (frame_width, frame_height), True)

        model = self.init_model(self.model_path)
        video_frame = 0
        average_fps = 0.0
        try:
            while True:
                success, frame = cap.read()
                print('视频帧获取是否成功：{}'.format(success))
                if success:
                    start = time.time()
                    results = model.predict(frame, conf=0.5)
                    end = time.time()
                    video_frame = video_frame + 1
                    video_fps = 1.0 / (end - start)
                    average_fps += video_fps
                    print('当前帧：{}'.format(video_frame))
                    print("平均帧率: %.1f" % (average_fps / video_frame))
                    # annotated_frame = results[0].plot()
                    # annotated_frame = results[0].plot()
                    Boxes.draw_boxes(frame, results)
                    # Boxes.drawBoxes(frame, results[0].boxes.data, score=True)
                    # out.write(frame)
                    # self.send_img.emit(annotated_frame if isinstance(annotated_frame, np.ndarray) else annotated_frame[0])
                    self.send_img.emit(frame if isinstance(frame, np.ndarray) else frame[0])
                    # if cv2.waitKey(1) & 0xFF == ord("q"):
                    if 0xFF == ord("q"):
                        break
                else:
                    print('结束了')
                    break
            cap.release()
            # out.release()
            cv2.destroyAllWindows()
        except Exception as e:
            print(e)

    def set_source(self, source):
        self.source = source
