
from bdr.brats_reader import BRATS_Reader as BR

# dataset_root = './raw_data/MICCAI_BraTS_2018'
dataset_root = './raw_data/BRATS_2019'

b = BR(dataset_root)
a = b.fetch_hgg_patients_paths()
img = b.read_patient_data(a[30])
b.show_patient(img)