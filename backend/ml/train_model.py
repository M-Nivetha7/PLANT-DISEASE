import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from config import IMG_SIZE

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "dataset")
MODEL_DIR = os.path.join(BASE_DIR, "model")
os.makedirs(MODEL_DIR, exist_ok=True)

IMG_SIZE = getattr(__import__('config'), 'IMG_SIZE', IMG_SIZE)
BATCH_SIZE = 32
EPOCHS = 5

if not os.path.exists(DATA_DIR):
    raise RuntimeError(f"Dataset directory not found: {DATA_DIR}")

datagen = ImageDataGenerator(validation_split=0.2, rescale=1.0/255.0,
                             rotation_range=20, width_shift_range=0.1,
                             height_shift_range=0.1, shear_range=0.1,
                             zoom_range=0.1, horizontal_flip=True)

train_gen = datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    subset="training",
    class_mode='binary'
)

val_gen = datagen.flow_from_directory(
    DATA_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    subset="validation",
    class_mode='binary'
)

# Build model (MobileNetV2 base)
base_model = MobileNetV2(input_shape=(IMG_SIZE, IMG_SIZE, 3), include_top=False, weights='imagenet')
base_model.trainable = False

model = models.Sequential([
    base_model,
    layers.GlobalAveragePooling2D(),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.4),
    layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

history = model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS)

model_path = os.path.join(MODEL_DIR, "plant_model.h5")
model.save(model_path)

# Save class indices mapping
class_indices = train_gen.class_indices  # e.g. {'Healthy': 0, 'diseased': 1}
with open(os.path.join(MODEL_DIR, "class_indices.json"), 'w') as f:
    json.dump(class_indices, f)

print("Saved model to:", model_path)
print("Class indices:", class_indices)
print("Final training accuracy:", history.history.get('accuracy', [None])[-1])