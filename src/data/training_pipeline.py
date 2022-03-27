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

class DataPipeline():
    def __init__(self, path, batch_size, window_crop_ratio=0.8, window_resolution=(192, 192), brightness_range=(0.8, 1.2), rotation_range=(-20, 20)):
        print('Class initiated')
        self.path = path
        self.batch_size = batch_size
        self.window_crop_ratio = window_crop_ratio
        self.window_resolution = window_resolution
        self.brightness_range = brightness_range
        self.rotation_range = rotation_range
        self.AUTOTUNE = tf.data.AUTOTUNE
    
    def get_img_resolution(self, img):
        aspect_ratio = tuple((img.shape[i]/img.shape[0] for i in range(2)))
        img_resolution = tuple(int((self.window_resolution[i]/self.window_crop_ratio)*aspect_ratio[i]) for i in range(2))
        return img_resolution
    
    def load_dataset(self):
        filelist = self.get_filelist(self.path)
        image_count = len(filelist)
        self.ds = tf.data.Dataset.list_files(filelist, shuffle=False)
        self.ds = self.ds.shuffle(image_count, reshuffle_each_iteration=False)
        self.ds = self.ds.map(self.wrapper_func)
        self.ds = self.configure_for_performance()
        return self.ds

    def decode_img(self, img):
        '''
        Decodes bytes into jpeg, resizes the image and convert it into tensorflow tensor
        
        Args:
            img: bytes from tf.io.read_file
        
        Returns:
            tensorflow tensor
        '''
        img = tf.io.decode_jpeg(img, channels=3)/255
        img_resolution = self.get_img_resolution(img)
        img = tf.image.resize(img, [*img_resolution])
        img = tf.convert_to_tensor(img, dtype=tf.float32)
        return img

    def augmentation(self, img):
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
        angle = random.randint(*self.rotation_range)
        img = ndimage.rotate(img, angle, reshape=False)
        win_size = int(img.shape[0]*self.window_crop_ratio)
        x0_min = 0
        x0_max = img.shape[0] - win_size
        y0_min = (img.shape[1] - img.shape[0])//2
        y0_max = img.shape[1] - win_size - y0_min
        x = random.randint(x0_min, x0_max)
        y = random.randint(y0_min, y0_max)
        brightness = random.uniform(*self.brightness_range)
        img = img[x:x+win_size, y:y+win_size]*brightness
        return tf.clip_by_value(img, 0, 1)

    def get_label(self, file_path):
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

    def process_path(self, file_path):
        '''
        Reads image and labels from file_path
        
        Args:
            file_path: string of the path of the image file - ends with .jpg
        
        Returns:
            img: tensorflow tensor
            label: tensorflow tensor
        '''
        img = tf.io.read_file(file_path)
        img = self.decode_img(img)
        img = self.augmentation(img)
        label = self.get_label(file_path)
        return img, label

    def wrapper_func(self, x):
        x, y = tf.py_function(self.process_path, [x], [tf.float32, tf.float32])
        return x, y

    def configure_for_performance(self):
        self.ds = self.ds.cache()
        self.ds = self.ds.batch(self.batch_size)
        self.ds = self.ds.prefetch(buffer_size=self.AUTOTUNE)
        return self.ds

    def get_filelist(self, directory_path):
        filelist = []
        for file in os.listdir(directory_path):
            if (file.endswith('.jpg') & file[-10:-6].isnumeric()):
                filepath = os.path.join(directory_path, file)
                filelist.append(filepath[:])
        return filelist