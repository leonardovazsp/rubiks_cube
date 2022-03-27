from sklearn import pipeline
from training_pipeline import *

PATH = {'train':'data/train',
        'val':'data/val',
        'test':'data/test'}

# def test_get_dataset():
#     train_ds, val_ds, test_ds = dataset(PATH, 128)
#     for img, label in train_ds.take(1).cache():
#         print(img.shape, label.shape)
#     for img, label in val_ds.take(1).cache():
#         print(img.shape, label.shape)
#     for img, label in test_ds.take(1).cache():
#         print(img.shape, label.shape)

# test_get_dataset()

my_pipeline = DataPipeline(PATH['train'], batch_size=64)
# print(pipeline)
train_ds = my_pipeline.load_dataset()
for img, label in train_ds.take(1).cache():
    print(img.shape, label.shape)