# -*- coding: utf-8 -*-
"""Skin_Mole_CNN.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Leiruf71I-3B7IHcum0hQxQKrVIehWxf
"""

import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from PIL import Image
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Ensure TensorFlow Version
#!pip install --upgrade tensorflow
#assert tf.__version__ >= "2.18.0", "TensorFlow version must be 2.8.0 or higher."

# Set default font sizes for matplotlib
plt.rc('font', size=14)
plt.rc('axes', labelsize=14, titlesize=14)
plt.rc('legend', fontsize=14)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

# Load metadata
metadata = pd.read_csv("/content/drive/My Drive/images/HAM10000_metadata.csv")

# Define paths to the two image directories
image_dir_part1 = "/content/drive/My Drive/images/HAM10000_images_part_1"
image_dir_part2 = "/content/drive/My Drive/images/HAM10000_images_part_2"

# Add 'image_path' column
metadata["image_path"] = metadata["image_id"].apply(
    lambda x: os.path.join(image_dir_part1, f"{x}.jpg")
    if os.path.exists(os.path.join(image_dir_part1, f"{x}.jpg"))
    else os.path.join(image_dir_part2, f"{x}.jpg")
)

# Filter rows with missing image files
metadata = metadata[metadata["image_path"].apply(os.path.exists)]
print(f"Number of valid images: {len(metadata)}")

# Split metadata into training and validation sets
train_df = metadata.sample(frac=0.8, random_state=42)  # 80% training data
val_df = metadata.drop(train_df.index)  # Use the remaining rows for validation

# Reset the indices for both DataFrames after splitting
train_df = train_df.reset_index(drop=True)
val_df = val_df.reset_index(drop=True)

# Verify the split
print(f"Training set: {len(train_df)} images")
print(f"Validation set: {len(val_df)} images")

# Visualization - Class Distribution
metadata["dx"].value_counts().plot(kind='bar', title='Class Distribution')
plt.show()

# Display sample images by class
classes = metadata["dx"].unique()
plt.figure(figsize=(15, 10))
for i, cls in enumerate(classes):
    sample = metadata[metadata["dx"] == cls].iloc[0]["image_path"]
    img = mpimg.imread(sample)
    plt.subplot(3, 3, i + 1)
    plt.imshow(img)
    plt.title(cls)
    plt.axis("off")
plt.tight_layout()
plt.show()

# Image Size Distribution
sizes = [Image.open(path).size for path in metadata["image_path"][:1000]]
widths, heights = zip(*sizes)
plt.hist(widths, bins=20, alpha=0.5, label="Width")
plt.hist(heights, bins=20, alpha=0.5, label="Height")
plt.legend()
plt.title("Image Dimensions Distribution (Sampled)")
plt.show()

# Data Augmentation and Normalization
train_datagen = ImageDataGenerator(
    rescale=1.0/255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
val_datagen = ImageDataGenerator(rescale=1.0/255)

# Create Data Generators
train_generator = train_datagen.flow_from_dataframe(
    dataframe=train_df,
    x_col="image_path",
    y_col="dx",
    target_size=(128, 128),
    batch_size=32,
    class_mode="categorical"
)
val_generator = val_datagen.flow_from_dataframe(
    dataframe=val_df,
    x_col="image_path",
    y_col="dx",
    target_size=(128, 128),
    batch_size=32,
    class_mode="categorical"
)

# Verify Data Generators
x_batch, y_batch = next(train_generator)
print(f"Image batch shape: {x_batch.shape}")
print(f"Label batch shape: {y_batch.shape}")

# Display the first image from the batch
plt.imshow(x_batch[0])
plt.axis('off')
plt.title("Sample Image")
plt.show()

"""# **CNN Architecture**"""

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(len(train_generator.class_indices), activation='softmax')
])
model.summary()

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(
    train_generator,
    validation_data=val_generator,
    epochs=20,  # Start with 10-20 epochs
    verbose=1
)

plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.title('Training and Validation Accuracy')
plt.legend()
plt.show()

plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Training and Validation Loss')
plt.legend()
plt.show()

val_loss, val_acc = model.evaluate(val_generator)
print(f"Validation Loss: {val_loss}")
print(f"Validation Accuracy: {val_acc}")

model.save('skin_mole_cnn_model.h5')

model.save('/content/drive/My Drive/my_model.keras')  # Save in your Google Drive

from sklearn.svm import SVC
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

# Load the pretrained CNN (VGG16 without top layers for feature extraction)
vgg_model = VGG16(weights='imagenet', include_top=False, input_shape=(128, 128, 3))

# Data generator for feature extraction
datagen = ImageDataGenerator(rescale=1.0/255)

# Extract features for training set
train_generator = datagen.flow_from_dataframe(
    dataframe=train_df,
    x_col="image_path",
    y_col="dx",
    target_size=(128, 128),
    batch_size=32,
    class_mode=None,
    shuffle=False  # Ensure the order matches labels
)

train_features = vgg_model.predict(train_generator)
train_features = train_features.reshape(train_features.shape[0], -1)  # Flatten features

# Extract features for validation set
val_generator = datagen.flow_from_dataframe(
    dataframe=val_df,
    x_col="image_path",
    y_col="dx",
    target_size=(128, 128),
    batch_size=32,
    class_mode=None,
    shuffle=False
)

val_features = vgg_model.predict(val_generator)
val_features = val_features.reshape(val_features.shape[0], -1)  # Flatten features

# Encode labels into numerical format
label_encoder = LabelEncoder()
train_labels = label_encoder.fit_transform(train_df["dx"])
val_labels = label_encoder.transform(val_df["dx"])

# Normalize features
scaler = StandardScaler()
train_features = scaler.fit_transform(train_features)
val_features = scaler.transform(val_features)

# Train the SVM classifier
svm = SVC(kernel='linear', probability=True)  # Use linear kernel
svm.fit(train_features, train_labels)

# Make predictions
val_predictions = svm.predict(val_features)

# Evaluate the model
print("SVM Classification Report:")
print(classification_report(val_labels, val_predictions, target_names=label_encoder.classes_))

# Calculate accuracy
val_accuracy = accuracy_score(val_labels, val_predictions)
print(f"Validation Accuracy: {val_accuracy:.2f}")