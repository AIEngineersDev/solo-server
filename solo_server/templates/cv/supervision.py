import cv2
import supervision as sv
from ultralytics import YOLO

image = cv2.imread(...)
model = YOLO('yolov8s.pt')
result = model(image)[0]
detections = sv.Detections.from_ultralytics(result)

len(detections)
# 5