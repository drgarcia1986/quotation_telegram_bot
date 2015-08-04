# -*- coding: utf-8 -*-
import os
import logging


# LOG CONF
LOGGING = {
    'filename': 'cotacaobot.log',
    'level': logging.WARNING,
    'maxBytes': 50 * 1024 * 1024,  # 50 MB
    'backupCount': 5,
    'format': '%(levelname)s %(asctime)s %(name)s %(module)s %(message)s',
    'logentries_token': os.environ.get('LOGENTRIES_TOKEN')
}


# BOT CONF
BOT_TOKEN = os.environ.get('BOT_TOKEN')
REGEX_BASE = r'<input type="text" id="nacional" value="(?P<quote>[^"]+)"/>'
QUOTATIONS = {
    'dolar': ('http://dolarhoje.com/', REGEX_BASE),
    'dolar australiano': ('http://dolarhoje.com/australiano/', REGEX_BASE),
    'dolar canadense': ('http://dolarhoje.com/canadense/', REGEX_BASE),
    'libra': ('http://librahoje.com/', REGEX_BASE),
    'euro': ('http://eurohoje.com/', REGEX_BASE),
    'peso': ('http://pesohoje.com/', REGEX_BASE),
    'peso chileno': ('http://pesohoje.com/chileno/', REGEX_BASE),
    'peso uruguaio': ('http://pesohoje.com/uruguaio/', REGEX_BASE)
}

QUOTATIONS_LIST = list(QUOTATIONS.keys())

SUPORTED_QUOTATIONS = (
    ', '.join(QUOTATIONS_LIST[:-1]) + ' e ' + QUOTATIONS_LIST[-1]
)
