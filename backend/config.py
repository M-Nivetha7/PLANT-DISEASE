import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MODEL_PATH = os.path.join(BASE_DIR, "model/plant_model.h5")
CLASS_INDEX_PATH = os.path.join(BASE_DIR, "model/class_indices.json")

IMG_SIZE = 128