import logging 
from datetime import datetime
import os
log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_path = os.path.join(os.getcwd(),'Logs',log_file)

os.makedirs(log_path,exist_ok=True)

log_File_path = os.path.join(log_path,log_file)

logging.basicConfig(
    filename=log_File_path,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,


)

