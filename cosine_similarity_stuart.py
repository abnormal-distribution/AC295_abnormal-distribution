# calculates cosine similarity of images

import numpy as np
import pandas as pd
# pip install opencv-python to get cv2
import cv2
import matplotlib.pyplot as plt
import dask.array as da

# numpy arrays as inputs - can be any shape but have to be the same shape as each other
def cosine_similarity(img1,img2):
    return np.sum(np.multiply(img1,img2))/(np.sqrt(np.sum(np.multiply(img1,img1)))*np.sqrt(np.sum(np.multiply(img2,img2)))) 

# dask inputs
def cosine_similarity_dask(img1,img2):
    return da.sum(da.multiply(img1,img2))/(da.sqrt(da.sum(da.multiply(img1,img1)))*da.sqrt(da.sum(da.multiply(img2,img2)))) 

size_spec = [32,32,3]

# function that returns the ID of the image with the highest similarity
# arguments are:
#   the input image as jpg
#   pandas dataframe with list of IDs and filenames referring to the list of all images
#   folder path where comparison images are located 
def pick_similar_image(input_img,image_list_frame,image_folder):
    max_sim = 0
    for i in range(len(image_list_frame)):
        img_compare = cv2.resize(cv2.cvtColor(cv2.imread(image_folder + image_list_frame['file_id'][i]), cv2.COLOR_RGB2BGR), (size_spec[0], size_spec[1]))
        similarity = cosine_similarity(input_img.astype('double'),img_compare.astype('double'))
        if similarity >= max_sim:
            best_image_id = image_list_frame['id'][i]
            max_sim = similarity 
    return best_image_id

# running an example

meta = pd.read_csv('gap_images/metadata.csv')

meta['id'] = meta['file_id'].str.slice(4,9)
file_key = meta[['id','file_id']]

# we would eventually have this as a database table
file_key_short = file_key[:10]

print(file_key_short)

image_folder = 'gap_images/gap_images/'

input_img = cv2.resize(cv2.cvtColor(cv2.imread(image_folder + 'gap_11144.jpg'), cv2.COLOR_RGB2BGR),(size_spec[0],size_spec[1]))
input_img2 = cv2.resize(cv2.cvtColor(cv2.imread(image_folder + 'gap_11155.jpg'), cv2.COLOR_RGB2BGR),(size_spec[0],size_spec[1]))


print(pick_similar_image(input_img,file_key_short,image_folder))
    
input_img_dask = da.from_array(input_img.astype('double'),chunks=1000)
input_img2_dask = da.from_array(input_img2.astype('double'),chunks=1000)    

print(cosine_similarity(input_img.astype('double'),input_img2.astype('double')))
print(cosine_similarity_dask(input_img_dask,input_img2_dask).compute())