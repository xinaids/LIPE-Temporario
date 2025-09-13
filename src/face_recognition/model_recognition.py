import argparse
import pickle
from pathlib import Path
import cv2
from src.face_recognition.face_recognizer import FaceRecognizer
from src.globals.variables import Loading_Counter
import os
from threading import Lock
from src.constants.constants import NUM_IMAGES_USE_TRAINING
import face_recognition
import sys

sys.path.append(".")

DEFAULT_ENCODINGS_PATH = Path("output" + os.sep + "encodings.pkl")

PATH_TRAINING = "PlayerImages"
PATH_OUTPUT = "output"
PATH_VALIDATION = "images" + os.sep + "faces" + os.sep + "validation"


# Create directories if they don't already exist
Path(PATH_TRAINING).mkdir(exist_ok=True)
Path(PATH_OUTPUT).mkdir(exist_ok=True)
Path(PATH_VALIDATION).mkdir(exist_ok=True)

parser = argparse.ArgumentParser(description="Recognize faces in an image")
parser.add_argument("--train", action="store_true", help="Train on input data")
parser.add_argument("--validate", action="store_true", help="Validate trained model")
parser.add_argument(
    "--test", action="store_true", help="Test the model with an unknown image"
)
parser.add_argument(
    "-m",
    action="store",
    default="hog",
    choices=["hog", "cnn"],
    help="Which model to use for training: hog (CPU), cnn (GPU)",
)
parser.add_argument("-f", action="store", help="Path to an image with an unknown face")
args = parser.parse_args()


def encode_known_faces(shared_loading_counter = 0, lock =  None,
    model: str = "hog", encodings_location: Path = DEFAULT_ENCODINGS_PATH, 
) -> None:
    
    lock = Lock()

    players_count = 1
    total_players = len(list(Path(PATH_TRAINING).iterdir()))

    names = []
    encodings = []

    for subdir in Path(PATH_TRAINING).iterdir():
        if subdir.is_dir(): 
            for num_of_picture, filepath in enumerate(subdir.glob("*.*")): 
                image = face_recognition.load_image_file(filepath)

                face_locations = face_recognition.face_locations(image, model=model)
                face_encodings = face_recognition.face_encodings(image, face_locations)

                for encoding in face_encodings:
                    names.append(subdir.name)
                    encodings.append(encoding)
                    
                if num_of_picture >= NUM_IMAGES_USE_TRAINING - 1:
                    break

        if not lock is None:
            with lock:
                shared_loading_counter.value = round(players_count / total_players * 100, 1)
        players_count += 1
        
    name_encodings = {"names": names, "encodings": encodings}
    with encodings_location.open(mode="wb") as f:
        pickle.dump(name_encodings, f)


def validate(model: str = "hog"):
    """
    Runs recognize_faces on a set of images with known faces to validate
    known encodings.
    """
    my_face_recognizer = FaceRecognizer(encodings_location=DEFAULT_ENCODINGS_PATH)
    for filepath in Path(PATH_VALIDATION).rglob("*"):
        if filepath.is_file():
            my_face_recognizer.recognize_faces(
                img=str(filepath.absolute()), model=model
            )


if __name__ == "__main__":
    if args.train:
        encode_known_faces(model=args.m)
    if args.validate:
        validate(model=args.m)
    if args.test:
        video = cv2.VideoCapture(0)  # lê da webcam
        check, img = video.read()  # lê o vídeo
        my_face_recognizer = FaceRecognizer(encodings_location=DEFAULT_ENCODINGS_PATH)
        my_face_recognizer.recognize_faces(img=img, model=args.m)
        video.release()
        cv2.destroyAllWindows()
