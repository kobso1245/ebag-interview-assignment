import configparser
import os

def read_config():
    # run the configuration
    env = os.environ.get('ENV', 'LOCAL')
    config = configparser.ConfigParser()
    config.read(f'src/confs/conf_{env}/settings.cfg')
    if not config.sections():
        raise ValueError('Error: Not support env provided. Valid options are: [LOCAL]')
    
    return config

def build_db_config():
    config = read_config()
    return {
        "connections": {
            "default": f"{config.get('database', 'type')}://{config.get('database', 'filename')}"
        },
        "apps": {
            "models": {
                "models": ["src.db.models"],
                "default_connection": "default",
                "migrations": "src.db.migrations"
            }
        }
    }
    
CONFIG = build_db_config()