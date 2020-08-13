import time

start_time = time.time()

from app.log import logger

from app import model,view,controller

logger.debug("--- Import in %s seconds ---" % (time.time() - start_time))
