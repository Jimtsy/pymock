from sanic.request import Request
from sanic.response import json

from lib.base import RPCTreeHandler, BaseClient, is_json_rpc_request
from lib.base.response import bad_request, fine
from lib.wexin_service.status import __all__
from .model import WXServiceRequest, \
    new_get_user_summary_response, \
    new_get_user_cumulate_response, \
    new_get_open_ids_response,\
    new_get_user_info_response


class _FansJSONRPCHandler(RPCTreeHandler):

    def __init__(self, url):
        super().__init__(url)
        self._url = url

    def __call_rpc_method__(self, method, req_params: list):
        if not isinstance(req_params, list) and len(req_params) != 1:
            return bad_request("error rpc method")
        return getattr(self, method)(req_params[0])

    def getUserSummary(self, req_param: dict):
        """ 获取用户增减数据

        :param req_param:
        :return:
        """
        req = WXServiceRequest(**req_param)
        return json(new_get_user_summary_response(req))

    def getUserCumulate(self, req_param):
        """ 获取用户累计统计数据

        :param req_param:
        :return:
        """
        req = WXServiceRequest(**req_param)
        return json(new_get_user_cumulate_response(req))

    def getOpenIds(self, req_param):
        """ 获取openid列表

        :param req_param:
        :return:
        """
        # req = WXServiceRequest(**req_param)
        return json(new_get_open_ids_response())

    def getUserInfos(self, req_param):
        """ 获取粉丝详情

        :return:
        """
        req = WXServiceRequest(**req_param)
        return json(new_get_user_info_response(req))


async def handle_rpc_request(req: Request):
    """ RPC Method Handler

    :param req:
    :return:
    """
    b = req.json
    if is_json_rpc_request(req.method, b):
        _b_get = b.get
        method = _b_get("method")
        params = _b_get("params")
        if not all([method, params]):
            return fine(msg="invalid request")

        handler = _FansJSONRPCHandler(req.url)
        if not hasattr(handler, method):
            return fine(msg="not found")
        else:
            return handler.__call_rpc_method__(method=method, req_params=params)


class WXServiceClient(BaseClient):
    def __init__(self, name, url_prefix="/"):
        super().__init__(name, url_prefix)
        self.registered_middleware = []

    def list_all_status(self):
        return __all__

wx_client = WXServiceClient("微信", "/wx_service")
wx_client.add_route(handle_rpc_request, uri="/rpc/datacude/", methods=["POST"])
wx_client.add_route(handle_rpc_request, uri="/rpc/user/", methods=["POST"])


        

