import tifffile as tf
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
import imutils
import os
import math

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
    # brightness_factor = 2 # adjust this as needed
    # img *= brightness_factor

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
    # # #now let's rotate the image if x is greater than y
    # if newImg.shape[0] > newImg.shape[1]:
    #     newImg = np.rot90(newImg)
    newImg = np.ascontiguousarray(newImg)

    # newImg_path = "satellite_data/image_files/" + filename + ".png"
    plt.imsave(image_path, newImg.astype(np.uint8)[:, :, [0, 1, 2]])

def rotate_image(topleft_lat, topleft_lng, topright_lat, topright_lng, bottomleft_lat, bottomleft_lng, image_path, output_image_path):
    # Open the image file
    im = Image.open(image_path)

    # Calculate the angle of rotation
    x_dist = topright_lng - topleft_lng
    y_dist = topleft_lat - bottomleft_lat
    angle = math.degrees(math.atan2(y_dist, x_dist))

    # Rotate the image
    im = im.rotate(angle, resample=Image.BICUBIC, expand=True)

    # Save the rotated image
    im.save(output_image_path)


if __name__ == "__main__":
    file_to_render = "satellite_data/test/20230301_155145_86_24cc_3B_Visual_clip.tif"
    render_tiff(file_to_render, "test_611.png")
    # rotate_image(40.30755118678022, -88.12844111806457, 40.236450233259035, -87.71013728656837, 40.1161230839948, -88.18262304366571, "test_407.png", "rotated_test_407.png")