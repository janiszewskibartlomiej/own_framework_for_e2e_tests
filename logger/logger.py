import logging
import os.path
from datetime import datetime

dir_path = os.path.dirname(__file__)

logger = logging.getLogger('sqlalchemy.engine')
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

today = datetime.today()
file_handler = logging.FileHandler(
    f'{dir_path}{os.sep}logs{os.sep}strava_web_scrapping_{today.strftime("%Y_%m_%d_%H_%M")}.log', mode='a',
    encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
