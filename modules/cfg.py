#!/usr/bin/env python3
# -*- coding: utf-8 -*-

RPN_CFG = {
    'pre_nms_top_n_train'  : 2000,
    'pre_nms_top_n_test'   : 1000,
    'post_nms_top_n_train' : 2000,
    'post_nms_top_n_test'  : 1000,
    'nms_thresh'           : 0.7,
    'fg_iou_thresh'        : 0.7,
    'bg_iou_thresh'        : 0.3,
    'batch_size_per_image' : 256,
    'positive_fraction'    : 0.5,
    'aspect_ratio'         : ((0.5, 1.0, 2.0),),
    'anchor_sizes'         : ((32,), (64,), (128,), (256,), (512,)),
}

RoI_CFG = {
    'score_thresh'         : 0.05,
    'nms_thresh'           : 0.5,
    'detections_per_img'   : 100,
    'fg_iou_thresh'        : 0.5,   # BUG
    'bg_iou_thresh'        : 0.5,
    'batch_size_per_image' : 512,    # Core
    'positive_fraction'    : 0.25,
    'reg_weights'          : (10., 10., 5., 5.), # TODO
    'featmap_names'        : [0, 1, 2, 3],       # according to backbone
    'representation_size'  : 1024,               # TODO
    'mask_layers'          : (256, 256, 256, 256),
    'mask_pred_in_channels': 256,
    'mask_dim_reduced'     : 256,
    'mask_dilation'        : 1,
    'output_size'          : 7,
    'mask_o_size'          : 14,
    'sampling_ratio'       : 2,
}

TRANS_CFG = {
    'min_size' : 800,        # short-side
    'max_size' : 1333,       # long-side
    'img_mean' : [0.485, 0.456, 0.406],
    'img_std'  : [0.229, 0.224, 0.225],
}
