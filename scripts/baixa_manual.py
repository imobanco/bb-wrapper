from threading import Thread

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper


wrapper = CobrancasBBWrapper()


number_of_threads = 5
threads = []


def baixa_boletos(index):
    for number in range(index, 9999999999, number_of_threads):
        print(f"Dando baixa no {number}...")
        try:
            response = wrapper.baixa_boleto(wrapper.build_our_number(number))
            print(number, response)
        except Exception as e:
            print(number, e)


for i in range(number_of_threads):
    start_index = i + 0
    t = Thread(target=baixa_boletos, args=[start_index])
    t.start()
    threads.append(t)

for t in threads:
    t.join()
