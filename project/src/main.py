#!/usr/bin/python3
from logger import logger
from worker import worker

if __name__ == "__main__":
    logger.logger.info("Started")
    main = worker.ScrapingThread()
    main.start()
    main.join()
