import logging
import logging.handlers

# create file handler which logs even debug messages
fh = logging.handlers.RotatingFileHandler('scraping_main.log', maxBytes=104857, backupCount=3)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)


