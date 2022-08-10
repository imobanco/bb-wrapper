Cliente não oficial feito em Python, para realizar integração com as API's do Banco do Brasil.

`Documentação oficial do BB <https://developers.bb.com.br/>`_

Instalando
===========

Nosso pacote está hospedado no `PyPI <https://pypi.org/project/bb-wrapper/>`_

.. code-block:: bash

    pip install bb-wrapper



Configuração
==================
Para utilizar o `bb-wrapper` é necessário ter algumas constantes/variáveis. sendo elas:

.. code-block:: python

    IMOBANCO_BB_IS_SANDBOX='flag True ou False para indicar utilização de sandbox ou não'
    IMOBANCO_BB_BASIC_TOKEN='chave de autenticação gerada para a aplicação no site developers.bb'
    IMOBANCO_BB_GW_APP_KEY='chave de desenvolvimento gerada para a aplicação no site developers.bb'


Para geração de boletos é necessário:

.. code-block:: python

    IMOBANCO_BB_CONVENIO='convênio do contrato para geração de boletos'
    IMOBANCO_BB_CARTEIRA='carteira do contrato para geração de boletos'
    IMOBANCO_BB_VARIACAO_CARTEIRA='variação da carteira do contrato para geração de boletos
    IMOBANCO_BB_AGENCIA='agência da conta berço do contrato para geração de boletos'
    IMOBANCO_BB_CONTA='nº da conta berço do contrato para geração de boletos'


Recomendamos criar um arquivo `.env` contendo essas varíaveis de ambiente.

::

    Podem ser criadas diretamente no terminal (não recomendado).

    Podem ser criadas também diretamente no `arquivo.py` (não recomendado).

Recursos disponíveis
=====================

API's
---------------------

- ☑ API de Cobrança (geração de boletos)
- ☑ API PIX (recebimento PIX) {essa API ainda está instável e incompleta no BB}
- ☐ API Arrecadação PIX {sem previsão de implementação}
- ☑ API Lotes de Pagamentos {essa API ainda está instável e incompleta no BB}

  - ☐ Transferência PIX
  - ☑ Transferência Bancária
  - ☐ Pagamento GPS
  - ☐ Pagamento GRU
  - ☐ Pagamento DARF Preto
  - ☑ Pagamento Tributos
  - ☑ Pagamento Boletos

Recursos auxiliares
-------------------

- ☑ Geração de imagem b64
- ☑ Geração, validação e conversão de código de barras de boleto
- ☑ Geração, validação e conversão de código de barras de tributos
- ☑ Geração de QR Code PIX
- ☑ Validação e limpeza de CPF/CNPJ

Exemplos disponíveis
=====================
Existem exemplos de utilização da biblioteca na pasta `examples`.

Preparando ambiente de desenvolvimento
=======================================

> O Nix é utilizado para gerenciar os pacotes necessários, por exemplo como a versão correta do python.

Certifique-se que o ambiente está ativado, se não estiver execute:

.. code-block:: bash

    nix develop

