import cv2
import mediapipe as mp
from cv2.typing import MatLike


def detect_hand_like(img: MatLike, limiar_thumb=0.25):
    mp_hands = mp.solutions.hands

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:

        image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        if not results.multi_hand_landmarks:
            return False

        for hand_landmarks in results.multi_hand_landmarks:
            thumb_top = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
            thumb_base = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC].y

            fingers_raised = 0
            for i in [
                mp_hands.HandLandmark.INDEX_FINGER_TIP,
                mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
                mp_hands.HandLandmark.RING_FINGER_TIP,
                mp_hands.HandLandmark.PINKY_TIP,
            ]:
                if hand_landmarks.landmark[i].y < thumb_top:
                    fingers_raised += 1

            if thumb_base - thumb_top > limiar_thumb and fingers_raised == 0:
                return True

    return False
