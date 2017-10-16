import logging

from functools import partial

import requests

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


class To:

    def __init__(self, hooks=None):

        self._root = 'https://hooks.slack.com/services'
        self._hooks = hooks or {}
        self._targets = []
        self._partial = []

        self._verify()

    def __call__(self, msg):

        if self._partial:
            raise Exception('Invalid target: "{}".'.format(
                '.'.join(self._partial)
            ))

        targets = self._flush()
        self._send_all(targets, msg)

    def __getattr__(self, attr):

        if self._partial:
            self._partial.append(attr)
            attr = '.'.join(self._partial)

        if attr not in self._hooks:

            if not self._partial:
                self._partial.append(attr)

            return self

        self._targets.append(
            '{}/{}'.format(self._root, self._hooks[attr])
        )

        self._partial = []

        return self

    def __getitem__(self, item):

        return getattr(self, item)

    def _verify(self):

        for k, v in self._hooks.items():
            if v.startswith('https://'):
                raise Exception('Invalid hook for "{}": "{}".'.format(
                    k, v
                ))

    @classmethod
    def _send_all(cls, channels, msg):

        for chan in channels:
            try:
                cls._send(chan, msg)
            except Exception as ex:
                print('Could not send message to "{}": {}'.format(chan, ex))

    def _flush(self):

        targets = set(self._targets[:])
        self._targets = []

        return targets

    @classmethod
    def _send(cls, chan, msg):

        _log.debug('Sending "{}" to "{}"...'.format(
            msg, chan
        ))
        r = requests.post(
            chan,
            json={"text": msg}
        )

        if r.status_code != 200:

            try:
                msg = r.json()
            except:
                msg = r.text

            raise Exception(msg)


def freeze(to):

    targets = to._flush()

    return partial(
        To._send_all,
        targets
    )
