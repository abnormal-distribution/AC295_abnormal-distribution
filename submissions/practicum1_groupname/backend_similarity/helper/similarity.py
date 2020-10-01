import numpy as np
import pandas as pd
import dask_image.imread as di
import dask.array as da

from PIL import Image
from glob import glob
from joblib import Parallel, delayed
from dask_distance import cosine


PATH_IMAGES = "image-data/gap_"
PATH_IMAGES_RESIZE_BW = "resize-data/"
PATH_RESIZED_LIST = "resize-data/resized_list.csv"


SIZE = 32, 32


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
        image.save(PATH_IMAGES_RESIZE_COLOR + img + '.jpg')
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


def cosine_similarity(image):
    """This functions computes cosine similarity between images in the database and the image provided by the user"""
    
    img_bw = resize_image(image, size=SIZE)
    
    df_bw = di.imread(PATH_IMAGES_RESIZE_BW + '*.jpg').reshape(-1, SIZE[0] * SIZE[1])
    img_bw = np.asarray(img_bw).reshape(1, (SIZE[0] * SIZE[1]))
    
    bw_cos_sim = da.apply_along_axis(cosine, 1, df_bw, img_bw)
    id = bw_cos_sim.argmin()

    """
    id, val = bw_cos_sim.argmin(), bw_cos_sim.min()
    
    if img_col:
        df_col = di.imread(PATH_IMAGES_RESIZE_COLOR + '*.jpg').reshape(-1, SIZE[0] * SIZE[1] * 3)
        img_col = np.asarray(img_col).reshape(1, (SIZE[0] * SIZE[1] * 3))

        col_cos_sim = da.apply_along_axis(cosine, 1, df_col, img_col)
        id2, val2 = col_cos_sim.argmin(), col_cos_sim.min()
        
        id = id if val < val2 else id2
    """
    
    filenames = sorted(glob(PATH_IMAGES_RESIZE_BW + "*.jpg"))
    
    return filenames[id.compute()].replace(PATH_IMAGES_RESIZE_BW, "").replace(".jpg", "")
    


if __name__ == '__main__':
    resize_library()
    print("Resize Done")
    filename = glob(PATH_IMAGES + "11112.jpg")
    filename = filename[np.random.randint(len(filename))].replace(PATH_IMAGES, "").replace(".jpg", "")
    
    print(cosine_similarity(filename))
