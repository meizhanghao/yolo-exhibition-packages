import os
import shutil
import xml.etree.ElementTree as ET

# VOC格式数据集路径
voc_data_path = '../datasets'
voc_annotations_path = os.path.join(voc_data_path, 'Annotations')
voc_images_path = os.path.join(voc_data_path, 'JPEGImages')

# YOLO格式数据集保存路径
yolo_data_path = '../datasets/results'
yolo_images_path = os.path.join(yolo_data_path, 'images')
yolo_labels_path = os.path.join(yolo_data_path, 'labels')

# 创建YOLO格式数据集目录
os.makedirs(yolo_images_path, exist_ok=True)
os.makedirs(yolo_labels_path, exist_ok=True)

# 类别映射 (可以根据自己的数据集进行调整)
class_mapping = {
    'fire': 0,
    'smoke': 1,
    '_background_': 2,
    'other': 3
}


def convert_voc_to_yolo(voc_annotation_file, yolo_label_file):
    tree = ET.parse(voc_annotation_file)
    root = tree.getroot()

    size = root.find('size')
    width = float(size.find('width').text)
    height = float(size.find('height').text)

    with open(yolo_label_file, 'w') as f:
        for obj in root.findall('object'):
            cls = obj.find('name').text
            if cls not in class_mapping:
                continue
            cls_id = class_mapping[cls]
            xmlbox = obj.find('bndbox')
            xmin = float(xmlbox.find('xmin').text)
            ymin = float(xmlbox.find('ymin').text)
            xmax = float(xmlbox.find('xmax').text)
            ymax = float(xmlbox.find('ymax').text)

            x_center = (xmin + xmax) / 2.0 / width
            y_center = (ymin + ymax) / 2.0 / height
            w = (xmax - xmin) / width
            h = (ymax - ymin) / height

            f.write(f"{cls_id} {x_center} {y_center} {w} {h}\n")


def convert():
    # 遍历VOC数据集的Annotations目录，进行转换
    for voc_annotation in os.listdir(voc_annotations_path):
        if voc_annotation.endswith('.xml'):
            voc_annotation_file = os.path.join(voc_annotations_path, voc_annotation)
            image_id = os.path.splitext(voc_annotation)[0]
            voc_image_file = os.path.join(voc_images_path, f"{image_id}.jpg")
            yolo_label_file = os.path.join(yolo_labels_path, f"{image_id}.txt")
            yolo_image_file = os.path.join(yolo_images_path, f"{image_id}.jpg")

            convert_voc_to_yolo(voc_annotation_file, yolo_label_file)
            if os.path.exists(voc_image_file):
                shutil.copy(voc_image_file, yolo_image_file)

    print("转换完成！")


if __name__ == '__main__':
    convert()
