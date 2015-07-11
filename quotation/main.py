# -*- coding: utf-8 -*-
import asyncio

import aiohttp
from exceptions import InvalidCurrency
from telegram import bot
from utils import get_quotation


@bot.command(r'(/start|/?help)')
def help_cmd(message, **kwargs):
    msg = """
Olá, posso verificar para você a cotação de algumas moedas em relação ao real.

Atualmente conheço a cotação das seguintes moedas:
Dolar, Euro e Libra

Veja um exemplo de como ver a cotação:
/cotação dolar


Esse é um projeto OpenSource
criado por @drgarcia1986

O código fonte está disponivel em:
https://github.com/drgarcia1986/quotation_telegram_bot
    """
    message.reply(msg)


@bot.command(r'(/cotação|/cotacao) (?P<currency>\w+)')
def quotation_cmd(message, currency, **kwargs):
    try:
        quotation = yield from get_quotation(currency)
        message.reply(
            '$1 {} vale R${}'.format(currency, quotation)
        )
    except InvalidCurrency as e:
        message.reply(e.msg)


if __name__ == '__main__':
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.stop()
