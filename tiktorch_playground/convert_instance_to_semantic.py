import os
from pathlib import Path
import shutil
from skimage.io import imread, imsave
import numpy as np
import random

def convert():
    """
    1. Get the data from https://www.kaggle.com/competitions/data-science-bowl-2018/data
    2. Extract train.zip and test.zip
    3. We expect that the masks are multiple images represent the instances
    4. We will convert the instances masks to one image semantic to be compatible with data loading scheme of pytorch-3dunet
    5. Replace the data dir with your own path of extracted data
    6. Run the script to do the conversion. The semantic images will be created under the same directory you specified as `data_dir`
    7. The validation set is 0.2 of the training, created under `val_semantic`
    """
    data_dir = Path("/home/thodkatz/repos/kreshuklab/ilastik-playground/tiktorch_playground/2d_unet_dsb_2018/data/")
    train_instances_dir = data_dir / "train_instances"
    train_semantic_dir = data_dir / "train_semantic"
    
    def per_mask_dir(masks_dir: str, output_file_path: str):
        label_image = None

        black = 0
        white = 255
        for i, mask_file in enumerate(sorted(os.listdir(masks_dir))):
            mask = imread(os.path.join(masks_dir, mask_file))
            if label_image is None:
                label_image = np.full_like(mask, fill_value=black, dtype=np.uint8)
            label_image[mask == white] = white
            
        print("File saved:", f"{output_file_path}/mask.png")
        imsave(f"{output_file_path}/mask.png", label_image)
        
    def per_instances_dir(source_instances_dir: Path, target_semantic_dir: Path):
        for instance_dir in os.listdir(source_instances_dir):
            mask_dir = source_instances_dir / instance_dir / "masks"
            raw_dir = source_instances_dir / instance_dir / "images"
            assert mask_dir.exists(), f"{mask_dir} doesn't exist"
            assert raw_dir.exists(), f"f{raw_dir} doesn't exist"
            
            target_mask_semantic_dir = target_semantic_dir /  instance_dir / "masks"
            target_images_semantic_dir = target_semantic_dir / instance_dir / "images"
            
            shutil.copytree(raw_dir, target_images_semantic_dir, dirs_exist_ok=True)

            os.makedirs(target_mask_semantic_dir, exist_ok=True)            
            per_mask_dir(str(mask_dir), str(target_mask_semantic_dir))

    #per_instances_dir(train_instances_dir, train_semantic_dir)
    
    def split_train_val(train_dir: Path):
        instances_dir = os.listdir(train_dir)
        num = len(instances_dir)
        val_idx = random.sample(range(0, num), int(0.2 * num))
        val_instances = [instances_dir[idx] for idx in val_idx]
        val_dir = data_dir / "val_semantic"
        os.makedirs(val_dir)
        for val_instance in val_instances:
            print("File moved:", str(val_dir / val_instance))
            shutil.move(src=str(train_dir / val_instance), dst=str(val_dir / val_instance))

    split_train_val(train_semantic_dir)

if __name__ == "__main__":
    convert()