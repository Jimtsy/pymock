# -*- coding: utf-8 -*-

import threading
from sanic.request import Request
from sanic.response import HTTPResponse
from pymock.log import logger

lock = threading.Condition()

async def qr_performance_middleware(req: Request):
    """
    全链路压测中间件，检测faker标示记录请求各下游是否为压测流程
    :param req:
    :return:
    """
    print(req.url, "\n", req.json)
    print(req.headers)

async def response_middleware(req: Request, response: HTTPResponse):
    logger.info("response - body: {}".format(str(response.body, encoding="utf-8")))
