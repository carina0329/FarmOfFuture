import tifffile as tf
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
import imutils
import os

def render_tiff(raster_path, image_path):
    # raster_fp = "satellite_data/raster_files/" + filename + ".tif"
    img = tf.imread(raster_path)
    # scale to 0-255
    img = img // (img.max() / 255)
    orig = img
    # plt.imsave("orig.png", img.astype(np.uint8))
    # so the shape should be (x, y, 4)
    # let's remove all the initial rows and columns that are all zeros
    rows = 0
    while np.all(orig[rows] == 0):
        rows += 1
    cols = 0
    while np.all(orig[:, cols] == 0):
        cols += 1
    orig = orig[rows:, cols:]
    # #now let's rotate the image so that the first non-zero pixel is in the top left
    firstX = np.nonzero(orig[0, :, :])[0][0]
    firstY = np.nonzero(orig[:, 0, :])[0][0]
    # print(firstX)
    # print(firstY)
    angle = np.arctan2(firstX, firstY)
    # print(angle * 180 / np.pi)
    # print(img.shape)
    img = img.transpose(1, 2, 0)
    # print(img.shape)
    img = imutils.rotate_bound(img, angle * 180 / np.pi)
    brightness_factor = 2 # adjust this as needed
    img *= brightness_factor

    newImg = np.array(img)
    # #let's crop all the rows and columns that are all zeros
    rows = 0
    while np.all(newImg[rows] == 0):
        rows += 1
    cols = 0
    while np.all(newImg[:, cols] == 0):
        cols += 1
    newImg = newImg[rows:, cols:]
    # #now let's remove the rows and columns that are all zeros from the other side
    rows = newImg.shape[0] - 1
    while np.all(newImg[rows] == 0):
        rows -= 1
    cols = newImg.shape[1] - 1
    while np.all(newImg[:, cols] == 0):
        cols -= 1
    newImg = newImg[: rows + 1, : cols + 1]
    # #now let's rotate the image if x is greater than y
    if newImg.shape[0] > newImg.shape[1]:
        newImg = np.rot90(newImg)
    newImg = np.ascontiguousarray(newImg)
    # newImg_path = "satellite_data/image_files/" + filename + ".png"
    plt.imsave(image_path, newImg.astype(np.uint8)[:, :, [0, 1, 2]])

if __name__ == "__main__":
    # assign directory
    directory = 'satellite_data/raster_files/2023-04-12_psscene_analytic_udm2/files'
    # iterate over files in
    # that directory
    for rasterFileName in os.listdir(directory):
        f = os.path.join(directory, rasterFileName)
        # checking if it is a file
        if os.path.isfile(f):
            if f.endswith(".tif") and "Analytic" in f:
                image_filename = os.path.splitext(rasterFileName)[0] + ".png"
                image_folder = "satellite_data/image_files/"
                image_path = os.path.join(image_folder, image_filename)
                print(image_path)
                render_tiff(f, image_path)