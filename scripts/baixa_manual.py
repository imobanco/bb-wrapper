import logging
import threading
from time import sleep

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper


wrapper = CobrancasBBWrapper()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)-15s| %(threadName)-10s| %(levelname)-5s| %(message)s",
)

number_of_threads = 13


def baixa_slice(start, step):
    logger = logging.getLogger(__name__)
    for number in range(start, 9999999999, step):
        logger.info(f"Dando baixa no {number}...")
        try:
            response = wrapper.baixa_boleto(wrapper.build_our_number(number))
            sleep(1)
            logger.info(f"{number} {response}")
        except Exception as e:
            logger.info(f"{number} {e}")


threads = []

for i in range(number_of_threads):
    start_index = i
    thread = threading.Thread(
        target=baixa_slice, name=f"thread-{i}", args=[start_index, number_of_threads]
    )
    threads.append(thread)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
