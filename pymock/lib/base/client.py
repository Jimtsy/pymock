# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from pymock.utils import SingletonIfSameParameters
from sanic import Blueprint


def is_json_rpc_request(method, body: dict):
    if method == "POST" and body.get("jsonrpc"):
        return True
    else:
        return False


class BaseClient(Blueprint):
    __metaclass__ = ABCMeta

    def __init__(self, name, url_prefix=None, **kwargs):
        super().__init__(name, url_prefix=url_prefix, **kwargs)

    @abstractmethod
    def list_all_status(self):
        pass

    def register_middleware(self, middleware):
        self.middleware(middleware)


class RPCTreeHandler(metaclass=SingletonIfSameParameters):
    # todo: 如果单实例对性能有多大影响？

    def __init__(self, url):
        self._url = url
