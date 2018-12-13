import random
import faker
import time
import queue
from datetime import datetime, timedelta
from sanic.response import HTTPResponse
from lib.base.response import bad_request
from lib.base.state import collection
from functools import lru_cache
from utils import Counter, gen_rand_str
from .status import \
    stateWXServiceUserSources, stateWXServiceSubscribe, \
    stateWXServiceSex, stateWXServiceSubscribeScene

try:
    from ujson import dumps
except BaseException:
    from json import dumps


counter = Counter("open_id_counter")
fake = faker.Factory.create(locale="zh_CN")


class WXServiceRequest:
    def __init__(self, appId=None, beginDate=None, endDate=None, openIds=None, **kwargs):
        self.app_id = appId
        self.begin_date = beginDate
        self.end_date = endDate
        self.kwargs = kwargs
        self.openIds = openIds


class Response(HTTPResponse):
    def __init__(self, result):
        body = dict(
            jsonrpc="2.0",
            id=0,
            result=result
        )
        super().__init__(body=dumps(body), content_type="application/json")


@lru_cache()
def _response_date(begin_date, end_date):
    days = datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(begin_date, "%Y-%m-%d")
    if days.days < 0:
        return bad_request("时间错误: begin={}, end={}".format(begin_date, end_date))

    resp_days = []
    add = 0
    while True:
        up_to = datetime.strptime(begin_date, "%Y-%m-%d") + timedelta(days=add)
        if add >= 7:
            break
        else:
            if up_to == datetime.strptime(end_date, "%Y-%m-%d"):
                resp_days.append(int(up_to.timestamp() * 1000))
                break
            else:
                resp_days.append(int(up_to.timestamp() * 1000))
                add += 1
    return resp_days


def new_get_user_summary_response(req: WXServiceRequest):
    """
    https://mp.weixin.qq.com/wiki/3/ecfed6e1a0a03b5f35e5efac98e864b7.html
    :param req:
    :return:
    """
    begin_date = req.begin_date
    end_date = req.end_date
    if not all([req.app_id, begin_date, end_date]):
        return bad_request(msg="lack of necessary parameters")

    resp_days = _response_date(begin_date, end_date)
    result = []

    source_list = collection.config.pop("source_list", None)
    new_users = collection.config.pop("new_users", 100)
    cancel_users = collection.config.pop("cancel_users", 50)

    for day in resp_days:
        if source_list:
            new_users = int(new_users - 1)
            cancel_users = 0 if (cancel_users - 1) < 0 else cancel_users - 1
            result = [dict(refDate=day, userSource=source, newUser=new_users, cancelUser=cancel_users)
                      for source in source_list]
        else:
            _source_cached = []
            for _ in range(3):
                new_users = int(new_users - 1)
                cancel_users = 0 if (cancel_users - 1) < 0 else cancel_users - 1

                source = stateWXServiceUserSources.pick_up()
                if source in _source_cached:
                    continue
                else:
                    _source_cached.append(source)
                    b = dict(
                        refDate=day,
                        userSource=source,
                        newUser=new_users,
                        cancelUser=cancel_users
                    )
                    result.append(b)
    return Response(dict(list=result))


def new_get_user_cumulate_response(req: WXServiceRequest):
    """
    https://mp.weixin.qq.com/wiki/3/ecfed6e1a0a03b5f35e5efac98e864b7.html
    :param req:
    :return:
    """
    begin_date = req.begin_date
    end_date = req.end_date
    if not all([req.app_id, begin_date, end_date]):
        return bad_request(msg="lack of necessary parameters")

    days = datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(begin_date, "%Y-%m-%d")
    if days.days < 0:
        return bad_request("时间错误: begin={}, end={}".format(begin_date, end_date))

    resp_days = _response_date(begin_date, end_date)
    result = []

    cancel_users = collection.config.pop("cancel_users", None)

    for day in resp_days:
        cumulate_user = cancel_users if cancel_users is not None else random.randint(0, 1000)
        b = dict(
            refDate=day,
            cumulateUser=cumulate_user
        )
        result.append(b)
    return Response(dict(list=result))


def new_get_open_ids_response():
    """
    https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140840&token=&lang=zh_CN
    :return:
    """
    total = collection.config.pop("open_id_counts", 5)

    if counter.offset >= total:
        count = 0
        counter.offset = 0
        next_openid = ""
    else:
        count = random.randint(1000, 10000)
        count = count if total - counter.offset >= count else total - counter.offset
        counter.offset = count
        next_openid = gen_rand_str(prefix="wx", length=26)

    return Response(dict(
        total=total,
        count=count,
        data=dict(
            openid=[gen_rand_str(prefix="xxx", length=26) for _ in range(count)],
            nextOpenid=next_openid
        )
    ))


def new_get_user_info_response(req: WXServiceRequest):
    """
    https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140839
    :return:
    """
    open_ids = req.openIds
    result = [dict(
            subscribe=stateWXServiceSubscribe.pick_up(),
            openid=oi,
            nickname=fake.name(),
            sex=stateWXServiceSex.pick_up(),
            city=fake.city(),
            country=fake.country(),
            province=fake.province(),
            language="zh_CN",
            headimgurl="http://thirdwx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
            subscribeTime=int(time.time()),
            unionid="o6_bmasdasdsad6_2sgVt7hMZOPfL",
            remark="",
            groupid=0,
            tagidList=[128],
            subscribe_scene=stateWXServiceSubscribeScene.pick_up(),
            qrScene=98765,
            qrScene_str="qr_scene_str"
        ) for oi in open_ids]

    return Response(dict(list=result))


