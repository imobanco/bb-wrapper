Cliente não oficial feito em Python, para realizar integração com a API do Banco do Brasil.

`Documentação oficial do BB <https://developers.bb.com.br/>`_

Instalando
===========

Nosso pacote está hospedado no `PyPI <https://pypi.org/project/bb-wrapper/>`_

.. code-block:: bash

    pip install bb-wrapper



Configuração
==================
Para utilizar o `zoop-wrapper` é necessário ter duas constantes/variáveis. sendo elas:

.. code-block:: python
    IMOBANCO_BB_IS_SANDBOX='flag True ou False para indicar utilização de sandbox ou não'
    IMOBANCO_BB_BASIC_TOKEN='chave de autenticação gerada para a aplicação no site developers.bb'
    IMOBANCO_BB_GW_APP_KEY='chave de desenvolvimento gerada para a aplicação no site developers.bb'

    IMOBANCO_BB_CONVENIO='convênio do contrato para geração de boletos'
    IMOBANCO_BB_CARTEIRA='carteira do contrato para geração de boletos'
    IMOBANCO_BB_VARIACAO_CARTEIRA='variação da carteira do contrato para geração de boletos
    IMOBANCO_BB_AGENCIA='agência da conta berço do contrato para geração de boletos'
    IMOBANCO_BB_CONTA='nº da conta berço do contrato para geração de boletos'


Recomendamos criar um arquivo `.env` contendo essas varíaveis de ambiente.

Podem ser criadas diretamente no terminal (não recomendado).

Podem ser criadas também diretamente no `arquivo.py`

.. danger::

    Fazer isso além de não ser recomendado é uma **FALHA** de segurança.

Recursos disponíveis
=====================

- ☑ API de Cobrança (geração de boletos)
- ☑ API PIX (recebimento PIX) {essa API ainda está instável e incompleta no BB}
- ☑ Geração de imagem b64
- ☑ Geração e validação de código de barras de boleto
- ☐ Geração e validação de código de barras de convênio
- ☑ Geração de QR Code PIX
