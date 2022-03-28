from sklearn import pipeline
from training_pipeline import *

PATH = {'train':'data/train',
        'val':'data/val',
        'test':'data/test'}

my_pipeline = DataPipeline(PATH['train'], batch_size=64)
train_ds = my_pipeline.load_dataset()
for img, label in train_ds.take(1).cache():
    print(img.shape, label.shape)