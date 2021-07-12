import os
import argparse

from cv import Cv
from user_skimage import Skimage

import user_exeptions as ex

if __name__ == '__main__':

    commands = ["info", "get_rgb", "convert_to_bw", "histogram", "thresholding", "morphology", "segmentation"]

    parser = argparse.ArgumentParser(description='Check images')
    parser.add_argument('-i', type=str, dest="img_path", required=True, help='path to image')
    parser.add_argument('-c', type=str, dest="command", required=True,
                        help='command to be done with the image (info, get_rgb, convert_to_bw, histogram, thresholding, morphology, segmentation')
    parser.add_argument('-l', type=str, dest="lib", required=True, help='library (cv2, skimage)')
    parser.add_argument('-x', type=int, dest="x_pixel", required=False, help='pixel x-coordinate')
    parser.add_argument('-y', type=int, dest="y_pixel", required=False, help='pixel y-coordinate')
    parser.add_argument('-s', type=str, dest="save_path", required=False, help='path where you want to save the image')
    parser.add_argument('-rw', type=bool, dest="rewrite", required=False, help='rewrite file (True or False)')

    args = parser.parse_args()

    if args.command not in commands:
        print("args error: argument -c must be correct (enter --help to see details)")

    else:
        if args.lib == "cv2":
            try:
                cv = Cv(args.img_path, args.rewrite)
            except ex.FileError as fe:
                print("file error: {} (enter --help for details)".format(fe.txt))

            def_dict = {
                "info": cv.info,
                "get_rgb": cv.get_rgb,
                "convert_to_bw": cv.convert_to_bw,
                "histogram": cv.histogram,
                "thresholding": cv.thresholding,
                "morphology": cv.morphology,
                "segmentation": cv.segmentation
            }

            try:
                def_dict[args.command](x=args.x_pixel, y=args.y_pixel, save_path=args.save_path)

            except ex.ArgumentsError as ae:
                print("args error: {} (enter --help for details)".format(ae.txt))
            except ex.FileError as fe:
                print("file error: {} (enter --help for details)".format(fe.txt))
            except ex.ImageError as ie:
                print("image error: {} (enter --help for details)".format(ie.txt))
            except ex.ConversionError as ce:
                print("conversion error: {} (enter --help for details)".format(ce.txt))

        elif args.lib == "skimage":
            skimage = Skimage(args.img_path)

            def_dict = {
                "info": skimage.info,
                "get_rgb": skimage.get_rgb,
                "convert_to_bw": skimage.convert_to_bw,
                "histogram": skimage.histogram,
                "thresholding": skimage.thresholding,
                "morphology": skimage.morphology,
                "segmentation": skimage.segmentation
            }

            try:
                def_dict[args.command](x=args.x_pixel, y=args.y_pixel, save_path=args.save_path)

            except ex.ArgumentsError as ae:
                print("args error: {} (enter --help for details)".format(ae.txt))
            except ex.FileError as fe:
                print("file error: {} (enter --help for details)".format(fe.txt))
            except ex.ImageError as ie:
                print("image error: {} (enter --help for details)".format(ie.txt))
            except ex.ConversionError as ce:
                print("conversion error: {} (enter --help for details)".format(ce.txt))

        else:
            print("args error: argument -l must be correct (enter --help for details)")

