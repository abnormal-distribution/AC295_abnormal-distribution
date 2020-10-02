import pickle
import numpy as np
import pandas as pd
import dask_image.imread as di
import dask.array as da

from PIL import Image
from glob import glob
from joblib import Parallel, delayed
from sklearn.metrics.pairwise import cosine_similarity
from dask_ml.decomposition import PCA


"""
PATH_IMAGES = "image-data/gap_images/gap_"
PATH_IMAGES_RESIZE_BW = "resize-data/bw_resize/"
PATH_RESIZED_LIST = "resize-data/resized_list.csv"
PATH_PCA_ARRAY = "resize-data/PCA_array"
PATH_TEMP = "resize-data"
"""

PATH_IMAGES = "../../data/gap_images/gap_"
PATH_IMAGES_RESIZE_BW = "../../backend_similarity/data/bw_resize/"
PATH_IMAGES_RESIZE_COL = "../../backend_similarity/data/col_resize/"
PATH_RESIZED_LIST = "../../backend_similarity/data/resized_list.csv"
PATH_PCA_ARRAY = "../../backend_similarity/data/PCA_array"
PATH_PCA_MODEL = "../../backend_similarity/data/PCA_model_64.sav"


N_COMPONENTS = 64
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
    
    Parallel(n_jobs=-1)(delayed(resize_image)(filename, size, save=True) for filename in filenames)
    
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


def resize_bw(image_in, size, img, save=False):
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
        
        df_bw = di.imread(PATH_IMAGES_RESIZE_BW + '*.jpg').reshape(-1, SIZE[0] * SIZE[1])
        df_bw = pca.fit_transform(df_bw)
        
        da.to_npy_stack(PATH_PCA_ARRAY, df_bw)
        pickle.dump(pca, open(PATH_PCA_MODEL, 'wb'))
    

def cosine_dist(image):
    """This functions computes cosine similarity between images in the database and the image provided by the user"""

    f = open(PATH_PCA_MODEL, 'rb')
    pca = pickle.load(f)
    f.close()
    
    img_bw = resize_image(image, size=SIZE)
    img_bw = np.asarray(img_bw).reshape(1, (SIZE[0] * SIZE[1]))
    img_bw = pca.transform(img_bw).reshape(1, -1)
    
    df_bw = da.from_npy_stack(PATH_PCA_ARRAY, mmap_mode='r')
    bw_cos_sim = cosine_similarity(df_bw, img_bw)
    id = bw_cos_sim.argmax()
    
    filenames = sorted(glob(PATH_IMAGES_RESIZE_BW + "*.jpg"))
    print("at the last step")
    return filenames[id].replace(PATH_IMAGES_RESIZE_BW, "").replace(".jpg", "")
    


if __name__ == '__main__':
    resize_library()
    print("Resize Done")
    
    compute_library_latent_space()
    print("Latent Space Calculated")
    
    filename = glob(PATH_IMAGES + "11112.jpg")
    filename = filename[np.random.randint(len(filename))].replace(PATH_IMAGES, "").replace(".jpg", "")
    
    print(cosine_dist(filename))
