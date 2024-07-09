import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


class BRATS_Reader():
    def __init__(self, datapath):
        self.datapath = datapath
        self.HGG_root = datapath + '/HGG'
        self.LGG_root = datapath + '/LGG'
        self.p_list = []
    
    
    def fetch_hgg_patients_paths(self):
        hgg_patients = os.listdir(self.HGG_root)
        return [self.HGG_root + '/' + p for p in hgg_patients]
    
    
    def fetch_lgg_patients_paths(self):
        lgg_patients = os.listdir(self.LGG_root)
        return [self.LGG_root + '/' + p for p in lgg_patients]
    
    
    def create_single_patients_list(self):
        hgg_patients = self.fetch_hgg_patients_paths()
        lgg_patients = self.fetch_lgg_patients_paths()
        return hgg_patients + lgg_patients
    
    
    def read_patient_data(self, path_to_patient):
        p_files = os.listdir(path_to_patient)
        for f in p_files:
            path = path_to_patient + '/' + f
            if f.endswith('t2.nii.gz'):
                t2 = nib.load(path).get_fdata()
            if f.endswith('flair.nii.gz'):
                flair = nib.load(path).get_fdata()
            if f.endswith('t1.nii.gz'):
                t1 = nib.load(path).get_fdata()
            if f.endswith('t1ce.nii.gz'):
                t1ce = nib.load(path).get_fdata()
            if f.endswith('seg.nii.gz'):
                seg = nib.load(path).get_fdata()
        print(t1.shape, seg.shape)
        
        img = np.zeros((5,) + t1.shape)
        print(type(img), type(t1))
        img[0, :, :, :] = t1
        img[1] = t1ce
        img[2] = t2
        img[3] = flair 
        img[4] = seg
        
        return img
        
    def show_patient(self, patient):
        s = 90
        plt.figure(figsize=(15, 15)) 
        l = ['T1', 'T1ce', 'T2', 'Flair', 'Seg']
        for i in range(1, 6):
            plt.subplot(2, 5, i)
            plt.imshow(patient[i-1, :, :, s], cmap='gray')
            plt.axis('off')
            plt.title(l[i-1], fontsize=8)
            
        for i in range(6, 11):
            plt.subplot(2, 5, i)
            plt.imshow(patient[i-6, :, :, s], cmap='gray')
            plt.imshow(patient[4, :, :, s], alpha=0.3)
            plt.axis('off')
            
        plt.savefig('./check/test.png')
        plt.close()
