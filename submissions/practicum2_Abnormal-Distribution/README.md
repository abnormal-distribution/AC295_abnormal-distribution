# Visual Question Answering by Abnormal Distribution

## Practicum 2


## Eduardo PEYNETTI, Jessica WIJAYA, Rohit BERI, Stuart NEILSON


## Overview
Visual Question Answering comprises of the following parts:

* Model and Utility notebooks in main directory
* Frontend directory for user input
* You can watch a short intro video [here](https://youtu.be/vz57yPF3OcA)
* A presentation deck is available [here](Visual Question Answering.pdf)


## Practicum Memo
* [Link Here](Visual Question Answering.pdf)


## Video Presentation
* [Link Here](https://youtu.be/vz57yPF3OcA)

## Notebooks

## Models:

### BasicModel_Final.ipynb

This notebook implements our baseline baseline model and can be used for training the model. 

### Distilled_Model_Final.ipynb

This notebook is used to distill and train a student model based on the baseline model.

### Pruned_Quantized_Model_Final.ipynb

This notebook implements a pruned and quantized version of our baseline model.

## Utilities:

### Pipeline_Final.ipynb

This notebook implements the pipeline used to convert TFRecords into inputs to our models.

### TFRecords_Final.ipynb

This notebook converts the raw image and text data into a TFRecords format used in our data pipeline

## Frontend

The directory contains 

## How to run the frontend application

### Step 0: Clone repo
* Clone the repo to a local or a virtual machine

### Step 1: Download trained model:

* Download the model from [Google Cloud](https://storage.googleapis.com/practicum2-abnormal-distribution/big2/vqa_model.h5) 
and place it in the frontend directory.

### Step 2: Build docker image
* Execute the below commands on the shell from the following folder ```~/AC295_abnormal-distribution/submissions/practicum2_Abnormal-Distribution/frontend```
```
docker build -t frontend -f Docker_frontend . 
```

### Step 3: Run the container
* Execute the following command:
```
docker run -it -p 8081:8081 frontend 
```
* On your browser, log into address 0.0.0.0:8081

