from training_pipeline import *

PATH = {'train':'data/train',
        'val':'data/val',
        'test':'data/test'}

def test_get_dataset():
    train_ds, val_ds, test_ds = dataset(PATH, 256)
    for i in train_ds.take(1):
        print(i.shape)
    for i in val_ds.take(1):
        print(i.shape)
    for i in test_ds.take(1):
        print(i.shape)

test_get_dataset()