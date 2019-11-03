'''
This script is taken from https://github.com/xinntao/BasicSR/blob/master/codes/scripts/generate_mod_LR_bic.py
Need to understand, but for now using for generating Low res ang bicubic upscale images.
Can be done using much simpler code.
This code is useful for variable size of images but my images are square, so don't Need
this now but useful for later use cases.
'''
import os
import sys
import cv2
import numpy as np
import glob

try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils import imresize_np
except ImportError:
    pass


def generate_mod_LR_bic():
    # set parameters
    up_scale = 4
    mod_scale = 4
    # set data dir
    # directory structure on sunray server pc
    # Need to change later when refactoring, code cleaning and testing.
    sourcedir = '/home/jakaria/Super_Resolution/Datasets/COWC/DetectionPatches_256x256/Potsdam_ISPRS'
    savedir = '/home/jakaria/Super_Resolution/Datasets/COWC/DetectionPatches_256x256/Potsdam_ISPRS'

    saveHRpath = os.path.join(savedir, 'HR', 'x' + str(mod_scale))
    saveLRpath = os.path.join(savedir, 'LR', 'x' + str(up_scale))
    saveBicpath = os.path.join(savedir, 'Bic', 'x' + str(up_scale))

    if not os.path.isdir(sourcedir):
        print('Error: No source data found')
        exit(0)
    if not os.path.isdir(savedir):
        os.mkdir(savedir)

    if not os.path.isdir(os.path.join(savedir, 'HR')):
        os.mkdir(os.path.join(savedir, 'HR'))
    if not os.path.isdir(os.path.join(savedir, 'LR')):
        os.mkdir(os.path.join(savedir, 'LR'))
    if not os.path.isdir(os.path.join(savedir, 'Bic')):
        os.mkdir(os.path.join(savedir, 'Bic'))

    if not os.path.isdir(saveHRpath):
        os.mkdir(saveHRpath)
    else:
        print('It will cover ' + str(saveHRpath))

    if not os.path.isdir(saveLRpath):
        os.mkdir(saveLRpath)
    else:
        print('It will cover ' + str(saveLRpath))

    if not os.path.isdir(saveBicpath):
        os.mkdir(saveBicpath)
    else:
        print('It will cover ' + str(saveBicpath))

    filepaths = [f for f in os.listdir(sourcedir) if f.endswith('.jpg') and not f.endswith('check.jpg')]
    num_files = len(filepaths)

    # prepare data with augementation
    for i in range(num_files):
        filename = filepaths[i]
        print('No.{} -- Processing {}'.format(i, filename))
        # read image
        image = cv2.imread(os.path.join(sourcedir, filename))

        width = int(np.floor(image.shape[1] / mod_scale))
        height = int(np.floor(image.shape[0] / mod_scale))
        # modcrop
        if len(image.shape) == 3:
            image_HR = image[0:mod_scale * height, 0:mod_scale * width, :]
        else:
            image_HR = image[0:mod_scale * height, 0:mod_scale * width]
        # LR
        image_LR = imresize_np(image_HR, 1 / up_scale, True)
        # bic
        image_Bic = imresize_np(image_LR, up_scale, True)

        cv2.imwrite(os.path.join(saveHRpath, filename), image_HR)
        cv2.imwrite(os.path.join(saveLRpath, filename), image_LR)
        cv2.imwrite(os.path.join(saveBicpath, filename), image_Bic)

def copy_folder_name_for_valid_image():
    for file in glob.glob("/home/jakaria/Super_Resolution/Filter_Enhance_Detect/saved/val_images/*/"):
        print(file[:-1])

if __name__ == "__main__":
    generate_mod_LR_bic()
