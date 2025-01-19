#!/bin/bash/python3
from worker import worker
from logger import logger

if __name__ == "__main__":
    logger.logger.info('Started')
    main = worker.ScrappingThread()
    main.start()
    main.join()
