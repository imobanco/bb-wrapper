from .bb import BaseBBWrapper
from ..constants import CONVENIO, CARTEIRA, VARIACAO_CARTEIRA, AGENCIA, CONTA
from ..models.boleto import Boleto
from ..services import parse_unicode_to_alphanumeric, BarcodeService, QRCodeService


class CobrancasBBWrapper(BaseBBWrapper):
    def __init__(
        self,
        convenio=None,
        carteira=None,
        variacao_carteira=None,
        agencia=None,
        conta=None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        if convenio is None:
            convenio = CONVENIO

        if carteira is None:
            carteira = CARTEIRA

        if variacao_carteira is None:
            variacao_carteira = VARIACAO_CARTEIRA

        if carteira is None:
            carteira = CARTEIRA

        if agencia is None:
            agencia = AGENCIA

        if conta is None:
            conta = CONTA

        assert len(convenio) == 7, "O convênio não possui 7 dígitos!"
        self.__convenio = convenio
        self.__carteira = carteira
        self.__variacao_carteira = variacao_carteira
        self.__agencia = agencia
        self.__conta = conta

    def _construct_base_url(self):
        base_url = super()._construct_base_url()
        base_url += "/cobrancas/v2/boletos"
        return base_url

    def _injeta_b64_images(self, response):
        """"""
        response.data["codigo_barras_b64"] = BarcodeService().generate_barcode_b64image(
            response.data["codigoBarraNumerico"]
        )

        qr_code = response.data.get("qrCode")
        if qr_code:
            response.data["qrCode"]["b64"] = QRCodeService().generate_qrcode_b64image(
                qr_code["emv"]
            )

    def registra_boleto(self, data):
        """"""
        Boleto(**data)
        self.authenticate()
        url = self._construct_url()
        response = self._post(url, data)
        self._injeta_b64_images(response)
        return response

    def consulta_boleto(self, our_number):
        """"""

        assert len(our_number) == 20, "O nósso número não tem 20 dígitos!"

        self.authenticate()
        url = self._construct_url(
            our_number, search={"numeroConvenio": self.__convenio}
        )
        response = self._get(url)
        return response

    def lista_boletos(self, query=None, liquidados_flag=True):
        """"""
        indicadorSituacao = "B" if liquidados_flag else "A"
        query_data = {
            "indicadorSituacao": indicadorSituacao,
            "agenciaBeneficiario": self.__agencia,
            "contaBeneficiario": self.__conta,
        }
        if query is not None:
            query_data.update(query)
        self.authenticate()
        url = self._construct_url(search=query_data)
        response = self._get(url)
        return response

    def baixa_boleto(self, our_number):
        """"""
        self.authenticate()
        url = self._construct_url(our_number, "baixar")

        data = {"numeroConvenio": self.__convenio}

        response = self._post(url, data)
        return response

    def build_our_number(self, number):
        """
        Método para construir o 'Nosso Número'.

        20 dígitos, que deverá ser formatado da seguinte forma:
            '000' + (número do convênio com 7 dígitos) + (10 algarismos)
        """
        number = str(number)
        number = number.zfill(10)

        assert len(number) == 10, "O número não tem 10 dígitos!"

        return f"000{self.__convenio}{number}"

    def create_boleto_data_with_defaults(self, data: dict):
        """
        Método para criar um dict com algumas infos padrões.

        É uma função pura, retornando um novo dict!

        Esse novo dict possui as infos padrões + dados do original,
        dando prioridade às infos do dict original (sim, ele sobreescreve as padrões!)
        """
        fields_to_transliterate = [
            "textoCampoUtilizacaoBeneficiario",
            "textoMensagemBloquetoOcorrencia",
        ]

        default_data = {
            "numeroConvenio": self.__convenio,
            "numeroCarteira": self.__carteira,
            "numeroVariacaoCarteira": self.__variacao_carteira,
            "codigoModalidade": 1,  # SIMPLES (4 seria split!)
            "quantidadeDiasProtesto": 0,  # 0 dias para protestar!
            "indicadorAceiteTituloVencido": "S",  # COM tolerância
            "numeroDiasLimiteRecebimento": 0,  # 0 dias de tolerância
            "codigoAceite": "N",  # Boleto não reconhecido pelo pagador
            "codigoTipoTitulo": 4,  # convênio tipo 4 (cliente numera, emite e expede)
            "indicadorPermissaoRecebimentoParcial": "N",  # sem recibimento parcial!
            "descricaoTipoTitulo": "DM",  # tipo de cobrança, Duplicata Mercantil
            "indicadorPix": "S",  # PIX para o pagamento!
        }
        default_data.update(data)

        for field in fields_to_transliterate:
            try:
                default_data[field] = parse_unicode_to_alphanumeric(default_data[field])
            except KeyError:
                pass
        return default_data
