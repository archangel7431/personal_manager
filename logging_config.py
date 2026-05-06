import logging.config
import yaml
import inspect
from pathlib import Path
from logging.handlers import RotatingFileHandler

_config_loaded = False

def setup_logging(module_name=None, config_path='logging_config.yaml'):
    """
    Setup logging configuration from a YAML file and automatically add 
    a module-specific activity log.
    
    Args:
        module_name (str, optional): The name of the module. If None, it is 
                                    automatically detected from the caller.
        config_path (str): Path to the YAML configuration file.
    """
    global _config_loaded
    
    # Automatically detect the calling module's name if not provided
    if module_name is None:
        stack = inspect.stack()
        if len(stack) > 1:
            caller_frame = stack[1].frame
            module_name = caller_frame.f_globals.get('__name__')

    # Load global configuration once
    if not _config_loaded:
        config_file = Path(config_path)
        if config_file.exists():
            with config_file.open('r') as f:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
            _config_loaded = True
        else:
            # Fallback if config file is missing
            logging.basicConfig(level=logging.INFO)
            _config_loaded = True

    # If a module name is detected/provided, add a specific activity log
    if module_name and module_name not in ('root', '__main__'):
        logger = logging.getLogger(module_name)
        
        # Check if a file handler already exists for this logger to avoid duplicates
        has_file_handler = any(
            isinstance(h, RotatingFileHandler) and 'activity.log' in str(h.baseFilename) 
            for h in logger.handlers
        )
        
        if not has_file_handler:
            # Convert module name to a directory path (e.g., 'a.b' -> Path('a/b'))
            module_dir = Path(*module_name.split('.'))
            
            # Ensure the directory exists before creating the log file
            if module_dir.is_dir():
                log_file = module_dir / 'activity.log'
                
                try:
                    handler = RotatingFileHandler(
                        log_file, 
                        maxBytes=5242880, # 5 MB
                        backupCount=5, 
                        encoding='utf-8'
                    )
                    handler.setLevel(logging.DEBUG)
                    
                    # Match the format defined in logging.yaml
                    formatter = logging.Formatter(
                        '{asctime} - {name} - {levelname} - {message}', 
                        style='{', 
                        datefmt='%Y-%m-%d  %H:%M:%S'
                    )
                    handler.setFormatter(formatter)
                    
                    logger.addHandler(handler)
                except Exception as e:
                    # Fallback if file cannot be created
                    logging.getLogger(__name__).warning(f"Could not create dynamic log for {module_name}: {e}")
