from tiktorch.trainer import TrainerYamlParser
from tiktorch_playground.utils import expand_loaders_path

def parse():
    yaml_config_path = '/home/katzalis/kreshuklab/ilastik-playground/tiktorch_playground/2d_unet_dsb_2018/unet_config_train.yaml'
    
    to_expand = False
    
    if to_expand:
        config = expand_loaders_path(yaml_config_path)
        
        with open('./unet_config_parsed.yaml', 'w') as f:
            f.write(config)
    else:
        with open(yaml_config_path, 'r') as f:
            config = f.read()
    
    parser = TrainerYamlParser(config)
    parser.parse()
    
if __name__ == "__main__":
    parse()