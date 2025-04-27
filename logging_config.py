import logging.config
import yaml

def setup_logging(config_path='logging_config.yaml'):
    """
    Setup logging configuration from a YAML file.
    
    Args:
        config_path (str): Path to the YAML configuration file.
    """
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(config)

