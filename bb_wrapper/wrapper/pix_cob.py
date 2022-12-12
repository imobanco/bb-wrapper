from .bb import BaseBBWrapper
from ..models.perfis import TipoInscricaoEnum
from ..models.pix_cob import CobrancaPix
from ..services.pixcode import PixCodeService


class PIXCobBBWrapper(BaseBBWrapper):
    """
    Wrapper da API PIX de cobranças (recebimento na conta berço)
    """

    SCOPE = "cob.read cob.write pix.read pix.write"

    BASE_DOMAIN = ".bb.com.br/pix/v1"

    def listar_pix(self, inicio=None, fim=None, page=0):
        """
        Método para consultar todos os pix recebidos.

        Args:
            inicio: filtro de data inicio. Respeita o formato definido na RFC 3339
            fim: filtro de data final. Respeita o formato definido na RFC 3339
            page: número da página atual. Padrão 0
        """
        search = {
            "paginaAtual": page,
        }
        if inicio:
            search["inicio"] = inicio
        if fim:
            search["fim"] = fim

        url = self._construct_url("pix", end_bar=False, search=search)

        response = self._get(url)

        return response

    def consultar_pix(self, end_to_end_id):
        """
        Método para consultar um pix recebido.

        Args:
            end_to_end_id: identificador end_to_end do pix
        """
        url = self._construct_url("pix", end_to_end_id)

        response = self._get(url)

        return response

    def devolver_pix(self, end_to_end_id, valor, txid):
        """
        Método para devolver uma quantia de um pix recebido.

        Args:
            end_to_end_id: identificador end_to_end do pix
            valor: valor a ser devolvido (formato float vulgo 10.00 para R$ 10,00)
            txid: identificador único da devolução
        """
        url = self._construct_url("pix", end_to_end_id, "devolucao", txid)

        response = self._put(url, {"valor": valor})

        return response

    def consultar_devolucao_pix(self, end_to_end_id, txid):
        """
        Método para consultar uma devolução feita.

        Args:
            end_to_end_id: identificador end_to_end do pix
            txid: identificador único da devolução
        """
        url = self._construct_url("pix", end_to_end_id, "devolucao", txid)

        response = self._get(url)

        return response

    def _create_and_validate_cobranca_data(
        self,
        expiracao: int,
        chave: str,
        documento_devedor: str,
        nome_devedor: str,
        valor: float,
        descricao: str,
        info: list = None,
    ):
        """
        Criar a estrutura de uma cobrança PIX

        Args:
            expiracao: segundos antes da expiracao
            chave: chave PIX
            documento_devedor: CPF ou CNPJ
            nome_devedor: Nome do devedor
            valor: valor da cobrança
            descricao: descrição da cobrança
        """
        tipo_documento = None
        if len(documento_devedor) == 11:
            tipo_documento = TipoInscricaoEnum.cpf.name
        elif len(documento_devedor) == 14:
            tipo_documento = TipoInscricaoEnum.cnpj.name

        if tipo_documento is None:
            raise ValueError("Tipo de documento não identificado!")

        data = {
            "calendario": {"expiracao": expiracao},
            "valor": {"original": valor},
            "devedor": {tipo_documento: documento_devedor, "nome": nome_devedor},
            "chave": chave,
            "solicitacaoPagador": descricao,
        }
        if info is not None:
            data["infoAdicionais"] = info

        CobrancaPix(**data)
        return data

    def _injeta_qrcode_data(self, response, nome_recebedor):
        (
            response.data["qrcode_data"],
            response.data["qrcode_b64"],
        ) = PixCodeService().create(response.data["location"], nome_recebedor)

    def criar_cobranca(
        self,
        expiracao: int,
        chave: str,
        documento_devedor: str,
        nome_devedor: str,
        nome_recebedor: str,
        valor: float,
        descricao: str,
        info: list = None,
    ):
        """
        Criar uma cobrança PIX

        Args:
            expiracao: segundos antes da expiracao
            chave: chave PIX
            documento_devedor: CPF ou CNPJ
            nome_devedor: Nome do devedor
            nome_recebedor: Nome do recebedor
            valor: valor da cobrança
            descricao: descrição da cobrança
            info: lista de informações adicionais
        """
        data = self._create_and_validate_cobranca_data(
            expiracao, chave, documento_devedor, nome_devedor, valor, descricao, info
        )

        url = self._construct_url("cob", end_bar=True)

        response = self._put(url, data)

        self._injeta_qrcode_data(response, nome_recebedor)

        return response

    def criar_cobranca_qrcode(
        self,
        expiracao: int,
        chave: str,
        documento_devedor: str,
        nome_devedor: str,
        nome_recebedor: str,
        valor: float,
        descricao: str,
        info: list = None,
    ):
        """
        Criar uma cobrança PIX com QRCode dinâmico

        Args:
            expiracao: segundos antes da expiracao
            chave: chave PIX
            documento_devedor: CPF ou CNPJ
            nome_devedor: Nome do devedor
            nome_recebedor: Nome do recebedor
            valor: valor da cobrança
            descricao: descrição da cobrança
        """
        data = self._create_and_validate_cobranca_data(
            expiracao, chave, documento_devedor, nome_devedor, valor, descricao, info
        )

        url = self._construct_url("cobqrcode", end_bar=True)

        response = self._put(url, data)

        self._injeta_qrcode_data(response, nome_recebedor)

        return response

    def consultar_cobranca(self, txid):
        """
        Consultar uma cobrança PIX

        Args:
            txid: identificador único da cobrança
        """
        url = self._construct_url("cob", txid)

        response = self._get(url)

        return response
