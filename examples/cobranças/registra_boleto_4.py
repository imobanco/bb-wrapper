import os

from examples.utils import dump_response

from bb_wrapper.wrapper.cobrancas import CobrancasBBWrapper

wrapper = CobrancasBBWrapper()

data = {
    "numeroConvenio": 3128557,
    "numeroCarteira": 17,
    "numeroVariacaoCarteira": 35,
    "codigoModalidade": 1,
    "dataEmissao": "07.12.2020",
    "dataVencimento": "07.12.2020",
    "valorOriginal": 100.00,
    "quantidadeDiasProtesto": 0,
    "indicadorNumeroDiasLimiteRecebimento": "N",
    "numeroDiasLimiteRecebimento": 0,
    "codigoAceite": "A",
    "codigoTipoTitulo": 4,
    "descricaoTipoTitulo": "DS",
    "indicadorPermissaoRecebimentoParcial": "N",
    "numeroTituloBeneficiario": "TESTE2",
    "textoCampoUtilizacaoBeneficiario": "TESTE3",
    "numeroTituloCliente": "00031285571231230012",
    "textoMensagemBloquetoOcorrencia": "TESTE5",
    "pagador": {
        "tipoRegistro": 1,
        "numeroRegistro": "71128590182",
        "nome": "NOME",
        "endereco": "ENDERECO",
        "cep": "70675727",
        "cidade": "SAO PAULO",
        "bairro": "CENTRO",
        "uf": "SP",
        "telefone": "999939669",
    },
    "avalista": {
        "tipoRegistro": 1,
        "numeroRegistro": "71128590182",
        "nomeRegistro": "NOME",
    },
    "jurosMora": {"tipo": 1, "valor": 0.1},
    "multa": {"tipo": 2, "porcentagem": 0.1, "data": "08.12.2020"},
}

response = wrapper.registra_boleto(data)

dump_response(response, os.path.basename(__file__).split(".")[0])
