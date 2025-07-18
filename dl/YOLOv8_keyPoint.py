# -*- coding: UTF-8 -*-
import numpy as np
import cv2
import os
from ultralytics import YOLO
from util.logger import logger
import torch

print('YOLOv8 key point model train and test code URL: https://docs.ultralytics.com/tasks/pose/')
device = torch.device('cuda:0' if torch.cuda.is_available() else "cpu")


def normPoints(points, box):
    minx, miny, maxx, maxy = points[0][0], points[0][1], points[0][0], points[0][1]
    for i in range(len(points)):
        x = round(max(box[0], min(points[i][0], box[2])))
        y = round(max(box[1], min(points[i][1], box[3])))
        minx = min(x, minx)
        miny = min(y, miny)
        maxx = max(x, maxx)
        maxy = max(y, maxy)
        points[i] = [x, y]
    width = maxx - minx
    height = maxy - miny
    if width < (box[2] - box[0]) / 4 or height < (box[3] - box[1]) / 4:
        return np.array([[box[0], box[1]], [box[2], box[1]], [box[2], box[3]], [box[0], box[3]]])
    return points


def orderPoints(points):
    dstPoints = np.zeros((4, 2), dtype="float32")
    s = points.sum(axis=1)
    dstPoints[0] = points[np.argmin(s)]
    dstPoints[2] = points[np.argmax(s)]
    diff = np.diff(points, axis=1)
    dstPoints[1] = points[np.argmin(diff)]
    dstPoints[3] = points[np.argmax(diff)]
    return dstPoints


def warpImage(image, box, width, height):
    box = np.array(box, dtype=np.float32)

    dst_rect = np.array([[0, 0],
                         [width, 0],
                         [width, height],
                         [0, height]], dtype="float32")

    M = cv2.getPerspectiveTransform(box, dst_rect)
    warped = cv2.warpPerspective(image, M, (width, height))
    return warped


def yolov8_keypoint(image_path, model_path, save_path, reSize=[1000, 750], dstSize=[960, 720]):
    try:
        model = YOLO(model_path)
        image = cv2.imread(image_path)
        image = cv2.resize(image, reSize)
        result = model(image, device=device)
        if len(result) < 1:
            logger.error('keypoint - yolov8_keypoint - Image correct failed!')
            return image
        save_path = os.path.join(save_path, 'result.jpg')
        print(save_path)
        result[0].save(filename=save_path)
        key_point = result[0].keypoints.xy
        key_point = key_point.cpu().numpy()[0]
        box = result[0].boxes.xyxy
        box = box.cpu().numpy()[0]
        key_point = normPoints(key_point, box)
        key_point = orderPoints(key_point)
        dst = warpImage(image, key_point, dstSize[0], dstSize[1])
        return dst
    except Exception as e:
        logger.error(f'keypoint - yolov8_keypoint - {e}')
        image = cv2.imread(image_path)
        return image


# path = r'F:\speed\yolov8\ss\1674903566906.jpg'
# vi = yolov8_keypoint(path, r'D:\F\prenatal_py38\configs\yolov8_best_model_correct.pt', r'D:\F\prenatal_py38\output')
# cv2.imwrite(r'D:\F\prenatal_py38\output\output.jpg', vi)
