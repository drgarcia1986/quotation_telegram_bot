# -*- coding: utf-8 -*-
import asyncio

import aiohttp
import re

import settings


class Message:

    def __init__(self, bot, **data):
        self.bot = bot
        self._data = data
        self.text = data['text']
        self.chat_id = data['chat']['id']
        self.is_group = 'title' in self._data['chat']
        self.message_id = data['message_id']
        self.sender = data['from'].get('username', data['from']['first_name'])

    def reply(self, text):
        asyncio.async(
            self.bot.api_call(
                action='sendMessage',
                chat_id=self.chat_id,
                text=text,
                disable_web_page_preview='true',
                reply_to_message_id=self.message_id
            )
        )


class Bot:

    API_URL = 'https://api.telegram.org'
    API_TIMEOUT = 60

    def __init__(self, token, loop=None):
        self.token = token
        self._running = False
        self._commands = []
        self.loop = (
            loop if loop else asyncio.get_event_loop()
        )

    def _api_url(self, action):
        return '{api}/bot{token}/{action}'.format(
            api=self.API_URL,
            token=self.token,
            action=action
        )

    @asyncio.coroutine
    def _process_message(self, message):
        if 'text' not in message:
            return
        for pattern, handler in self._commands:
            match = re.search(pattern, message['text'])
            if match:
                return handler(
                    Message(self, **message),
                    **match.groupdict()
                )

    @asyncio.coroutine
    def _check_update_loop(self):
        offset = 0
        while self._running:
            resp = yield from self.api_call(
                'getUpdates',
                offset=offset + 1,
                timeout=self.API_TIMEOUT
            )
            if not resp:
                offset += 1
                continue

            for update in resp['result']:
                offset = max(offset, update['update_id'])
                asyncio.async(self._process_message(update['message']))

    @asyncio.coroutine
    def api_call(self, action, **data):
        url = self._api_url(action)
        resp = yield from aiohttp.request('POST', url, data=data)
        try:
            return (yield from resp.json())
        except ValueError:
            return

    def command(self, regex):
        def decorator(func):
            self._commands.append((regex, func))
            return func
        return decorator

    def run(self):
        self._running = True
        self.loop.run_until_complete(self._check_update_loop())

    def stop(self):
        self._running = False
        self.loop.close()


bot = Bot(settings.BOT_TOKEN)
