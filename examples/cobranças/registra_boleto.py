from imobanco_bb.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

data = {
    "numeroConvenio": 3128557,
    "numeroCarteira": 17,
    "numeroVariacaoCarteira": 35,
    "codigoModalidade": 1,
    "dataEmissao": "07.12.2020",
    "dataVencimento": "07.12.2020",
    "valorOriginal": 100.00,
    "valorAbatimento": 0,
    "quantidadeDiasProtesto": 0,
    "indicadorNumeroDiasLimiteRecebimento": "N",
    "numeroDiasLimiteRecebimento": 0,
    "codigoAceite": "A",
    "codigoTipoTitulo": 4,
    "descricaoTipoTitulo": "DS",
    "indicadorPermissaoRecebimentoParcial": "N",
    "numeroTituloBeneficiario": "TESTE2",
    "textoCampoUtilizacaoBeneficiario": "TESTE3",
    "codigoTipoContaCaucao": 0,
    "numeroTituloCliente": "00031285571231230001",
    "textoMensagemBloquetoOcorrencia": "TESTE5",
    "pagador": {
        "tipoRegistro": 1,
        "numeroRegistro": 71128590182,
        "nome": "NOME",
        "endereco": "ENDERECO",
        "cep": 70675727,
        "cidade": "SAO PAULO",
        "bairro": "CENTRO",
        "uf": "SP",
        "telefone": "999939669",
    },
    "email": "cliente@email.com",
}

response = wrapper.registra_boleto(data)

print(response.data)
