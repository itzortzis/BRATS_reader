import os
import random
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt


class BRATS_Reader():
    def __init__(self, datapath):
        self.datapath = datapath
        self.HGG_root = datapath + '/HGG'
        self.LGG_root = datapath + '/LGG'
        self.p_list = []
        self.get_original_input_shape()
    
    
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
    
    def get_original_input_shape(self):
        paths = self.fetch_hgg_patients_paths()
        print("Moooods: ", paths[0])
        mods = os.listdir(paths[0])
        path_to_mods = paths[0] + '/' + mods[0]
        patient = nib.load(path_to_mods).get_fdata()
        self.original_input_shape = patient.shape
        
    def read_patient_data(self, path_to_patient):
        p_files = os.listdir(path_to_patient)
        img = np.zeros((5,) + self.original_input_shape)
        for f in p_files:
            path = path_to_patient + '/' + f
            if f.endswith('t2.nii.gz'):
                img[2] = nib.load(path).get_fdata()
            if f.endswith('flair.nii.gz'):
                img[3] = nib.load(path).get_fdata()
            if f.endswith('t1.nii.gz'):
                img[0] = nib.load(path).get_fdata()
            if f.endswith('t1ce.nii.gz'):
                img[1] = nib.load(path).get_fdata()
            if f.endswith('seg.nii.gz'):
                img[4] = nib.load(path).get_fdata()
        
        return img
    
    def show_random_patients(self, dataset, times):
        for i in range(times):
            p = random.randint(0, len(dataset) - 1)
            s = random.randint(60, 100)
            self.show_patient(dataset[p], s, p)
            
    
    def show_patient(self, patient, s, id):
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
            
        plt.savefig('./check/p_'+ str(id) +'.png')
        plt.close()
        
        
    def create_dataset(self, p_list):
        num_of_patients = len(p_list)
        dataset = np.zeros((num_of_patients, 5,) + self.original_input_shape)
        for i in range(num_of_patients):
            dataset[i] = self.read_patient_data(p_list[i])
            
        return dataset
