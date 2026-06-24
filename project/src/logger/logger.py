#!/usr/bin/python3
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="main.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)


def main():
    logger.info("Started")
    logger.info("Finished")


if __name__ == "__main__":
    main()
