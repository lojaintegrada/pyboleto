#-*- coding: utf-8 -*-
from ..data import BoletoData, custom_property


class BoletoCaixa(BoletoData):
    '''
        Gera Dados necessários para criação de boleto para o banco Caixa
        Economica Federal

    '''

    agencia_cedente = custom_property('agencia_cedente', 4)
    conta_cedente = custom_property('conta_cedente', 6)
    # nosso_numero = custom_property('nosso_numero', 10)

    def __init__(self):
        super(BoletoCaixa, self).__init__()
        self.codigo_banco = "104"
        self.local_pagamento = u"Preferencialmente nas Casas Lotéricas e Agências da Caixa"
        self.logo_image = "logo_bancocaixa.jpg"

    @property
    def dv_nosso_numero(self):
        resto2 = self.modulo11(self.nosso_numero.split('-')[0], 9, 1)
        digito = 11 - resto2
        if digito in [10, 11]:
            return 0
        return digito

    @property
    def campo_livre(self):
        content = "%10s%4s%11s" % (self.nosso_numero,
                                   self.agencia_cedente,
                                   self.conta_cedente.split('-')[0])
        return content

    def format_nosso_numero(self):
        return "{}-{}".format(self.nosso_numero, str(self.dv_nosso_numero))


class BoletoCaixaV2(BoletoCaixa):
    """
        Gera Dados necessários para criação de boleto para o banco Caixa
        Economica Federal ( Nosso número maior que 10 dígitos )
    """
    nosso_numero = custom_property('nosso_numero', 16)
    agencia_cedente = custom_property('agencia_cedente', 4)
    conta_cedente = custom_property('conta_cedente', 6)

    def __init__(self, inicio_nosso_numero):
        super(BoletoCaixaV2, self).__init__()
        self.inicio_nosso_numero = inicio_nosso_numero

    @property
    def dv_nosso_numero(self):
        resto2 = self.modulo11('{}{}'.format(self.inicio_nosso_numero, self.nosso_numero.split('-')[0]), 9, 1)
        digito = 11 - resto2
        if digito in [10, 11]:
            return 0
        return digito

    @property
    def campo_livre(self):
        content = str("%1s%6s%2s%16s" % (self.inicio_nosso_numero[1],
                                         self.conta_cedente.split('-')[0],
                                         self.inicio_nosso_numero,
                                         self.nosso_numero))
        return content

    def format_nosso_numero(self):
        return '{}{}-{}'.format(self.inicio_nosso_numero, self.nosso_numero, str(self.dv_nosso_numero))


class BoletoCaixaSIGCB(BoletoCaixa):
    """
        Gera Dados necessários para criação de boleto para o banco Caixa
        Economica Federal - SIGCB
    """

    nosso_numero = custom_property('nosso_numero', 15)
    agencia_cedente = custom_property('agencia_cedente', 4)
    conta_cedente = custom_property('conta_cedente', 6)

    def __init__(self, inicio_nosso_numero='24'):
        super(BoletoCaixaSIGCB, self).__init__()
        self.inicio_nosso_numero = inicio_nosso_numero

    @property
    def dv_conta_cedente(self):
        resto2 = self.modulo11(self.conta_cedente.split('-')[0], 9, 1)
        digito = 11 - resto2
        if digito in [10, 11]:
            return 0
        return digito

    @property
    def agencia_conta_cedente(self):
        return "{} / {}-{}".format(
            self.agencia_cedente,
            self.conta_cedente.split('-')[0],
            self.dv_conta_cedente)


    @property
    def campo_livre(self):
        content = "{}{}{}{}{}{}{}".format(
            self.conta_cedente.split('-')[0],
            self.dv_conta_cedente,
            self.nosso_numero[:3],
            self.inicio_nosso_numero[0:1],
            self.nosso_numero[3:6],
            self.inicio_nosso_numero[1:2],
            self.nosso_numero[6:15]
        )
        return str("{}{}".format(content, self._dv_num(content)))

    def _dv_num(self, num):
        resto2 = self.modulo11(num.split('-')[0], 9, 1)
        digito = 11 - resto2
        if digito in [10, 11]:
            return 0
        return digito

    def format_nosso_numero(self):
        nnum = "{}{}{}{}".format(
            self.inicio_nosso_numero[0:2],
            self.nosso_numero[:3],
            self.nosso_numero[3:6],
            self.nosso_numero[6:15]
        )
        nossonumero = '{}{}'.format(nnum, self._dv_num(nnum))
        return nossonumero
