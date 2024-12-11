import os
from pathlib import Path
import shutil
from skimage.io import imread, imsave
import numpy as np

def convert():
    """
    1. Get the data from https://www.kaggle.com/competitions/data-science-bowl-2018/data
    2. Extract train.zip and test.zip to directories `train_instances` and `test_instances`
    3. We expect that the masks are multiple images represent the instances
    4. We will convert the instances masks to one image semantic to be compatible with data loading scheme of pytorch-3dunet
    5. Replace the data dir with your own path of extracted data
    6. Run the script to do the conversion. The semantic images will be created under the same directory you specified as `data_dir`
    """
    data_dir = Path("/home/thodkatz/repos/kreshuklab/ilastik-playground/tiktorch_playground/2d_unet_dsb_2018/data/")
    train_instances_dir = data_dir / "train_instances"
    test_instances_dir = data_dir / "test_instances"
    
    def per_mask_dir(masks_dir: str, output_file_path: str):
        label_image = None

        black = 0
        white = 255
        for i, mask_file in enumerate(sorted(os.listdir(masks_dir))):
            mask = imread(os.path.join(masks_dir, mask_file))
            if label_image is None:
                label_image = np.full_like(mask, fill_value=black, dtype=np.uint8)
            label_image[mask == white] = white

        imsave(f"{output_file_path}/mask.png", label_image)
        
    def per_instances_dir(instances_dir: Path, semantic_name_dir: str):
        for instance_dir in os.listdir(instances_dir):
            mask_dir = instances_dir / instance_dir / "masks"
            raw_dir = instances_dir / instance_dir / "images"
            assert mask_dir.exists()
            assert raw_dir.exists()
            
            semantic_dir = data_dir / semantic_name_dir / instance_dir
            
            
            shutil.copytree(raw_dir, semantic_dir / "images", dirs_exist_ok=True)

            output_file_path = semantic_dir / "masks"
            os.makedirs(output_file_path, exist_ok=True)            
            per_mask_dir(str(mask_dir), str(output_file_path))
    
    per_instances_dir(train_instances_dir, semantic_name_dir = "train_semantic")
    per_instances_dir(test_instances_dir, semantic_name_dir = "test_semantic")
        


if __name__ == "__main__":
    convert()