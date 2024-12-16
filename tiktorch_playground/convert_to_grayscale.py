import os
from pathlib import Path
from skimage.io import imread, imsave


def convert_to_grayscale():
    data_dir = Path("/home/thodkatz/repos/kreshuklab/ilastik-playground/dsb_2018_data")
    train_images_dir = data_dir / "train_semantic"
    test_images_dir = data_dir / "test"
    val_images_dir = data_dir / "val_semantic"
    
    def _convert(images_dir):
        for instance_dir in os.listdir(images_dir):
            raw_image_path = images_dir / instance_dir / "images"/ f"{instance_dir}.png"
            raw_image = imread(raw_image_path)
            # mask_image_path = images_dir / instance_dir / "masks" / "mask.png"
            # mask_image = imread(mask_image_path)
            # print(mask_image.shape)
            print(raw_image.shape)
            raw_image_single_channel = raw_image[:, :, 0]
            # detect num of channels and convert them to 1 grayscale
            imsave(raw_image_path, raw_image_single_channel)
    
    #_convert(train_images_dir)
    #_convert(test_images_dir)
    #_convert(val_images_dir)

if __name__ == "__main__":
    convert_to_grayscale()