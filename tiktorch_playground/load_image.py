from pathlib import Path
import torch
from skimage.io import imread, imsave
import numpy as np
import matplotlib.pyplot as plt

def load_image():
    tensor_path = Path("/home/thodkatz/repos/kreshuklab/ilastik-playground/sample_output.pt")
    # convert to 255
    tensor = torch.load(tensor_path).detach().numpy()
    print(tensor)
    print(tensor.max())
    print(tensor.min())
    img_array = (tensor * 255).astype(np.uint8)
    imsave("sample_output.png", img_array)
    
    plt.imshow(tensor, cmap="gray")  
    plt.colorbar()  # Optional: Display a color bar for intensity values
    plt.title("Grayscale Image")
    plt.axis("off")  # Optional: Turn off axis labels
    plt.show()
    

if __name__ == "__main__":
    load_image()