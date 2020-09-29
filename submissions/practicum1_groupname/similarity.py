import numpy as np
import pandas as pd

from PIL import Image
from glob import glob
from joblib import Parallel, delayed


PATH_IMAGES = "/Users/rberi/Google Drive (Stanford GSB)/EdX & Coursera/HarvardX/Advanced Practical Data Science/AC295_abnormal-distribution/data/gap_images/gap_"
PATH_IMAGES_RESIZE_COLOR = "/Users/rberi/Google Drive (Stanford GSB)/EdX & Coursera/HarvardX/Advanced Practical Data Science/AC295_abnormal-distribution/data/color_resize/col_"
PATH_IMAGES_RESIZE_BW = "/Users/rberi/Google Drive (Stanford GSB)/EdX & Coursera/HarvardX/Advanced Practical Data Science/AC295_abnormal-distribution/data/bw_resize/bw_"
PATH_RESIZED_LIST = "/Users/rberi/Google Drive (Stanford GSB)/EdX & Coursera/HarvardX/Advanced Practical Data Science/AC295_abnormal-distribution/data/resized_list.csv"


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


def resize_image(img, size, save=False):
    """This functions reads the image files and calls the color and grayscale resizing."""
    
    image = Image.open(PATH_IMAGES+img+".jpg")
    img_col = resize_color(image, size, img, save)
    img_bw = resize_bw(image, size, img, save)
    
    if save:
        with open(PATH_RESIZED_LIST, "a") as f:
            f.write(img+'\n')
        return
    else:
        return img_bw, img_col


if __name__ == '__main__':
    resize_library()
