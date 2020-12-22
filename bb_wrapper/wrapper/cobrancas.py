from .bb import BaseBBWrapper
from ..constants import CONVENIO, CARTEIRA, VARIACAO_CARTEIRA
from ..models.boleto import Boleto


class CobrancasBBWrapper(BaseBBWrapper):
    def __init__(self, convenio=None, carteira=None, variacao_carteira=None, **kwargs):
        super().__init__(**kwargs)

        if convenio is None:
            convenio = CONVENIO

        if carteira is None:
            carteira = CARTEIRA

        if variacao_carteira is None:
            variacao_carteira = VARIACAO_CARTEIRA

        assert len(convenio) == 7, "O convênio não possui 7 dígitos!"
        self.__convenio = convenio
        self.__carteira = carteira
        self.__variacao_carteira = variacao_carteira

    def _construct_base_url(self):
        base_url = super()._construct_base_url()
        base_url += "/cobrancas/v1/boletos"
        return base_url

    def registra_boleto(self, data):
        """"""
        Boleto(**data)
        self.authenticate()
        url = self._construct_url()
        response = self._post(url, data)
        return response

    def consulta_boleto(self, our_number):
        """"""

        assert len(our_number) == 20, "O nósso número não tem 20 dígitos!"

        self.authenticate()
        url = self._construct_url(
            identifier=our_number, search={"numeroConvenio": self.__convenio}
        )
        response = self._get(url)
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
        default_data = {
            "numeroConvenio": self.__convenio,
            "numeroCarteira": self.__carteira,
            "numeroVariacaoCarteira": self.__variacao_carteira,
            "codigoModalidade": 1,  # SIMPLES (4 seria split!)
            "quantidadeDiasProtesto": 0,  # 0 dias para protestar!
            "indicadorNumeroDiasLimiteRecebimento": "N",  # SEM tolerância
            "numeroDiasLimiteRecebimento": 0,  # SEM tolerância
            "codigoAceite": "N",  # Boleto não reconhecido pelo pagador
            "codigoTipoTitulo": 4,  # convênio tipo 4 (cliente numera, emite e expede)
            "indicadorPermissaoRecebimentoParcial": "N",  # sem recibimento parcial!
            "descricaoTipoTitulo": "DM",  # tipo de cobrança, Duplicata Mercantil
        }
        default_data.update(data)
        return default_data
