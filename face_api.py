import face_recognition
import os
import io, base64
from PIL import Image
from pathlib import Path
import uuid


class FaceApi:
    root_dir: str
    facesDict = {}
    images_root_folder: str
    images_find_folder: str

    def __init__(self, root_dir: str):
        self.root_dir = root_dir
        self.images_root_folder = os.path.join(self.root_dir, "raw_images")
        self.images_find_folder = os.path.join(self.root_dir, "find_images")
        if not os.path.exists(self.images_root_folder):
            os.mkdir(self.images_root_folder)

        if not os.path.exists(self.images_find_folder):
            os.mkdir(self.images_find_folder)

    def train_from_root(self, face_id: str = None):
        files = os.listdir(self.images_root_folder)
        if face_id is not None:
            files = filter(lambda x: x == face_id + ".jpg", files)

        for file in files:
            image = face_recognition.load_image_file(os.path.join(self.images_root_folder, file))
            self.facesDict[Path(file).stem] = face_recognition.face_encodings(image)

    def add_face(self, face_id: str, image_base64: str):
        img = Image.open(io.BytesIO(base64.decodebytes(bytes(image_base64, "utf-8"))))
        img.save(os.path.join(self.images_root_folder, face_id + ".jpg"))
        self.train_from_root(face_id)

    def delete_face(self, face_id: str):
        self.facesDict.pop(face_id)
        os.remove(os.path.join(self.images_root_folder, face_id + ".jpg"))

    def get_all_faces(self):
        return self.facesDict

    def find_face(self, image_base64: str):

        search_img_encoding = face_recognition.face_encodings(
            face_recognition.load_image_file(
                io.BytesIO(base64.decodebytes(bytes(image_base64, "utf-8")))
            )
        )

        highest_scorer: str = ""
        lowest_score: int = 1000

        for known_faces in os.listdir(self.images_root_folder):
            known_face_encoding = self.facesDict[Path(known_faces).stem]

            face_distances = face_recognition.face_distance(known_face_encoding, search_img_encoding[0])
            score = face_distances[0] * 100
            if score < lowest_score:
                lowest_score = score
                highest_scorer = known_faces

        return {
                "match": Path(highest_scorer).stem,
                "score": lowest_score
        }
