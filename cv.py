import os.path

import cv2
import matplotlib.pyplot as plt
import numpy as np

import user_exeptions as ex


class Cv:
    def __init__(self, path, rw=True):
        self.img_path = path
        self.img = self.open(path)
        self.rw = rw

    def open(self, path, color_mode=cv2.IMREAD_ANYCOLOR):
        if not os.path.exists(path):
            raise ex.PathError("there is no file with this name")

        if not os.access(path, os.R_OK):
            raise ex.PermissionError("no permissions to open the file")

        try:
            img = cv2.imread(path, color_mode)
        except:
            raise ex.OpenError("unable to open the file for reading")

        if img is None:
            raise ex.FormatError("invalid file format")

        return img

    def isColor(self, img):
        shape = img.shape

        if len(shape) == 2:
            return False

        elif len(shape) == 3:
            if shape[2] == 1:
                return False
            elif shape[2] == 3 or shape[2] == 4:
                return True
            else:
                raise ex.ImageFormatError("unknown image color format. image shape = {}".format(shape))

        else:
            raise ex.ImageFormatError("unknown image size format. image shape = {}".format(shape))

    def info(self, **kwargs):
        print("Image Properties:")
        print("- Number of Pixels: {}".format(self.img.size))
        print("- Shape: {}".format(self.img.shape))

        self.show(self.img_path, True)

    def get_rgb(self, **kwargs):
        if kwargs['x'] is None or kwargs['y'] is None:
            raise ex.ArgumentsError('you have to specify the arguments -x and -y')

        isColor = self.isColor(self.img)
        pixel = self.img[kwargs['x'], kwargs['y']]

        print("Pixel color: ")
        if isColor:
            for i in range(pixel.size):
                print("- {}".format(pixel[i]))
        else:
            print(pixel)

    def convert_to_bw(self, **kwargs):
        if kwargs['save_path'] is None:
            raise ex.ArgumentsError('you have to specify the argument -s')

        if self.isColor(self.img):
            bw_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        else:
            bw_img = self.img

        self.save(kwargs['save_path'], bw_img)
        self.show(kwargs['save_path'])

    def histogram(self, **kwargs):
        img = self.open(self.img_path, 0)

        equ = cv2.equalizeHist(img)

        res = np.hstack((img, equ))

        self.save("histogram.jpg", res)
        self.show("histogram.jpg")

    def thresholding(self, **kwargs):
        types = [cv2.THRESH_BINARY, cv2.THRESH_BINARY_INV, cv2.THRESH_TRUNC, cv2.THRESH_TOZERO, cv2.THRESH_TOZERO_INV]

        for t in types:
            ret, thresh = cv2.threshold(self.img, 127, 255, t)
            self.save("thresh_{}.jpg".format(t), thresh)

    def morphology(self, **kwargs):
        kernel = np.ones((5, 5), np.uint8)

        dilation = cv2.dilate(self.img, kernel, iterations=1)
        self.save("morphology_dilation.jpg", dilation)

        types = [cv2.MORPH_OPEN, cv2.MORPH_CLOSE, cv2.MORPH_GRADIENT, cv2.MORPH_TOPHAT, cv2.MORPH_BLACKHAT]

        for t in types:
            morphology = cv2.morphologyEx(self.img, t, kernel)
            self.save("morphology_{}.jpg".format(t), morphology)

    def segmentation(self, **kwargs):
        if self.isColor(self.img):
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        else:
            gray = self.img

        ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        sure_bg = cv2.dilate(opening, kernel, iterations=3)

        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        ret, markers = cv2.connectedComponents(sure_fg)

        markers = markers + 1

        markers[unknown == 255] = 0

        markers = cv2.watershed(self.img, markers)

        self.img[markers == -1] = [255, 0, 0]

        self.save("segmentation.jpg", self.img)

    def show(self, path, toRgb=False):
        img = self.open(path)

        img = self.open(path)

        if toRgb:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        plt.imshow(img)
        plt.show()

    def save(self, path, img):
        if not self.rw:
            if os.path.exists(path):
                raise ex.PathError("file with the same name already exists")

        absolute_path = os.path.abspath(path)
        file_name = os.path.basename(absolute_path)
        path_without_name = absolute_path.replace(file_name, '')

        if not os.path.exists(path_without_name):
            os.makedirs(path_without_name)

        cv2.imwrites(path, img)
