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
    
    All logs are now centralized in the 'data/logs' directory.
    
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
        # Ensure the log directory exists
        Path("data/logs").mkdir(parents=True, exist_ok=True)
        
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

    # Centralize module-specific activity logs in 'data/logs/'
    if module_name and module_name not in ('root', '__main__'):
        logger = logging.getLogger(module_name)
        
        # Check if a file handler already exists for this logger to avoid duplicates
        has_file_handler = any(
            isinstance(h, RotatingFileHandler) and 'activity.log' in str(h.baseFilename) 
            for h in logger.handlers
        )
        
        if not has_file_handler:
            # Base directory for all logs
            log_dir = Path.cwd() / "data" / "logs"
            
            # Create a path based on module hierarchy (e.g., 'a.b' -> 'data/logs/a/b/')
            module_log_dir = log_dir / Path(*module_name.split('.'))
            
            # Ensure the directory exists
            try:
                module_log_dir.mkdir(parents=True, exist_ok=True)
                log_file = module_log_dir / 'activity.log'
                
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
                # Fallback if file or directory cannot be created
                logging.getLogger(__name__).warning(f"Could not create dynamic log for {module_name} in {module_log_dir}: {e}")
