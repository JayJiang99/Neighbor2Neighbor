import os
import glob
import fnmatch
from PIL import Image


def filter_image_sizes(images):
    filtered = []
    for idx, fname in enumerate(images):
        if (idx % 10000) == 0:
            print('loading images', idx, '/', len(images))
        try:
            with Image.open(fname) as img:
                w, h = img.size
                if (w < 256 or h < 256):
                    continue
                filtered.append(fname)
        except:
            print('Could not load image', fname, 'skipping file..')
    return filtered


def load_and_crop(img_path, save_dir):
    img_name = os.path.basename(img_path)
    img = Image.open(img_path)
    img = img.convert("L")
    width, height = img.size
    crop_size = 256
    num_x_crops = (width - 1) // crop_size + 1
    num_y_crops = (height - 1) // crop_size + 1
    for i in range(num_x_crops):
        for j in range(num_y_crops):
            left = i * crop_size
            upper = j * crop_size
            right = min(left + crop_size, width)
            lower = min(upper + crop_size, height)
            cropped_img = img.crop((left, upper, right, lower))
            cropped_img_name = f"{os.path.splitext(img_name)[0]}_{i}_{j}.JPEG"
            cropped_img.save(os.path.join(save_dir, cropped_img_name), quality=100, subsampling=0)
def load_and_save(img_path):
    img_name = os.path.basename(img_path)
    img = Image.open(img_path)
    img = img.convert("L")
    save_path = os.path.join(save_dir, img_name)
    img.save(save_path, quality=100, subsampling=0)

# input_dir = "./oct_16_40"
input_dir = "D:/zhiyi/OCT_SR/OCT_data/all_noisy_data"
save_dir = "D:/zhiyi/OCT_SR/OCT_data/all_noisy_data_n2n"

images = []
pattern = os.path.join(input_dir, '**/*')
all_fnames = glob.glob(pattern, recursive=True)
for fname in all_fnames:
    # include only JPEG/jpg/png
    if fnmatch.fnmatch(fname, '*.JPEG') or fnmatch.fnmatch(
            fname, '*.jpg') or fnmatch.fnmatch(fname, '*.png') or fnmatch.fnmatch(fname, '*.tif'):
        images.append(fname)
images = sorted(images)

filtered = filter_image_sizes(images)
print(len(filtered))

os.makedirs(save_dir, exist_ok=True)
for idx, img_path in enumerate(filtered):
    if (idx % 1000) == 0:
        print('loading and cropping images', idx, '/', len(filtered))
    load_and_save(img_path)
print(len(glob.glob(os.path.join(save_dir, "*.JPEG"))))