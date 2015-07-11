# -*- coding: utf-8 -*-
import os


BOT_TOKEN = os.environ.get('BOT_TOKEN')
REGEX_BASE = r'<input type="text" id="nacional" value="(?P<quote>[^"]+)"/>'
QUOTATIONS = {
    'dolar': ('http://dolarhoje.com/', REGEX_BASE),
    'libra': ('http://librahoje.com/', REGEX_BASE),
    'euro': ('http://eurohoje.com/', REGEX_BASE)
}
