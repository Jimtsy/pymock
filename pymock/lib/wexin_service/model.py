import random
import faker
import time
from datetime import datetime, timedelta
from pymock.lib.base.response import bad_request
from functools import lru_cache
from pymock.utils import Counter, gen_rand_str
from .status import \
    stateWXServiceUserSources, stateWXServiceCountGenerator,  stateWXServiceSubscribe, \
    stateWXServiceSex, stateWXServiceSubscribeScene


counter = Counter("open_id_counter")
fake = faker.Factory.create(locale="zh_CN")


class WXServiceRequest:
    def __init__(self, appId=None, beginDate=None, endDate=None, openIds=None, **kwargs):
        self.app_id = appId
        self.begin_date = beginDate
        self.end_date = endDate
        self.kwargs = kwargs
        self.openIds = openIds


@lru_cache()
def _response_date(begin_date, end_date):
    days = datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(begin_date, "%Y-%m-%d")
    if days.days < 0:
        return bad_request("时间错误: begin={}, end={}".format(begin_date, end_date))

    resp_days = []
    add = 0
    while True:
        print(add)
        up_to = datetime.strptime(begin_date, "%Y-%m-%d") + timedelta(days=add)
        if add >= 7:
            break
        else:
            if up_to == datetime.strptime(end_date, "%Y-%m-%d"):
                resp_days.append(up_to.__format__("%Y-%m-%d"))
                break
            else:
                resp_days.append(up_to.__format__("%Y-%m-%d"))
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
    resp = []
    for day in resp_days:
        _source_cached = []
        for _ in range(3):
            new_users = random.randint(0, 100)
            source = stateWXServiceUserSources.pick_up()
            if source in _source_cached:
                continue
            else:
                _source_cached.append(source)
                b = dict(
                    ref_date=day,
                    user_source=stateWXServiceUserSources.pick_up(),
                    new_user=new_users,
                    cancel_user=new_users-10 if new_users-5 >=0 else 0
                )
                resp.append(b)
    return resp


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
    resp = []

    for day in resp_days:
        b = dict(
            ref_date=day,
            cumulate_user=random.randint(0, 1000)
        )
        resp.append(b)
    return resp


def new_get_open_ids_response():
    """
    https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140840&token=&lang=zh_CN
    :return:
    """
    total = 20000

    if counter.offset >= total:
        count = 0
        next_openid = ""
    else:
        way = stateWXServiceCountGenerator.pick_up()
        if way == "max":
            count = 10000 if total - counter.offset >= 10000 else total - counter.offset
        else:
            count = random.randint(1000, 10000)
            count = count if total - counter.offset >= count else total - counter.offset
        counter.offset = count
        next_openid = gen_rand_str(prefix="wx", length=26)

    return dict(
        total=total,
        count=count,
        data=dict(
            openid=[gen_rand_str(prefix="oa", length=26) for _ in range(count)],
            next_openid=next_openid
        )
    )


def new_get_user_info_response(req: WXServiceRequest):
    """
    https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140839
    :return:
    """
    open_ids = req.openIds
    response = [dict(
            subscribe=stateWXServiceSubscribe.pick_up(),
            openid=oi,
            nickname=fake.name(),
            sex=stateWXServiceSex.pick_up(),
            city=fake.city(),
            country=fake.country(),
            province=fake.province(),
            language="zh_CN",
            headimgurl="http://thirdwx.qlogo.cn/mmopen/g3MonUZtNHkdmzicIlibx6iaFqAc56vxLSUfpb6n5WKSYVY0ChQKkiaJSgQ1dZuTOgvLLrhJbERQQ4eMsv84eavHiaiceqxibJxCfHe/0",
            subscribe_time=int(time.time()),
            unionid="o6_bmasdasdsad6_2sgVt7hMZOPfL",
            remark="",
            groupid=0,
            tagid_list=[128],
            subscribe_scene=stateWXServiceSubscribeScene.pick_up(),
            qr_scene=98765,
            qr_scene_str="qr_scene_str"
        ) for oi in open_ids]

    return response


