import logging.config
import yaml
import inspect
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from personal_manager.core.config import get_log_dir

_config_loaded = False

def setup_logging(module_name=None, config_path=None):
    """
    Setup logging configuration from a YAML file and automatically add 
    a module-specific activity log.
    
    All logs are stored in the user-configured log directory.
    
    Args:
        module_name (str, optional): The name of the module. If None, it is 
                                    automatically detected from the caller.
        config_path (str, optional): Path to the YAML configuration file.
    """
    global _config_loaded
    
    # Automatically detect the calling module's name if not provided
    if module_name is None:
        stack = inspect.stack()
        if len(stack) > 1:
            caller_frame = stack[1].frame
            module_name = caller_frame.f_globals.get('__name__')

    # Get the user-configured logs directory
    log_dir = get_log_dir()

    # Load global configuration once
    if not _config_loaded:
        # Resolve the logging configuration YAML file
        if config_path is not None:
            config_file = Path(config_path)
        else:
            # If running in PyInstaller bundle, look under sys._MEIPASS
            if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
                config_file = Path(sys._MEIPASS) / "personal_manager" / "logging_config.yaml"
            else:
                config_file = Path(__file__).parent / "logging_config.yaml"

        if config_file.exists():
            try:
                # Ensure the main log directory exists
                log_dir.mkdir(parents=True, exist_ok=True)
                
                with config_file.open('r', encoding='utf-8') as f:
                    config = yaml.safe_load(f.read())
                    
                    # Dynamically update global log handler file path
                    if 'handlers' in config and 'file' in config['handlers']:
                        app_errors_log = log_dir / 'app_errors.log'
                        config['handlers']['file']['filename'] = str(app_errors_log)
                        
                    logging.config.dictConfig(config)
                _config_loaded = True
            except Exception as e:
                # Fallback to stderr logging if configuration loading fails
                logging.basicConfig(level=logging.INFO)
                logging.getLogger(__name__).warning(f"Failed to load logging config {config_file}: {e}")
                _config_loaded = True
        else:
            # Fallback if config file is missing
            logging.basicConfig(level=logging.INFO)
            logging.getLogger(__name__).warning(f"Logging configuration not found at {config_file}. Using basic config.")
            _config_loaded = True

    # Centralize module-specific activity logs under the configured log_dir
    if module_name and module_name not in ('root', '__main__'):
        logger = logging.getLogger(module_name)
        
        # Check if a file handler already exists for this logger to avoid duplicates
        has_file_handler = any(
            isinstance(h, RotatingFileHandler) and 'activity.log' in str(h.baseFilename) 
            for h in logger.handlers
        )
        
        if not has_file_handler:
            # Create a path based on module hierarchy (e.g., 'a.b' -> '<log_dir>/a/b/')
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
                
                # Match the format defined in logging_config.yaml
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
