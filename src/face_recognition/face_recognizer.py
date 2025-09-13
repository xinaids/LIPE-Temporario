#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.append("/src")

import pickle
from collections import Counter
from pathlib import Path
from cv2.typing import MatLike
from src.constants.constants import NAME_UNKNOWN_PLAYER

import face_recognition
import time

class FaceRecognizer:
    def __init__(self, encodings_location: Path):
        """
        Given an unknown image, get the locations and encodings of any faces and
        compares them against the known encodings to find potential matches.
        """
        with encodings_location.open(mode="rb") as f:
            self.loaded_encodings = pickle.load(f)

    def recognize_faces(
        self,
        img: MatLike | str,
        model: str = "hog",
    ) -> str:
        # reconhecimento de imagens salva os captadas
        try:
            if type(img) is str:
                img = face_recognition.load_image_file(img)

            # redimensiona a imagem para melhorar a velocidade
            # small_img = cv2.resize(img, None, fx=0.5, fy=0.5)
            input_face_locations = face_recognition.face_locations(img, model=model)
            
            time.sleep(3)
            
            input_face_encodings = face_recognition.face_encodings(
                img, input_face_locations
            )

            for _, unknown_encoding in zip(input_face_locations, input_face_encodings):
                name = self._recognize_face(unknown_encoding)
                if not name:
                    name = 0
                return name
            
            return 0
        
        except Exception as e:
            print(f"[ERROR] recognize_faces failed: {e}")
            return 0
        

    def _recognize_face(self, unknown_encoding):
        """
        Given an unknown encoding and all known encodings, find the known
        encoding with the most matches.
        """
        boolean_matches = face_recognition.compare_faces(
            self.loaded_encodings["encodings"], unknown_encoding
        )
        votes = Counter(
            name
            for match, name in zip(boolean_matches, self.loaded_encodings["names"])
            if match
        )
        if votes:
            return votes.most_common(1)[0][0]
