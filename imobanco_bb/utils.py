import logging


def get_logger(name):
    """
    factory de Logger's

    Args:
        name: nome para gerar o logger

    Returns:
        novo logger para imobanco_bb.{name}
    """
    return logging.getLogger(f"imobanco_bb.{name}")
