import yaml
import os

def expand_loaders_path(yaml_path) -> str:
    with open(yaml_path, "r") as f:
        config = f.read()
    yaml_config = yaml.safe_load(config)
    train_files_path = yaml_config['loaders']['train']['file_paths']
    assert len(train_files_path) == 1, "we assume that it is a directory with all the training subdirectories"
    val_files_path = yaml_config['loaders']['val']['file_paths']
    assert len(val_files_path) == 1, "we assume that it is a directory with all the training subdirectories"
    train_file_path = train_files_path[0]
    val_file_path = val_files_path[0]
    
    train_files = os.listdir(train_file_path)
    val_files = os.listdir(val_file_path)
    train_files = [os.path.join(train_file_path, f) for f in train_files]
    val_files = [os.path.join(val_file_path, f) for f in val_files]
    yaml_config['loaders']['train']['file_paths'] = train_files
    yaml_config['loaders']['val']['file_paths'] = val_files
            
    # convert yaml_config to string
    config = yaml.dump(yaml_config)
    return config