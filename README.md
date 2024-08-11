# Video Crowd Localization with Multi-focus Gaussian Neighborhood Attention and a Large-Scale Benchmark

Haopeng Li, Lingbo Liu, Kunlin Yang, Shinan Liu, Junyu Gao, Bin Zhao, Rui Zhang, and Jun Hou

IEEE Transactions on Image Processing

This repository provides the introduction and access to the VSCrowd dataset proposed in this work ([Paper](https://ieeexplore.ieee.org/abstract/document/9893023)).

## Introduction
VSCrowd consists of 634 videos, 479 for training (`train_XXX`) and 137 for testing (`test_XXX`). For each video, the annotations are saved in the corresponding TXT file (`train_XXX.txt` or `test_XXX.txt`), with the following format: 
```
FrameID HeadID x1 y1 x2 y2 p1 p2 HeadID x1 y1 x2 y2 p1 p2 …
FrameID HeadID x1 y1 x2 y2 p1 p2 HeadID x1 y1 x2 y2 p1 p2 …
...
```
Each line in the TXT file corresponds to the crowd annotations of a specific frame in the video. In each line, `FrameID` is the ID of the frame and the subsequent is the labels of each head. For each head, we have three labels:

`HeadID`: Tracking ID of the head in the video for tracking;

`x1 y1 x2 y2`: Bounding box of the head (left, top, right, bottom) for detection;

`p1 p2`: Center point of the head for crowd counting/localization. 

Example:
```
0001 68 20.44 305.76 51.62 332.67 34.97 317.8 52 263.33 49.63 276.59 65.25 268.29 55.15 … 
0002 76 585.47 286.06 617.74 319.47 607.92 300.67 15 914.84 156.14 934.2 180.47 927.66 164.96 …
...
```

## Visualization

The annotations of four example videos from VSCrowd are visulized as follows (only the first five frames are shown).

![Untitled Diagram](https://user-images.githubusercontent.com/39694692/181676864-3cbf0fd8-90bb-464f-9f1b-8715f2569c46.svg)

## Download
The videos and annotations can be download at [OneDrive](https://unimelbcloud-my.sharepoint.com/:f:/g/personal/haopengl1_student_unimelb_edu_au/ElPHq3MxN-NOo0WFMCPU6VQB8Ia8V9S7u2IdrczBHpDjWQ?e=dFJhdP).

## Format Convert
### yolo format
convert the format to yolo (eg. label cx cy w h ...)

```python
python convert_yolo_format.py
```

## Citation
```
@article{li2022video,
  title={Video Crowd Localization With Multifocus Gaussian Neighborhood Attention and a Large-Scale Benchmark},
  author={Li, Haopeng and Liu, Lingbo and Yang, Kunlin and Liu, Shinan and Gao, Junyu and Zhao, Bin and Zhang, Rui and Hou, Jun},
  journal={IEEE Transactions on Image Processing},
  volume={31},
  pages={6032--6047},
  year={2022},
  publisher={IEEE}
}
```
