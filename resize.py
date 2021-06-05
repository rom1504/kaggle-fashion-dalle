
from multiprocessing import Pool
from tqdm import tqdm
import csv
import cv2
import os
import urllib.request
import hashlib
from glob import glob


IMAGE_SIZE = 256
IMAGE_FORMAT = 'jpg'

IMAGE_DIR = '/home/r.beaumont/output_fashion'
if not os.path.exists(IMAGE_DIR):
    os.mkdir(IMAGE_DIR)


images_to_resize = glob("/home/r.beaumont/fashion/images/*")
        
def resize_with_border(im, desired_size=256):
    old_size = im.shape[:2] # old_size is in (height, width) format

    ratio = float(desired_size)/max(old_size)
    new_size = tuple([int(x*ratio) for x in old_size])

    # new_size should be in (width, height) format

    im = cv2.resize(im, (new_size[1], new_size[0]))

    delta_w = desired_size - new_size[1]
    delta_h = desired_size - new_size[0]
    top, bottom = delta_h//2, delta_h-(delta_h//2)
    left, right = delta_w//2, delta_w-(delta_w//2)

    color = [255, 255, 255]
    new_im = cv2.copyMakeBorder(im, top, bottom, left, right, cv2.BORDER_CONSTANT,
        value=color)
    return new_im


def process_image(row):
    filename = row
    output = IMAGE_DIR + "/" + os.path.basename(filename)
    if os.path.exists(output):
        return
    try:
        img = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
        img = resize_with_border(img, IMAGE_SIZE)

        cv2.imwrite(output, img)
    except Exception as e:
        # todo remove
        if os.path.exists(output):
            os.remove(output)
        pass


pool = Pool(60)
for _ in tqdm(pool.imap_unordered(process_image, images_to_resize), total=len(images_to_resize)):
    pass
