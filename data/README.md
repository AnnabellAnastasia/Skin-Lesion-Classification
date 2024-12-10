# Skin Lesion Classification Data

This directory contains the HAM10000 dataset used for training and testing machine learning models for skin lesion classification. The dataset includes dermatoscopic images of skin lesions across seven classes.

## Dataset Overview

The HAM10000 dataset consists of 10,015 dermatoscopic images, with the following key details:

- **Total Images:** 10,015
- **Valid Images (used in this project):** 7,103
- **Classes:**
  - Melanoma (mel)
  - Basal cell carcinoma (bcc)
  - Benign keratosis-like lesions (bkl)
  - Actinic keratoses (akiec)
  - Dermatofibroma (df)
  - Vascular lesions (vasc)
  - Nevus (nv)

## Directory Structure

The data is split into two folders due to storage constraints:


### Files

1. **`HAM10000_images_part_1/`**:
   Contains a subset of images from the dataset.
   
2. **`HAM10000_images_part_2/`**:
   Contains the remaining subset of images.

3. **`HAM10000_metadata.csv`**:
   Metadata file containing image IDs, lesion types, patient information (age, gender, location), and more.

## Metadata Description

The `HAM10000_metadata.csv` file includes the following columns:

| Column        | Description                                          |
| ------------- | ---------------------------------------------------- |
| `lesion_id`   | Unique identifier for the lesion.                   |
| `image_id`    | Unique identifier for the image.                    |
| `dx`          | Lesion type (e.g., `mel`, `bcc`).                   |
| `dx_type`     | Type of diagnosis (e.g., clinical, histopathology). |
| `age`         | Age of the patient (if available).                  |
| `sex`         | Gender of the patient (male/female).                |
| `localization`| Body location of the lesion.                        |

## Notes

- Due to storage limitations, the dataset is not uploaded to the repository. It can be downloaded from [HAM10000 Dataset](https://doi.org/10.7910/DVN/DBW86T).
- To use this data in the project, ensure that the directory structure matches the format described above.
- Images have a uniform size of 600x450 pixels, which simplifies preprocessing.

## How to Use

1. **Download the Dataset:**
   Download the dataset from the https://www.kaggle.com/datasets/kmader/skin-cancer-mnist-ham10000?resource=download.

2. **Organize the Data:**
   Place the image folders and metadata file in the `data/` directory following the structure outlined above.

3. **Verify Data Path:**
   Update the file paths in your codebase to point to the correct data directory.

## Acknowledgments

The HAM10000 dataset is published and maintained by the Medical University of Vienna. It is available under open access for research purposes. Special thanks to the creators for making this valuable dataset publicly available.
