import numpy as np
from bdr.brats_reader import BRATS_Reader as BR

dataset_root = './raw_data/MICCAI_BraTS_2018'
# dataset_root = './raw_data/BRATS_2019'
dataset_root = './raw_data/BRATS_2020'

b = BR(dataset_root)
a = b.fetch_hgg_patients_paths()
# img = b.read_patient_data(a[30])
# b.show_patient(img)
dataset = b.create_dataset(a)
print(dataset.shape)
# b.show_patient(dataset[10],90,10)
dataset = b.crop_dataset(dataset)
b.show_random_patients(dataset, 20)
print(np.unique(dataset[:, 4, :, :, :]))
print("Faults: ", b.faults)