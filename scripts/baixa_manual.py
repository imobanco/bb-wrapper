from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper


wrapper = CobrancasBBWrapper()


for number in range(9999999999):
    print(f'Dando baixa no {number}...')
    try:
        response = wrapper.baixa_boleto(wrapper.build_our_number(number))
        print(response)
    except Exception as e:
        print(e)
