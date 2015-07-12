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
    'libra': ('http://librahoje.com/', REGEX_BASE),
    'euro': ('http://eurohoje.com/', REGEX_BASE)
}
