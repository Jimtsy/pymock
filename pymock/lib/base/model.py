# -*- coding: utf-8 -*-

from sanic.response import json, text, raw, html, http
"""
一个接口server，req model， res model, 支持动态生成

"""


class _Request:
    def __init__(self, *args, **kwargs):
        pass


class JsonParamsRequest(_Request):
    def __init__(self, **kwargs):
        super().__init__()
        self._marshal(**kwargs)

    def _marshal(self, **kwargs):
        [setattr(self, k, v) for k, v in kwargs.items()]


class ListParamsRequest(_Request):
    def __init__(self, *args):
        super().__init__(*args)

    def _marshal(self, *args):
        pass


class Response:
    def json(self, **kwargs):
        return json(body=kwargs)

    def xml(self, **kwargs):
        pass
