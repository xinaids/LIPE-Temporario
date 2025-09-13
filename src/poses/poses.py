#!/usr/bin/env python
# coding: utf-8

import mediapipe as mp

class Poses:
    def __init__(self):
        # define algumas configurações do mediapipe
        self.mpPose = mp.solutions.pose
        self.mpDraw = mp.solutions.drawing_utils
        self.pose = self.mpPose.Pose(min_tracking_confidence=0.5, min_detection_confidence=0.5)

    