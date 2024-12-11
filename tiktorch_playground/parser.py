from tiktorch.trainer import TrainerYamlParser
from tiktorch_playground.utils import expand_loaders_path

def parse():
    yaml_config_path = './3d_unet_lightseet_boundary/unet_config_train.yaml'
    config = expand_loaders_path(yaml_config_path)
    
    with open('./unet_config_parsed.yaml', 'w') as f:
        f.write(config)
    
    parser = TrainerYamlParser(config)
    parser.parse()
    
if __name__ == "__main__":
    parse()