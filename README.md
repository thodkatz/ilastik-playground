My ilastik ecosystem garden.

# Environment

```shell
conda env create -n ilastik-playground -f environment.yaml
conda activate ilastik-playground
pip install -e /path/to/tiktorch
pip install -e .
```

# Tiktorch training server

Expected the latest version of https://github.com/ilastik/tiktorch. Currently working on this PR https://github.com/ilastik/tiktorch/pull/225.

Let's try to test the tiktorch server to train a unet. Sample data is provided under `dsb_2018_data`.

1. `git clone git@github.com:thodkatz/ilastik-playground.git` 
2. Modify the [config file](https://github.com/thodkatz/ilastik-playground/blob/main/tiktorch_playground/2d_unet_dsb_2018/unet_config_train.yaml) that parameterizes the model. Replace the corresponding `checkpoint_dir`, and the `file_paths` for the `train` and `val` (`file_paths` needs to be absolute).
3. `cd ilastik-playground/tiktorch_server`
4. Start server `python server.py`.
5. Start client `python cli.py`.
6. Ask the client to what is currently available as action (`-h`)!
