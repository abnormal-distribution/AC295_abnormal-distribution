import pickle
import numpy as np
import pandas as pd

from PIL import Image
from glob import glob
from joblib import Parallel, delayed
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA

from tensorflow.keras.models import Model
from keras import backend as K
from tensorflow.keras.models import load_model


PATH_IMAGES = "image-data/gap_images/gap_"
PATH_IMAGES_RESIZE_BW = "resize-data/bw_resize/"
PATH_IMAGES_RESIZE_COL = "resize-data/col_resize/"
PATH_RESIZED_LIST = "resize-data/resized_list.csv"
PATH_PCA_ARRAY = "resize-data/PCA_images_128.npy"
PATH_PCA_MODEL = "resize-data/PCA_model_128.sav"
PATH_ENCODER_MODEL = "resize-data/conv_encoder.h5"
PATH_ENCODED_IMAGES = "resize-data/conv_encoding.npy"

"""
PATH_IMAGES = "/Users/rberi/Google Drive (Stanford GSB)/EdX & Coursera/HarvardX/Advanced Practical Data Science/AC295_abnormal-distribution/submissions/practicum1_groupname/image-data/gap_images/gap_"
PATH_IMAGES_RESIZE_BW = "/Users/rberi/Google Drive (Stanford GSB)/EdX & Coursera/HarvardX/Advanced Practical Data Science/AC295_abnormal-distribution/submissions/practicum1_groupname/resize-data/bw_resize/"
PATH_RESIZED_LIST = "/Users/rberi/Google Drive (Stanford GSB)/EdX & Coursera/HarvardX/Advanced Practical Data Science/AC295_abnormal-distribution/submissions/practicum1_groupname/resize-data/resized_list.csv"
PATH_PCA_ARRAY = "/Users/rberi/Google Drive (Stanford GSB)/EdX & Coursera/HarvardX/Advanced Practical Data Science/AC295_abnormal-distribution/submissions/practicum1_groupname/resize-data/PCA_images_128.npy"
PATH_PCA_MODEL = "/Users/rberi/Google Drive (Stanford GSB)/EdX & Coursera/HarvardX/Advanced Practical Data Science/AC295_abnormal-distribution/submissions/practicum1_groupname/resize-data/PCA_model_128.sav"
"""


N_COMPONENTS = 128
SIZE = 128, 128


def resize_library(size=SIZE):
    """This function resizes existing library of images"""
    
    filenames = glob(PATH_IMAGES + "*.jpg")
    filenames = [filename.replace(PATH_IMAGES, "").replace(".jpg", "") for filename in filenames]
    filenames = set(filenames)
    
    try:
        resized_list = pd.read_csv(PATH_RESIZED_LIST, dtype=str)
        filenames = set(filenames) - set(resized_list[resized_list.columns[0]])
        del resized_list
    except:
        pass
    
    Parallel(n_jobs=-1)(delayed(resize_image)(file, size, save=True) for file in filenames)
    
    return True


def resize_color(image_in, size, img, save=False):
    """This functions re-sizes a color image into new size"""

    channels = len(image_in.getbands())
    
    if channels < 3:
        return None
    
    image = image_in.convert('RGB').resize(size)
    
    if save:
        image.save(PATH_IMAGES_RESIZE_COL + img + '.jpg')
        return None
    else:
        return image


def resize_bw(image_in, size, img=None, save=False):
    """This functions re-sizes a color/grayscale image into new size and grayscale"""

    image = image_in.convert('L').resize(size)

    if save:
        image.save(PATH_IMAGES_RESIZE_BW + img + '.jpg')
        return None
    else:
        return image


def resize_image(img, size=SIZE, save=False):
    """This functions reads the image files and calls the color and grayscale resizing."""
    
    image = Image.open(PATH_IMAGES + img + ".jpg")
    #img_col = resize_color(image, size, img, save)
    img_bw = resize_bw(image, size, img, save)
    
    if save:
        with open(PATH_RESIZED_LIST, "a") as f:
            f.write(img+'\n')
        return
    else:
        return img_bw #, img_col


def compute_library_latent_space():
    """This functions reads the image files and converts them into latent space."""
    
    try:
        f = open(PATH_PCA_MODEL, 'rb')
        f.close()
        
    except FileNotFoundError:
        pca = PCA(n_components=N_COMPONENTS)
        
        images = []
        
        filename = sorted(glob(PATH_IMAGES_RESIZE_BW + "*.jpg"))
        for file in filename:
            img = np.asarray(Image.open(file)).reshape(-1)
            images.append(img)
        
        images = np.array(images)
        images = pca.fit_transform(images)
        
        
        np.save(PATH_PCA_ARRAY, images)
        pickle.dump(pca, open(PATH_PCA_MODEL, 'wb'))
    

def cosine_dist(image):
    """This functions computes cosine similarity between images in the database and the image provided by the user"""

    conv_encoder = load_model(PATH_ENCODER_MODEL)
    
    img_bw = resize_bw(image, size=SIZE)
    img_bw = np.asarray(img_bw).reshape((SIZE[0], SIZE[1], 1))
    pred = conv_encoder.predict(img_bw.reshape([1,SIZE[0],SIZE[1],1]) / 255.)
    
    df_bw = np.load(PATH_ENCODED_IMAGES)

    df_bw_flat = df_bw.reshape(9294,-1)
    pred_flat = pred.reshape(1,-1)
    
    bw_cos_sim = cosine_similarity(df_bw_flat, pred_flat)
    id = bw_cos_sim.argmax()
    
    filename = sorted(glob(PATH_IMAGES_RESIZE_BW + "*.jpg"))
    filename = filename[id].replace(PATH_IMAGES_RESIZE_BW, "").replace(".jpg", "")
    
    return filename
    

if __name__ == '__main__':
    resize_library()
    print("Resize Done\n")
    
    compute_library_latent_space()
    print("Latent Space Calculated\n")
    
    filename = glob(PATH_IMAGES + "*.jpg")
    filename = filename[np.random.randint(len(filename))]
    
    image = Image.open(filename)
    
    filename = filename.replace(PATH_IMAGES, "").replace(".jpg", "")
    print("File name given   :", filename)
    
    print("Predicted Filename:", cosine_dist(image))
