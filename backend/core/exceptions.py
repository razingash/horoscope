"""custom exceptions and logging"""
import logging


custom_logger = logging.getLogger('custom_logger')
custom_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('logs.log', encoding='utf-8')
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s (%(asctime)s): %(message)s [%(filename)s]', datefmt='%d/%m/%Y %H:%M:%S')
handler.setFormatter(formatter)
custom_logger.addHandler(handler)

