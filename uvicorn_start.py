
import os
import uvicorn

from src.utils.conf import read_config

CONFIG = read_config()

if __name__ == "__main__":
    # create the file dir, if not exists
    os.makedirs(CONFIG.get('general', 'files_dir'), exist_ok=True)
    
    # initiate the uvicorn server
    uvicorn.run(
        "src.main:app",
        host=CONFIG.get('server', 'host'),
        port=CONFIG.getint('server', 'port'),
        workers=CONFIG.getint('server', 'workers'),
        reload=CONFIG.getboolean('server', 'reload', fallback=False)
    )
