# -*- coding: utf-8 -*-

from sanic.response import json


def _basic_template(msg, result, status=200, **kwargs):
    return json(dict(msg=msg, result=result, **kwargs), status=status)


def bad_request(msg=None, **kwargs):
    """
    bad request response
    :param msg:
    :param kwargs:
    :return:
    """
    msg = "bad request" if not msg else msg
    return _basic_template(msg=msg, result=None, status=400, **kwargs)


def fine(msg=None, result=None, **kwargs):
    """

    :param msg:
    :param result:
    :param kwargs:
    :return:
    """
    msg = "success" if not msg else msg
    return _basic_template(msg=msg, result=result, status=200, **kwargs)