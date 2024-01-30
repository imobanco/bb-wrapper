from .bb import BaseBBWrapper
from ..models.pagamentos import (
    TransferenciaTED,
    Boleto,
    Tributo,
    LoteData,
    LoteTransferenciaData,
    LiberarPagamentos,
    TransferenciaChavePIX,
    TransferenciaDadosBancariosPIX,
)
from ..services.document import DocumentoService
from ..services.barcode import BarcodeService


class PagamentoLoteBBWrapper(BaseBBWrapper):
    """
    Wrapper da API Pagamentos em Lote
    """

    SCOPE = "pagamentos-lote.lotes-requisicao pagamentos-lote.transferencias-info pagamentos-lote.transferencias-requisicao pagamentos-lote.cancelar-requisicao pagamentos-lote.devolvidos-info pagamentos-lote.lotes-info pagamentos-lote.pagamentos-guias-sem-codigo-barras-info pagamentos-lote.pagamentos-info pagamentos-lote.pagamentos-guias-sem-codigo-barras-requisicao pagamentos-lote.pagamentos-codigo-barras-info pagamentos-lote.boletos-requisicao pagamentos-lote.guias-codigo-barras-info pagamentos-lote.guias-codigo-barras-requisicao pagamentos-lote.boletos-info pagamentos-lote.transferencias-pix-requisicao pagamentos-lote.transferencias-pix-info pagamentos-lote.pix-info"  # noqa

    BASE_PROD_ADDITION = "-ip"
    BASE_DOMAIN = ".bb.com.br/pagamentos-lote/v1"

    def _valida_lote_data(self, model, **kwargs):
        try:
            if kwargs["convenio"] is None:
                kwargs.pop("convenio")
        except KeyError:
            pass
        model(**kwargs)

    ##########################
    #  Lotes & Pagamentos    #
    ##########################

    def cancelar_pagamentos(self, _id, agencia, conta, dv_conta, convenio=None):
        """
        Args:
            _id: identificador do pagamento
            agencia: agência bancária
            conta: conta bancária
            dv_conta: dígito verificador da conta bancária
            convenio: nº do convênio/contrato
        """
        self._valida_lote_data(
            LoteData,
            n_requisicao=_id,
            agencia=agencia,
            conta=conta,
            dv_conta=dv_conta,
            convenio=convenio,
        )

        url = self._construct_url("cancelar-pagamentos")

        data = {
            "agenciaDebito": agencia,
            "contaCorrenteDebito": conta,
            "digitoVerificadorContaCorrente": dv_conta,
            "listaPagamentos": [{"codigoPagamento": _id}],
        }
        if convenio is not None:
            data["numeroContratoPagamento"] = convenio

        response = self._post(url, data)

        return response

    def liberar_pagamentos(self, n_requisicao, indicador_float="N"):
        """
        Args:
            n_requisicao: número da requisição
            indicador_float: Indicador de confirmação/concordância quanto ao
                pagamento da tarifa de antecipação de float a ser calculada posteriormente  # noqa: E501
        """
        url = self._construct_url("liberar-pagamentos")

        data = {"numeroRequisicao": n_requisicao, "indicadorFloat": indicador_float}
        LiberarPagamentos(**data)

        response = self._post(url, data)

        return response

    def resgatar_lote(self, n_requisicao):
        """
        Consulta um lote de pagamento

        Args:
            n_requisicao: Nº da requisição do lote
        """
        url = self._construct_url(n_requisicao)

        response = self._get(url)

        return response

    def resgatar_lote_solicitacao(self, n_requisicao):
        """
        Consulta a solicitação de um lote de pagamento

        Args:
            n_requisicao: Nº da requisição do lote
        """
        url = self._construct_url(n_requisicao, "solicitacao")

        response = self._get(url)

        return response

    def listar_pagamentos(self, inicio, fim, status=None, index=0):
        """
        Lista os pagamentos

        Args:
            inicio: Data inicio da consulta no formato ddmmaaaa
            fim: Data final da consulta no formato ddmmaaaa
            status: Status a ser consultado
            index: Índice da consulta
        """
        search = {
            "dataInicio": inicio,
            "dataFim": fim,
            "indice": index,
        }
        if status:
            search["estadoPagamento"] = status

        url = self._construct_url("pagamentos", search=search)

        response = self._get(url)

        return response

    ######################
    #  Transferências    #
    ######################

    def _criar_dados_transferencia(
        self,
        n_requisicao,
        agencia,
        conta,
        dv_conta,
        codigo_banco,
        agencia_destino,
        conta_destino,
        dv_conta_destino,
        documento,
        data_transferencia,
        valor_transferencia,
        descricao,
        finalidade_ted=1,
        tipo_pagamento=128,
        convenio=None,
    ):
        self._valida_lote_data(
            LoteTransferenciaData,
            n_requisicao=n_requisicao,
            agencia=agencia,
            conta=conta,
            dv_conta=dv_conta,
            tipo_pagamento=tipo_pagamento,
            convenio=convenio,
        )

        lote_data = {
            "numeroRequisicao": n_requisicao,
            "agenciaDebito": agencia,
            "contaCorrenteDebito": conta,
            "digitoVerificadorContaCorrente": dv_conta,
            "tipoPagamento": tipo_pagamento,
        }
        if convenio is not None:
            lote_data["numeroContratoPagamento"] = convenio

        documento = DocumentoService().valida(documento)
        documento_tipo = DocumentoService().identifica_tipo(documento)

        pagamento_data = {
            "numeroCOMPE": codigo_banco,
            "agenciaCredito": agencia_destino,
            "contaCorrenteCredito": conta_destino,
            "digitoVerificadorContaCorrente": dv_conta_destino,
            "dataTransferencia": data_transferencia,
            "valorTransferencia": valor_transferencia,
            "descricaoTransferencia": descricao,
        }
        if documento_tipo == 1:
            pagamento_data["cpfBeneficiario"] = documento
        else:
            pagamento_data["cnpjBeneficiario"] = documento
        if int(codigo_banco) != 1:
            """
            Só é utilizado finalidade TED para outros bancos
            que não sejam o BB!

            O código do BB é 1!
            """
            pagamento_data["codigoFinalidadeTED"] = finalidade_ted

        TransferenciaTED(**pagamento_data)

        return {**lote_data, "listaTransferencias": [{**pagamento_data}]}

    def cadastrar_transferencia(
        self,
        n_requisicao,
        agencia,
        conta,
        dv_conta,
        codigo_banco,
        agencia_destino,
        conta_destino,
        dv_conta_destino,
        documento,
        data_transferencia,
        valor_transferencia,
        descricao,
        finalidade_ted=1,
        tipo_pagamento=128,
        convenio=None,
    ):
        """
        Cadastra uma transferência bancária

        Args:
            n_requisicao: Nº da requisição a ser utilizado. Deve ser único
            agencia: Agência da conta de origem do pagamento
            conta: Nº da conta de origem do pagamento
            dv_conta: DV da conta de origem do pagamento
            tipo_pagamento: Tipo de pagamento a ser feito (126, 127 ou 128)
            codigo_banco: Nº do banco destino
            agencia_destino: Agência da conta de destino do pagamento
            conta_destino: Nº da conta de destino do pagamento
            dv_conta_destino: DV da conta de destino do pagamento
            documento: CPF/CNPJ do recebedor
            data_transferencia: Data do pagamento. No formato "ddmmyyyy"
            valor_transferencia: Valor do pagamento
            descricao: Descrição do pagamento
            finalidade_ted: Tipo de transferência a ser feita (1, 6 ou 11)
            convenio: Nº do convênio/contrato
        """
        data = self._criar_dados_transferencia(
            n_requisicao,
            agencia,
            conta,
            dv_conta,
            codigo_banco,
            agencia_destino,
            conta_destino,
            dv_conta_destino,
            documento,
            data_transferencia,
            valor_transferencia,
            descricao,
            finalidade_ted,
            tipo_pagamento,
            convenio,
        )

        url = self._construct_url("lotes-transferencias")

        response = self._post(url, data)

        return response

    def consultar_transferencia(self, _id):
        url = self._construct_url("transferencias", _id)

        response = self._get(url)

        return response

    ###############
    #  Boletos    #
    ###############

    def _criar_dados_pagamento_boleto(
        self,
        n_requisicao,
        agencia,
        conta,
        dv_conta,
        codigo_barras_ou_linha_digitavel,
        documento,
        data_pagamento,
        valor_pagamento,
        valor_nominal,
        descricao,
        convenio=None,
    ):
        self._valida_lote_data(
            LoteData,
            n_requisicao=n_requisicao,
            agencia=agencia,
            conta=conta,
            dv_conta=dv_conta,
            convenio=convenio,
        )

        lote_data = {
            "numeroRequisicao": n_requisicao,
            "numeroAgenciaDebito": agencia,
            "numeroContaCorrenteDebito": conta,
            "digitoVerificadorContaCorrenteDebito": dv_conta,
        }
        if convenio is not None:
            lote_data["codigoContrato"] = convenio

        documento = DocumentoService().valida(documento)
        documento_tipo = DocumentoService().identifica_tipo(documento)
        codigo_barras = (
            BarcodeService().identify(codigo_barras_ou_linha_digitavel).barcode
        )

        pagamento_data = {
            "numeroCodigoBarras": codigo_barras,
            "codigoTipoBeneficiario": documento_tipo,
            "documentoBeneficiario": documento,
            "dataPagamento": data_pagamento,
            "valorPagamento": valor_pagamento,
            "valorNominal": valor_nominal,
            "descricaoPagamento": descricao,
        }
        Boleto(**pagamento_data)

        return {**lote_data, "lancamentos": [{**pagamento_data}]}

    def cadastrar_pagamento_boleto(
        self,
        n_requisicao,
        agencia,
        conta,
        dv_conta,
        codigo_barras_ou_linha_digitavel,
        documento,
        data_pagamento,
        valor_pagamento,
        valor_nominal,
        descricao,
        convenio=None,
    ):
        """
        Cadastra o pagamento de um boleto

        Args:
            n_requisicao: Nº da requisição a ser utilizado. Deve ser único
            agencia: Agência da conta de origem do pagamento
            conta: Nº da conta de origem do pagamento
            dv_conta: DV da conta de origem do pagamento
            codigo_barras_ou_linha_digitavel: Linha digitável ou código de barras do boleto  # noqa: E501
            documento: CPF/CNPJ do recebedor
            data_pagamento: Data do pagamento. No formato "ddmmyyyy"
            valor_pagamento: Valor do pagamento
            valor_nominal: Valor nominal da conta (valor original?)
            descricao: Descrição do pagamento
            convenio: Nº do convênio/contrato
        """
        data = self._criar_dados_pagamento_boleto(
            n_requisicao,
            agencia,
            conta,
            dv_conta,
            codigo_barras_ou_linha_digitavel,
            documento,
            data_pagamento,
            valor_pagamento,
            valor_nominal,
            descricao,
            convenio,
        )

        url = self._construct_url("lotes-boletos")

        response = self._post(url, data)

        return response

    def consultar_pagamento_boleto(self, _id):
        url = self._construct_url("boletos", _id)

        response = self._get(url)

        return response

    ################
    #  Tributos    #
    ################

    def _criar_dados_pagamento_tributo(
        self,
        n_requisicao,
        agencia,
        conta,
        dv_conta,
        codigo_barras_ou_linha_digitavel,
        data_pagamento,
        valor_pagamento,
        descricao,
        convenio=None,
    ):
        self._valida_lote_data(
            LoteData,
            n_requisicao=n_requisicao,
            agencia=agencia,
            conta=conta,
            dv_conta=dv_conta,
            convenio=convenio,
        )

        lote_data = {
            "numeroRequisicao": n_requisicao,
            "numeroAgenciaDebito": agencia,
            "numeroContaCorrenteDebito": conta,
            "digitoVerificadorContaCorrenteDebito": dv_conta,
        }
        if convenio is not None:
            lote_data["codigoContrato"] = convenio

        codigo_barras = (
            BarcodeService().identify(codigo_barras_ou_linha_digitavel).barcode
        )

        pagamento_data = {
            "codigoBarras": codigo_barras,
            "dataPagamento": data_pagamento,
            "valorPagamento": valor_pagamento,
            "descricaoPagamento": descricao,
        }
        Tributo(**pagamento_data)

        return {**lote_data, "lancamentos": [{**pagamento_data}]}

    def cadastrar_pagamento_tributo(
        self,
        n_requisicao,
        agencia,
        conta,
        dv_conta,
        codigo_barras_ou_linha_digitavel,
        data_pagamento,
        valor_pagamento,
        descricao,
        convenio=None,
    ):
        """
        Cadastra o pagamento de um tributo

        Args:
            n_requisicao: Nº da requisição a ser utilizado. Deve ser único
            agencia: Agência da conta de origem do pagamento
            conta: Nº da conta de origem do pagamento
            dv_conta: DV da conta de origem do pagamento
            codigo_barras_ou_linha_digitavel: Linha digitável ou código de barras do boleto  # noqa: E501
            data_pagamento: Data do pagamento. No formato "ddmmyyyy"
            valor_pagamento: Valor do pagamento
            descricao: Descrição do pagamento
            convenio: Nº do convênio/contrato
        """
        data = self._criar_dados_pagamento_tributo(
            n_requisicao,
            agencia,
            conta,
            dv_conta,
            codigo_barras_ou_linha_digitavel,
            data_pagamento,
            valor_pagamento,
            descricao,
            convenio,
        )

        url = self._construct_url("lotes-guias-codigo-barras")

        response = self._post(url, data)

        return response

    def consultar_pagamento_tributo(self, _id):
        url = self._construct_url("guias-codigo-barras", _id)

        response = self._get(url)

        return response

    ################
    #     PIX      #
    ################

    def _criar_dados_transferencia_chave_pix(
        self,
        n_requisicao,
        agencia,
        conta,
        dv_conta,
        data_transferencia,
        valor_transferencia,
        chave,
        descricao,
        tipo_pagamento,
        documento,
    ):
        lote_data = {
            "numeroRequisicao": n_requisicao,
            "agenciaDebito": agencia,
            "contaCorrenteDebito": conta,
            "digitoVerificadorContaCorrente": dv_conta,
            "tipoPagamento": tipo_pagamento,
        }
        transferencia_data = {
            "documento": documento,
            "data": data_transferencia,
            "valor": valor_transferencia,
            "descricaoPagamento": descricao,
            "chave": chave,
        }

        transferencia_data = TransferenciaChavePIX(**transferencia_data).dict()
        return {**lote_data, "listaTransferencias": [transferencia_data]}

    def criar_transferencia_por_chave_pix(
        self,
        n_requisicao,
        agencia,
        conta,
        dv_conta,
        data_transferencia,
        valor_transferencia,
        chave,
        descricao="",
        tipo_pagamento=128,
        documento=None,
    ):
        """
        Efetua pagamentos em lote via tranferência PIX

        Args:
            n_requisicao: Nº da requisição a ser utilizado. Deve ser único
            agencia: Agência da conta de origem do pagamento
            conta: Nº da conta de origem do pagamento
            dv_conta: DV da conta de origem do pagamento
            tipo_pagamento: Tipo de pagamento a ser feito (126, 127 ou 128)
            data_transferencia: Data do pagamento. No formato "ddmmyyyy"
            valor_transferencia: Valor do pagamento
            chave: Valor corresponde a chave que sera usada para tranferência # noqa: E501
            documento:  Valor que corresponde ao CPF/CNPJ
                - Opcional e serve para validar que a chave aleatória/email/telefone pertencem ao cpf/cnpj # noqa: E501
                - Deve ser validado e contratado com o gerente BB/suporte da API
            descricao: Campo de uso livre pelo cliente
        """
        data = self._criar_dados_transferencia_chave_pix(
            n_requisicao,
            agencia,
            conta,
            dv_conta,
            data_transferencia,
            valor_transferencia,
            chave,
            descricao,
            tipo_pagamento,
            documento,
        )
        url = self._construct_url("lotes-transferencias-pix")
        response = self._post(url, data)

        return response

    def _criar_dados_transferencia_dados_bancarios_pix(
        self,
        n_requisicao,
        agencia,
        conta,
        dv_conta,
        data_transferencia,
        valor_transferencia,
        tipo_conta_favorecido,
        agencia_favorecido,
        conta_favorecido,
        digito_verificador_conta,
        conta_pagamento,
        descricao,
        tipo_pagamento,
        documento,
        numero_ispb,
    ):
        lote_data = {
            "numeroRequisicao": n_requisicao,
            "agenciaDebito": agencia,
            "contaCorrenteDebito": conta,
            "digitoVerificadorContaCorrente": dv_conta,
            "tipoPagamento": tipo_pagamento,
        }
        transferencia_data = {
            "documento": documento,
            "data": data_transferencia,
            "valor": valor_transferencia,
            "descricaoPagamento": descricao,
            "tipoConta": tipo_conta_favorecido,
            "agencia": agencia_favorecido,
            "conta": conta_favorecido,
            "digitoVerificadorConta": digito_verificador_conta,
            "contaPagamento": conta_pagamento,
            "numeroISPB": numero_ispb,
        }

        transferencia_data = TransferenciaDadosBancariosPIX(**transferencia_data).dict()
        return {**lote_data, "listaTransferencias": [transferencia_data]}

    def criar_transferencia_por_dados_bancarios_pix(
        self,
        n_requisicao,
        agencia,
        conta,
        dv_conta,
        data_transferencia,
        valor_transferencia,
        tipo_conta_favorecido,
        agencia_favorecido,
        conta_favorecido,
        digito_verificador_conta,
        numero_ispb,
        conta_pagamento=None,
        descricao="",
        tipo_pagamento=128,
        documento=None,
    ):
        """
        Efetua pagamentos em lote via tranferência PIX

        Args:
            n_requisicao: Nº da requisição a ser utilizado. Deve ser único
            agencia: Agência da conta de origem do pagamento
            conta: Nº da conta de origem do pagamento
            dv_conta: DV da conta de origem do pagamento
            tipo_pagamento: Tipo de pagamento a ser feito (126, 127 ou 128)
            data_transferencia: Data do pagamento. No formato "ddmmyyyy"
            valor_transferencia: Valor do pagamento
            tipo_conta_favorecido: Tipo de conta de crédito do favorecido
                - 1 Conta Corrente
                - 2 Conta Pagamento
                - 3 Conta Poupança
            agencia_favorecido: Número da agência da conta de crédito do favorecido.
            conta_favorecido: Número da conta de crédito do favorecido
            digito_verificador_conta: Dígito verificador da agência da conta de crédito do favorecido   # noqa: E501
            numero_ispb: Identificador de Sistema de Pagamento Brasileiro
            conta_pagamento: Número da conta pagamento do favorecido
            descricao: Campo de uso livre pelo cliente
            documento:  Valor que corresponde ao CPF/CNPJ
                - Obrigatório e serve para validar que os dados bancários pertencem ao cpf/cnpj # noqa: E501
        """
        data = self._criar_dados_transferencia_dados_bancarios_pix(
            n_requisicao,
            agencia,
            conta,
            dv_conta,
            data_transferencia,
            valor_transferencia,
            tipo_conta_favorecido,
            agencia_favorecido,
            conta_favorecido,
            digito_verificador_conta,
            conta_pagamento,
            descricao,
            tipo_pagamento,
            documento,
            numero_ispb,
        )
        url = self._construct_url("lotes-transferencias-pix")
        response = self._post(url, data)

        return response

    def consultar_pix(self, _id):
        """
        - Consulta os dados de um pagamento efetuado na modalidade PIX.
        """

        url = self._construct_url("pix", _id)
        response = self._get(url)
        return response
