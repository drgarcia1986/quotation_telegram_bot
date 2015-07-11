# -*- coding: utf-8 -*-


class InvalidCurrency(Exception):
    def __init__(self, currency):

        self.currency = currency
        self.msg = (
            'Não foi possível encontrar a cotação de {}'.format(currency)
        )
