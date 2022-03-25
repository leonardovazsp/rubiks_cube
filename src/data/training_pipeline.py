from tabnanny import verbose
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import os
import random
from scipy import ndimage
import copy
import tensorflow as tf

AUTOTUNE = tf.data.AUTOTUNE

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

def get_dataset(directory_path, batch_size):
    filelist = []
    for file in os.listdir(directory_path):
        if (file.endswith('.jpg') & file[-10:-6].isnumeric()):
            filepath = os.path.join(directory_path, file)
            filelist.append(filepath[:])
    image_count = len(filelist)
    ds = tf.data.Dataset.list_files(filelist, shuffle=False)
    ds = ds.shuffle(image_count, reshuffle_each_iteration=False)
    ds = ds.map(wrapper_func)
    ds = configure_for_performance(ds, batch_size)
    return ds

def get_label(file_path):
    label = np.load(str(file_path.numpy(), 'utf-8')[:-6] + '.npy')
    if str(file_path.numpy())[-6] == '2':
        label = label[[2,3,5]]
        label_ = copy.deepcopy(label)
        label[0] = np.rot90(label_[1], 2)
        label[1] = np.rot90(label_[0], 2)
        label[2] = np.rot90(label_[2], 1)
    else:
        label = label[[0,1,4]]
    label = label.reshape((27, 6))
    label = tf.convert_to_tensor(label, dtype=tf.float32)
    return label

def decode_img(img, img_resolution):
    '''
    Decodes bytes into jpeg, resizes the image and convert it into tensorflow tensor
    
    Args:
        img: bytes from tf.io.read_file
    
    Returns:
        tensorflow tensor
    '''
    img = tf.io.decode_jpeg(img, channels=3)/255
    img = tf.image.resize(img, *img_resolution)
    img = tf.convert_to_tensor(img, dtype=tf.float32)
    return img

def process_path(file_path):
    '''
    Reads image and labels from file_path
    
    Args:
        file_path: string of the path of the image file - ends with .jpg
    
    Returns:
        img: tensorflow tensor
        label: tensorflow tensor
    '''
    img = tf.io.read_file(file_path)
    img = decode_img(img)
    img = augmentation(img)
    label = get_label(file_path)
    return img, label

def configure_for_performance(ds, batch_size):
    ds = ds.cache()
    ds = ds.shuffle(buffer_size=8)
    ds = ds.batch(batch_size)
    ds = ds.prefetch(buffer_size=AUTOTUNE)
    return ds

def wrapper_func(x):
    x, y = tf.py_function(process_path, [x], [tf.float32, tf.float32])
    return x, y

def dataset(path, batch_size):
    train_ds = get_dataset(path['train'], batch_size)
    val_ds = get_dataset(path['val'], batch_size)
    test_ds = get_dataset(path['test'], batch_size)
    return train_ds, val_ds, test_ds