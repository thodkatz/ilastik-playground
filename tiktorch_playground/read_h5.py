import h5py


def read():
    file_path = "/home/thodkatz/repos/kreshuklab/ilastik-playground/tiktorch_playground/3d_unet_lightseet_boundary/data/train/Movie1_t00009_crop_gt.h5"

    # Open the HDF5 file
    with h5py.File(file_path, "r") as h5_file:
        print(f"Keys in the HDF5 file: {list(h5_file.keys())}")

        # Inspect 'raw' data
        if "raw" in h5_file:
            raw_data = h5_file["raw"][:]
            print(f"'raw' data shape: {raw_data.shape}")
            print(f"'raw' data type: {raw_data.dtype}")
            print(
                f"Sample raw data: {raw_data[0]}"
            )  # Print a sample (adjust indexing as needed)
        else:
            print("No 'raw' dataset found.")

        # Inspect 'label' data
        if "label" in h5_file:
            label_data = h5_file["label"][:]
            print(f"'label' data shape: {label_data.shape}")
            print(f"'label' data type: {label_data.dtype}")
            print(
                f"Sample label data: {label_data[0]}"
            )  # Print a sample (adjust indexing as needed)
        else:
            print("No 'label' dataset found.")


if __name__ == "__main__":
    read()
