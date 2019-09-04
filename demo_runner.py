#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on 2019/07/04
@author: lujie
"""

import os
import cv2
import time
import torch
from PIL import Image
import matplotlib.pyplot as plt
import torchvision.transforms as T
from detectlib import fasterrcnn_resnet50_fpn
from IPython import embed


COCO_INSTANCE_CATEGORY_NAMES = [
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]


def get_prediction(img_path, threshold):

    img = Image.open(img_path) # Load the image
    transform = T.Compose([T.ToTensor()]) # Defing PyTorch Transform
    img = transform(img) # Apply the transform to the image
    pred = model([img]) # Pass the image to the model
    pred_class = [COCO_INSTANCE_CATEGORY_NAMES[i] for i in list(pred[0]['labels'].numpy())] # Get the Prediction Score
    pred_boxes = [[(i[0], i[1]), (i[2], i[3])] for i in list(pred[0]['boxes'].detach().numpy())] # Bounding boxes
    pred_score = list(pred[0]['scores'].detach().numpy())  # already sorted in ascend
    pred_t = [pred_score.index(x) for x in pred_score if x > threshold][-1] # Get list of index with score greater than threshold.

    pred_boxes = pred_boxes[:pred_t+1]
    pred_class = pred_class[:pred_t+1]

    return pred_boxes, pred_class


def object_detection_api(img_path, threshold=0.5):

    boxes, pred_cls = get_prediction(img_path, threshold) # Get predictions
    img = cv2.imread(img_path) # Read image with cv2
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Convert to RGB

    # about display
    rect_th, text_size, text_th = 3, 2, 2
    bbox_color, txt_color = (0, 0, 255), (0, 255, 0)
    for i in range(len(boxes)):
      cv2.rectangle(img, boxes[i][0], boxes[i][1],color=bbox_color, thickness=rect_th) # Draw Rectangle with the coordinates
      cv2.putText(img,pred_cls[i], boxes[i][0],  cv2.FONT_HERSHEY_SIMPLEX, text_size, txt_color,thickness=text_th) # Write the prediction class

    fig, ax = plt.subplots()
    ax.imshow(img, aspect='equal'); plt.axis('off')
    height, width, channels = img.shape
    fig.set_size_inches(width/100.0/4.0, height/100.0/4.0)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
    plt.margins(0,0)

    # plt.xticks([]); plt.yticks([]); plt.show()
    plt.savefig(os.path.join('dataset/resimgs', img_path.split('/')[-1]), dpi=400); plt.close()

if __name__ == '__main__':

    model = fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()

    img_path = 'dataset/images/car.jpg'
    object_detection_api(img_path, threshold=0.8)