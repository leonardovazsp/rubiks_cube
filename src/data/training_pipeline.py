from tabnanny import verbose
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
import random
from scipy import ndimage
import copy

def augmentation(img,
                 brightness_range=(0.8, 1.2),
                 rotation_range=(-20, 20),
                 crop_ratio=0.8
                 ):
    '''
    Augments an image by rotating it, changing its brightness and cropping at certain range.
    
    Args:
        img: numpy array containing the image.
        brightness_range: tuple containing the range of scalability of brightness.
        rotation_range: tuple containing the range of rotation in degrees.
        crop_ratio: float that determines the ratio between cropped image and original image along dimension 0.
        
    Returns:
        tensorflow tensor of augmented image
    '''
    angle = random.randint(*rotation_range)
    img = ndimage.rotate(img, angle, reshape=False)
    win_size = int(img.shape[0]*crop_ratio)
    x0_min = 0
    x0_max = img.shape[0] - win_size
    y0_min = (img.shape[1] - img.shape[0])//2
    y0_max = img.shape[1] - win_size - y0_min
    x = random.randint(x0_min, x0_max)
    y = random.randint(y0_min, y0_max)
    brightness = random.uniform(*brightness_range)
    img = img[x:x+win_size, y:y+win_size]*brightness
    
    return tf.clip_by_value(img, 0, 1)

def create_dataset(directory_path, training_size=0.9, verbose=True):
    filelist = []
    for file in os.listdir(directory_path):
        if (file.endswith('.jpg') & file[-10:-6].isnumeric()):
            filepath = os.path.join(directory_path, file)
            filelist.append(filepath[:])
    image_count = len(filelist)
    train_size = int(image_count * training_size)
    train_ds = filelist[:train_size]
    train_ds = tf.data.Dataset.list_files(train_ds, shuffle=False)
    train_ds = train_ds.shuffle(train_size, reshuffle_each_iteration=False)
    val_ds = filelist[train_size:]
    val_ds = tf.data.Dataset.list_files(val_ds, shuffle=False)
    val_ds = val_ds.shuffle(image_count-train_size, reshuffle_each_iteration=False)
    if verbose:
        print(f'Training size: {tf.data.experimental.cardinality(train_ds).numpy()}')
        print(f'Validation size: {tf.data.experimental.cardinality(val_ds).numpy()}')
    
    return train_ds, val_ds