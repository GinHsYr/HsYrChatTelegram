import logging
from bot.utils import configLoader

def setupLogger():
    configs = configLoader.Config()
    logFile = configs.loggingFileName

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    fileHandler = logging.FileHandler(logFile, mode="a")
    fileHandler.setLevel(logging.INFO)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    fileHandler.setFormatter(formatter)
    fileHandler.stream.reconfigure(encoding="utf-8")
    consoleHandler.setFormatter(formatter)

    logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger

logger = setupLogger()
