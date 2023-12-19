import base64
import io
import json
import os
import uuid
from pathlib import Path
import logging
import face_recognition
from PIL import Image
import boto3
from botocore.exceptions import ClientError
from recognition_objects import RekognitionFace, RekognitionPerson

logger = logging.getLogger(__name__)


class FaceApi:
    root_dir: str
    face_dict = {}
    images_root_folder: str
    images_find_folder: str

    def __init__(self, root_dir: str):
        self.rekognition_client = boto3.client('rekognition')
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
        count = 1
        s_image = os.path.join(self.images_find_folder, "Gaurav.jpg")
        for file in files:
            _id = Path(file).stem
            print(f"learning {count} of {len(files)} - {_id}")
            count = count + 1

    def add_face(self, face_id: str, image_base64: str):
        img = Image.open(io.BytesIO(base64.decodebytes(bytes(image_base64, "utf-8"))))
        img.save(os.path.join(self.images_root_folder, face_id + ".jpg"))
        self.train_from_root(face_id)

    def delete_face(self, face_id: str):
        self.face_dict.pop(face_id)
        os.remove(os.path.join(self.images_root_folder, face_id + ".jpg"))

    def get_all_faces(self):
        return self.face_dict

    def find_face(self, image_base64: str):
        _id = str(uuid.uuid1())
        _temp_path = os.path.join(self.images_find_folder, _id + ".jpg")
        img = Image.open(io.BytesIO(base64.decodebytes(bytes(image_base64, "utf-8"))))
        img.save(_temp_path)

        for known_faces in os.listdir(self.images_root_folder):
            result = self.compare_faces(_temp_path, os.path.join(self.images_root_folder, known_faces))
            if result is True:
                return {
                    "match": Path(known_faces).stem,
                    "score": 100
                }

        return {
            "match": "NO MATCH",
            "score": 0
        }

    def compare_faces(self, source_image: str, target_image: str):

        try:
            with open(source_image, 'rb') as image_source:
                with open(target_image, 'rb') as image_target:
                    response = self.rekognition_client.compare_faces(
                        SourceImage={'Bytes': image_source.read()},
                        TargetImage={'Bytes': image_target.read()},
                        SimilarityThreshold=80,
                    )
                    matches = [
                        RekognitionFace(match["Face"]) for match in response["FaceMatches"]
                    ]
                    unmatches = [RekognitionFace(face) for face in response["UnmatchedFaces"]]
                    if len(matches) > 0:
                        return True

        except ClientError:
            return False
