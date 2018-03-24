import os
import random
import glob
import cv2
import numpy as np
import xlrd

#import matplotlib.pyplot as plt
#from matplotlib.widgets import Slider
#from sparcs.training.augmentation.preprocessing_functions import random_shift, random_rotation, random_flip, augment_intensity, crop_to_bounding_box

def listdir_nohidden(path):
    return glob.glob(os.path.join(path, '*'))


class ImageFeeder:
    def __init__(self, directory, split_ratio, output_dims=(400, 400), batchsize=16, expand_trainset=1, expand_validationset=1):
        """
        :param directory: images base directory path. Should contain a folder for each class
        :param split_ratio: tuple with the ratios (train_size, validation_size, test_size)
        :param output_dims: the image output dimensions
        :param batchsize: the batchsize
        """
        self.base_dir = directory
        self.file_paths = []
        #self.labels = []
        #contrains a list of filenames for each split and the corresponding labels
        self.splits = {
            "train": [],
            "val": [],
            "test": [],
            "train_labels": [],
            "val_labels": [],
            "test_labels": []
        }
        self.split_ratio = split_ratio
        self.batch_size = batchsize
        self.output_dims = output_dims

        #points to the current position in the list while iterating through the data
        self.current_list_pointer = {
            "train": 0,
            "val": 0,
            "test": 0
        }

        #how many steps to perform to iterate through the data once
        self.steps = {
            "train": 0,
            "val": 0,
            "test": 0
        }
        
        self.label = {}
        
        random.seed(42)
        self.load_filepaths()


    def load_filepaths(self):
        #num_class = 0
        book = xlrd.open_workbook("Label/labels.xlsx")
        sheet = book.sheet_by_index(0)
        
        for i in range(0,sheet.nrows):
            imgName = "img_%s" % (i)
            self.label[imgName] = sheet.cell_value(i,1)
        #iterate through directories
        #print(self.base_dir)
        #print(listdir_nohidden(self.base_dir))
        data_path = listdir_nohidden(self.base_dir)
        self.splits["train"].extend(data_path[0:int(self.split_ratio[0]*len(data_path))])
        self.splits["val"].extend(data_path[int(self.split_ratio[0] * len(data_path)):int((self.split_ratio[0]+self.split_ratio[1]) * len(data_path))])
        self.splits["test"].extend(data_path[int((self.split_ratio[0] + self.split_ratio[1]) * len(data_path)):len(data_path)])
        
        self.steps["train"] = 1#int(len(self.splits["train"])/self.batch_size)
        self.steps["val"] = 1#int(len(self.splits["val"])/self.batch_size)
        self.steps["test"] = 1#int(len(self.splits["test"])/self.batch_size)
        
        print(len(self.splits["train"]))
        print(len(self.splits["val"]))
        

    def shuffle_data(self):
        random.shuffle(self.splits["train"])
        random.shuffle(self.splits["val"])
        random.shuffle(self.splits["test"])

        #reset the list pointers
        self.current_list_pointer["train"] = 0
        self.current_list_pointer["val"] = 0
        self.current_list_pointer["test"] = 0


    def load_image(self, path, augment=False):
        """
        Loads one image at a time. Here is the place to perform augmentation.
        :param path: Path to the image
        :param augment: If the image should be augmented
        :return: The (augmented) image
        """

        img = cv2.imread(path)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        #crop images
        #img = crop_to_bounding_box(img, 2200)
        img = cv2.resize(img, self.output_dims)

        #if augment:
            #random flipping
            #img = random_flip(img)
            #random shifting
            #img = random_shift(img)
            #random rotation
            #img = random_rotation(img)

        #intensity augmentation
        #img = augment_intensity(img)

        #img = cv2.resize(img, self.output_dims)
        return img


    def get_next_train_batch(self):
        """
        Returns the next train batch
        :return: Data, labels
        """
        #images = [self.load_image(path, augment=False) for path in self.splits["train"][self.current_list_pointer["train"]:self.current_list_pointer["train"]+self.batch_size]]
        images = []
        Y = np.zeros((self.batch_size, 1))
        
        for i in range(self.current_list_pointer["train"],self.current_list_pointer["train"]+self.batch_size):
            path = self.splits["train"][i]
            images.append(self.load_image(path, augment=False))
            base = os.path.basename(path)
            imgName = os.path.splitext(base)[0]
            Y[i,0] = self.label[imgName]
        
        print(self.batch_size)
        print(len(images))
        
        X = np.stack(images)
        print(X.shape)
        #X = X[:,:,:,np.newaxis]
        #print(X.shape)
        
        return X, Y


    def get_next_val_batch(self):
        """
        Returns the next validation batch
        :return: Data, labels
        """

        if self.current_list_pointer["val"]+self.batch_size > len(self.splits["val"]):
            images = []
            Y = np.zeros((len(self.splits["val"])-self.current_list_pointer["val"], 1))
            for i in range(self.current_list_pointer["val"],len(self.splits["val"])):
                path = self.splits["val"][i]
                images.append(self.load_image(path))
                base = os.path.basename(path)
                imgName = os.path.splitext(base)[0]
                Y[i,0] = self.label[imgName]
        else:
            images = []
            Y = np.zeros((self.batch_size, 1))
            for i in range(self.current_list_pointer["val"],self.current_list_pointer["val"]+self.batch_size):
                path = self.splits["val"][i]
                images.append(self.load_image(path))
                base = os.path.basename(path)
                imgName = os.path.splitext(base)[0]
                Y[i,0] = self.label[imgName]

        X = np.stack(images)
        X = X[:,:,:,np.newaxis]
        
        return X, Y

    """
    def get_next_test_batch(self):
        "#""
        Returns the next test batch
        :return: Data, labels
        "#""
        images = [self.load_image(path) for path in self.splits["test"][self.current_list_pointer["test"]:self.current_list_pointer["test"]+self.batch_size]]
        #print(self.batch_size)
        #print(len(images))
        
        X = np.stack(images)
        X = X[:,:,:,np.newaxis]
        
        Y = np.zeros((self.batch_size, 1))
        for i in range(0,self.batch_size):
            path = self.splits["test"][self.current_list_pointer["test"] + i]
            base = os.path.basename(path)
            imgName = os.path.splitext(base)[0]
            Y[i,0] = imgName
            
        return X, Y
    
    
    
if __name__ == "__main__":
    imObj = ImageFeeder("C:/Users/Thomas/Documents/Studium/Vorlesung/Maschbau/Master/3. Semester/TMS/solAI/Code/Image", (0.75,0.25,0), output_dims=(400, 400), batchsize=16, expand_trainset=1, expand_validationset=1)
    
    (X_train, Y_train) = imObj.get_next_train_batch()
    (X_val, Y_val) = imObj.get_next_val_batch()
    """