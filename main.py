# -*- coding: utf-8 -*-

import argparse
from sanic import Sanic, Blueprint
from sanic.request import Request
from lib.wexin_service.client import wx_client
from lib.middleware import qr_performance_middleware, response_middleware
from lib.base import collection, fine

parser = argparse.ArgumentParser()
parser.add_argument("--host", dest="host", action="store", type=str, default="0.0.0.0",
                    help="host")
parser.add_argument("--port", dest="port", action="store", type=int, default=8868,
                    help="port")
parser.add_argument("--show_response", dest="show_response", action="store", type=bool, default=True,
                    help="是否打开response打印信息")
parser.add_argument("--load_performance_middleware", dest="load_qr_performance_middleware",
                    action="store", type=bool, default=False,
                    help="是否需要加载门店码全链路测试中间件")
args, other_args = parser.parse_known_args()


ULR_PREFIX = "sanic"

common_blueprint = Blueprint("common_blueprint", url_prefix=ULR_PREFIX)


@common_blueprint.route("/state/<state>", methods=["GET"])
async def get_ratio_of_val(req: Request, state):
    return fine(result=collection.get_state_info(state))


@common_blueprint.route("/state/<state>/<val>/<weight>", methods=["GET"])
async def set_ratio_of_val(req: Request, state, val, weight):
    return fine(result=collection.set_ratio_of_val(state_name=state, val=val, weight=weight))


@common_blueprint.route("/whitelist/<state>/<val>/", methods=["GET"])
async def whitelist(req:Request, state, val):
    return fine(result=collection.whitelist(state, val))


def main():
    sc = Sanic(__name__)
    sc.blueprint(common_blueprint)

    clients = [wx_client]
    # load blueprint
    sc.blueprint(clients)

    if args.load_qr_performance_middleware:
        sc.register_middleware(qr_performance_middleware)

    if args.show_response:
        sc.register_middleware(response_middleware, attach_to="response")

    sc.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()



