import cv2


def draw_boxes(img, results, rectangle_thickness=2, text_thickness=2):
    colors = [(89, 161, 197), (57, 76, 139), (19, 222, 24), (186, 55, 2), (167, 146, 11), (190, 76, 98), (139, 71, 93),
              (84, 139, 84)]
    for result in results:
        for box in result.boxes:
            conf = box.conf
            idx = int(box.cls.item()) % len(colors)
            color = colors[idx]
            cv2.rectangle(img,
                          (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                          (int(box.xyxy[0][2]), int(box.xyxy[0][3])),
                          color,
                          rectangle_thickness)
            cv2.putText(img,
                        f"{result.names[int(box.cls[0])]} {round(conf.item(), 1)}",
                        (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                        cv2.FONT_HERSHEY_PLAIN,
                        2,
                        color,
                        text_thickness)
    return img, results
