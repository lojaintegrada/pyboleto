# -*- coding: utf-8 -*-
"""
Gerar arquivo no formato Cnab240 para envio ao banco
"""

from cnab240.tipos import Arquivo
from pyboleto.data import BoletoException

class Remessa(object):

	def __init__(self):
		self.arquivo = None

	def iniciar_arquivo(self, boleto, **kwargs):
		if not hasattr(boleto, 'banco') or boleto.banco is None:
			raise BoletoException(
							u'Este banco não possui implementação para CNAB240')
		data = boleto.dicionario_cnab240
		data.update(kwargs)
		self.arquivo = Arquivo(boleto.banco, **data)

	def adicionar_boleto(self, boleto, **kwargs):
		if self.arquivo is None:
			self.iniciar_arquivo(boleto, **kwargs)

		data = boleto.dicionario_cnab240
		data.update(kwargs)
		self.arquivo.incluir_cobranca(**data)

	def gerar_arquivo(self, nome_arquivo):
		f = open(nome_arquivo, 'w')
		self.arquivo.escrever(f)
		f.close()
