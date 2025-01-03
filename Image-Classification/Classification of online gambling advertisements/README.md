# Online Gambling Advertisement Classification Using ResNet-50V2

## Background
Digital advertising has become an effective marketing strategy, with images and videos grabbing users' attention. However, the rise of online gambling advertisements has raised concerns due to the ease of access through smartphones and the internet. This has led to significant financial losses, with around 157 million online gambling transactions and a total turnover of IDR 190 trillion from 2017-2022. The increase in gambling-related activities presents a growing social and mental health risk.

## Problem
Online gambling advertisements can encourage harmful behaviors, such as gambling addiction. These ads often promise quick financial gains, which can lead people to engage in gambling activities, impacting their social, financial, and mental well-being.

## Solution
This study proposes a solution through an image classification model using Convolutional Neural Networks (CNN), specifically the Residual Network (ResNet-50V2). This model aims to automatically classify whether an advertisement is related to online gambling or not.

## Dataset
The dataset consists of 1,221 images, collected through Google and Bing Image search. The dataset is split into three categories:
- Online Gambling Ads: 625 images
- Non-Gambling Ads: 596 images

The dataset is further divided into:
- Training: 867 images (70%)
- Validation: 309 images (25%)
- Testing: 61 images (5%)

Preview Dataset

![image](https://github.com/user-attachments/assets/1d9e762c-4e8b-40a6-85ba-5241b8661159)


## Model Architecture
The model uses ResNet-50V2 as a backbone for feature extraction, with additional layers added for fully connected layers, including dropout and ReLU activation. For binary classification, the final dense layer has one unit with a sigmoid activation function.

![image](https://github.com/user-attachments/assets/6ff3091a-6698-45f1-8962-42fe5d856d63)


## Preprocessing
Data augmentation is applied during training using the TensorFlow `ImageDataGenerator` function, which includes:
- Rescaling to a range between 0 and 1
- Random rotations (up to 20 degrees)
- Horizontal flips
- Nearest-fill mode

## Model Training
- **Transfer Learning**: The model uses a pre-trained ResNet-50 model and fine-tunes it with the custom dataset.
- **Input Shape**: The image dimensions are resized to 150x200.
- **Optimizer**: Adam optimizer is used.
- **Callback**: Training stops when the accuracy reaches 0.95 and the loss reaches below 0.1.

## Evaluation
Evaluation metrics used in this study:
- **Accuracy**: Overall performance of the model.
- **Confusion Matrix**: Provides detailed information on True Positives (TP), True Negatives (TN), False Positives (FP), and False Negatives (FN).

## Experiment Setup

![image](https://github.com/user-attachments/assets/472fe009-5e8d-466b-af2d-76a33d8e6c65)

Hyperparameters tuned during training:
- Learning Rate
- Batch Size
- Epoch Count

## Results

![image](https://github.com/user-attachments/assets/8a66ab70-4cde-44b4-b701-493d346e78a0)

- The best model, from several experiments, achieved the highest accuracy and lowest loss.

![image](https://github.com/user-attachments/assets/4cab4f4a-7990-4073-85e0-c5276cf7543d)

- **Confusion Matrix**: The model showed consistent results in identifying true positives (TP) and false positives (FP). However, False Negatives (FN) indicate the model's inability to detect some positive samples.
