import logging


def _get_logger(name):
    """
    factory de Logger's

    Args:
        name: nome para gerar o logger

    Returns:
        novo logger para bb_wrapper.{name}
    """
    return logging.getLogger(f"bb_wrapper.{name}")
