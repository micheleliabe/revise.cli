import yaml
from utils.logger import log

# Load configs from config file


def load_configs(file='config.yml'):
    with open(file, 'r') as file:
        config = yaml.safe_load(file)
    return config
