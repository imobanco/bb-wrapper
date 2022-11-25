import threading
from multiprocessing import Process

from bb_wrapper.wrapper import PIXCobBBWrapper


def run_process():
    def run_thread():
        c = PIXCobBBWrapper()
        c.listar_pix(page=0)

    threads = [
        threading.Thread(target=run_thread)
        for i in range(3)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


while True:
    ps = [
        Process(target=run_process)
        for i in range(10)
    ]

    for p in ps:
        p.start()

    for p in ps:
        p.join(timeout=6)
        if p.exitcode is None:
            print('vou matar', str(p))
            p.kill()

    print('Estou tentando novamente!')
