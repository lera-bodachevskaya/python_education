import os.path

import matplotlib.pyplot as plt
import skimage.io as io
from skimage.color import rgb2gray
from skimage import segmentation, color
from skimage.util import img_as_ubyte
from skimage import exposure
from skimage.filters import threshold_niblack, threshold_sauvola
from skimage.morphology import erosion, opening, closing

import user_exeptions as ex


class Skimage:
    def __init__(self, path):
        self.img_path = path
        self.img = io.imread(path)

    def info(self, **kwargs):
        print("Image Properties:")
        print("- Number of Pixels: " + str(self.img.size))
        print("- Shape: " + str(self.img.shape))

        self.show(self.img_path)

    def get_rgb(self, **kwargs):
        if kwargs['x'] is None or kwargs['y'] is None:
            raise ex.ArgumentsError('you have to specify the arguments -x and -y')

        pixel = self.img[kwargs['x'], kwargs['y']]
        print("Pixel color in RGB: ")
        print("- Red: " + str(pixel[0]))
        print("- Green: " + str(pixel[1]))
        print("- Blue: " + str(pixel[2]))

    def convert_to_bw(self, **kwargs):
        if kwargs['save_path'] is None:
            raise ex.ArgumentsError('you have to specify the argument -s')

        bw_img = rgb2gray(self.img)
        self.save(kwargs['save_path'], bw_img)
        self.show(kwargs['save_path'], "gray")

    def histogram(self, **kwargs):
        try:
            res = exposure.equalize_hist(self.img)
        except:
            raise ex.HistogramError("histogram can't be created")

        self.save("histogram.jpg", res)
        self.show("histogram.jpg")

    def thresholding(self, **kwargs):
        thresh_niblack = self.img > threshold_niblack(self.img)
        self.save("thresholding_thresh_niblack.jpg", img_as_ubyte(thresh_niblack))

        thresh_sauvola = self.img > threshold_sauvola(self.img)
        self.save("thresholding_thresh_sauvola.jpg", img_as_ubyte(thresh_sauvola))

    def morphology(self, **kwargs):
        types = [erosion, opening, closing]

        for type in types:
            res = type(self.img)
            self.save("morphology" + str(type) + ".jpg", res)

    def segmentation(self, **kwargs):
        try:
            label = segmentation.slic(self.img, compactness=30, n_segments=400, start_label=1)
            res = color.label2rgb(label, self.img, kind='avg', bg_label=0)
        except:
            raise ex.SegmentationError("file can't be segmented")

        self.save("segmentation.jpg", res)

    def show(self, path, cmap=""):
        try:
            img = io.imread(path)

            if cmap == "gray":
                plt.imshow(img, cmap=plt.cm.gray)
            else:
                plt.imshow(img)

            plt.show()
        except:
            raise ex.ShowError("picture can't be displayed")

    def save(self, path, img):
        if os.path.exists(path):
            raise ex.SaveError("file with the same name already exists")

        absolute_path = os.path.abspath(path)
        file_name = os.path.os.path.basename(absolute_path)
        path_without_name = absolute_path.replace(file_name, '')

        if not os.path.exists(path_without_name):
            raise ex.SaveError("no such folder exists")

        try:
            io.imsave(path, img)
        except Exception:
            raise ex.SaveError("can't be saved to the specified path")
