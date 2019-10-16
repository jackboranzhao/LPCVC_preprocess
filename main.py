#! /usr/bin/env python
# coding=utf-8
import os
import numpy as np
from absl import app
from PIL import Image
from absl import flags

flags.DEFINE_string('init_dir',None,'testing images dataset folder path')
flags.DEFINE_string('new_dir',None,'preprocessed images folder')
FLAGS = flags.FLAGS

image_size = 256
CROP_PADDING = 32

def ImageNet_preprocess(image_dataset_dir,image_resized_dir,image_size):
	image_list = sorted(os.listdir(image_dataset_dir))
	for image_name in image_list:
		image_dir = os.path.join(image_dataset_dir,image_name)
		image = Image.open(image_dir)
		image = image.convert('RGB')

		shape = np.shape(image)
		image_height = shape[0]
		image_width = shape[1]
		ratio = image_size / (image_size + CROP_PADDING)
		min_edg = float(np.min([image_height, image_width]))
		padded_center_crop_size = int(ratio*min_edg)
		offset_height = ((image_height - padded_center_crop_size) + 1) // 2
		offset_width = ((image_width - padded_center_crop_size) + 1) // 2
		new_image = image.crop((offset_width,offset_height,offset_width+padded_center_crop_size,offset_height+padded_center_crop_size))
		new_image = new_image.resize((image_size,image_size),Image.BICUBIC)
		new_dir = os.path.join(image_resized_dir,image_name.split('.')[0]+'.bmp')
		new_image.save(new_dir) 

def main(argv):
	del argv
	image_dataset_dir = FLAGS.init_dir
	image_resized_dir = FLAGS.new_dir
	if not os.path.exists(image_resized_dir):
		os.mkdir(image_resized_dir)
	ImageNet_preprocess(image_dataset_dir,image_resized_dir,image_size)
	print('Resized images are saved in ',image_resized_dir)

if __name__=='__main__':
	app.run(main)