# -*- coding: utf-8 -*-
import asyncio
import logging
import logging.handlers
import re

import aiohttp
from logentries import LogentriesHandler

import settings
from exceptions import InvalidCurrency


@asyncio.coroutine
def get_quotation(currency):
    quotation_config = settings.QUOTATIONS.get(currency.lower())
    if not quotation_config:
        raise InvalidCurrency(currency)
    url, regex = quotation_config
    response = yield from aiohttp.request('GET', url)
    response = yield from response.text()
    quotation = re.search(regex, response)
    return quotation.group(1)


# log
logging.basicConfig(
    level=settings.LOGGING['level'],
    format=settings.LOGGING['format']
)
logger = logging.getLogger('cotacao.bot')

# File Handler
logger.addHandler(
    logging.handlers.RotatingFileHandler(
        settings.LOGGING['filename'],
        maxBytes=settings.LOGGING['maxBytes'],
        backupCount=settings.LOGGING['backupCount']
    )
)

# Logentries Handler
logger.addHandler(
    LogentriesHandler(settings.LOGGING['logentries_token'])
)
