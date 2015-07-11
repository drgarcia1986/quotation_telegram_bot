# -*- coding: utf-8 -*-
import asyncio
import re

import aiohttp

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
