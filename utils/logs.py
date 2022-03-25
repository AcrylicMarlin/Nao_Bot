import logging


log_format = (
        '%(asctime)s - '
        '%(name)s - '
        '%(funcName)s - '
        '%(levelname)s - '
        '%(message)s'
)

def setup_logging(name:str):
    
    logging.basicConfig(format=log_format)
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(log_format)

    infoFH = logging.FileHandler('logs/Nao_Bot.info.log')
    infoFH.setLevel(logging.INFO)
    infoFH.setFormatter(formatter)
    logger.addHandler(infoFH)

    warnFH = logging.FileHandler('logs/Nao_Bot.warn.log')
    warnFH.setLevel(logging.WARNING)
    warnFH.setFormatter(formatter)
    logger.addHandler(warnFH)

    errorFH = logging.FileHandler('logs/Nao_Bot.error.log')
    errorFH.setLevel(logging.ERROR)
    errorFH.setFormatter(formatter)
    logger.addHandler(errorFH)


    return logger
    