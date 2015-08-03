# -*- coding: utf-8 -*-
import asyncio

import aiohttp
from exceptions import InvalidCurrency
from telegram import bot
from utils import get_quotation, logger


@bot.command(r'(/start|/?help|/info)')
def help_cmd(message, **kwargs):
    logger.debug('running command help')
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


@bot.command(r'/cota\w{2}o (?P<currency>\w+)')
def quotation_cmd(message, currency, **kwargs):
    logger.info('running command quotation for currency: {}'.format(currency))
    try:
        quotation = yield from get_quotation(currency)
        message.reply(
            '$1 {} vale R${}'.format(currency, quotation)
        )
    except InvalidCurrency as e:
        logger.error('invalid currency: {}'.format(currency))
        message.reply(e.msg)


@bot.command(r'/cota\w{2}o')
def quotation_without_currency_cmd(message, **kwargs):
    logger.info('running command quotation with currency')
    msg = """
Eu preciso que você me informe a moeda que você deseja a cotação,
por exemplo /cotação dolar

ps: você também pode usar sem a acentuação e cedilha,
por exemplo: /cotacao euro
    """
    message.reply(msg)


if __name__ == '__main__':
    try:
        bot.run()
    except KeyboardInterrupt:
        bot.stop()
