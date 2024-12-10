# Skin Lesion Classification: A Comparative Study

This project aims to classify skin lesions using machine learning techniques. By leveraging the HAM10000 dataset, the study compares the performance of two machine learning algorithms: Convolutional Neural Networks (CNN) and Support Vector Machines (SVM). The goal is to identify the strengths and limitations of each method in the context of medical image classification and to propose a framework that can assist dermatologists in diagnosing skin lesions more effectively.

## Dataset

The HAM10000 dataset comprises dermatoscopic images of skin lesions from seven classes:
- Melanoma (mel)
- Basal cell carcinoma (bcc)
- Benign keratosis-like lesions (bkl)
- Actinic keratoses (akiec)
- Dermatofibroma (df)
- Vascular lesions (vasc)
- Nevus (nv)

### Data Summary:
- **Total Valid Images:** 7103
- **Training Set:** 5682 images
- **Validation Set:** 1421 images

## Methods

### 1. Convolutional Neural Network (CNN)
CNNs are employed for their ability to extract spatial features from images. The architecture includes Conv2D, MaxPooling, Dropout, and Dense layers, optimized with the Adam optimizer.

### 2. Support Vector Machine (SVM)
Features were extracted using a pre-trained VGG16 model, and the resulting feature vectors were classified using SVM with an RBF kernel.

## Results

### CNN:
- **Validation Accuracy:** 71.7%
- **Loss:** 0.7760

### SVM:
- **Validation Accuracy:** 71.0%

  
- **Classification Report:**
          precision    recall  f1-score   support

   akiec       0.29      0.31      0.30        48
     bcc       0.47      0.36      0.41        78
     bkl       0.33      0.42      0.37       136
      df       0.28      0.31      0.29        16
     mel       0.38      0.41      0.40       132
      nv       0.87      0.85      0.86       984
    vasc       0.74      0.52      0.61        27



  
## Technologies Used

- Python
- TensorFlow
- scikit-learn
- VGG16 Pre-trained Model
- HAM10000 Dataset

## How to Run

### Prerequisites
Ensure you have Python 3.x installed and the following dependencies:
- TensorFlow
- scikit-learn
- Pandas
- Matplotlib
- PIL

### Installation
```bash
# Clone the repository
git clone https://github.com/AnnabellAnastasia/Skin-Lesion-Classification.git

# Navigate to the project directory
cd Skin-Lesion-Classification

# Install dependencies
pip install -r requirements.txt


# Train the CNN model
python train_cnn.py

# Train the SVM model
python train_svm.py
# Test the CNN model
python test_cnn.py

# Test the SVM model
python test_svm.py

