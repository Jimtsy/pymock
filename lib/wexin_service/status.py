from lib.base import new_state

stateWXServiceUserSources = new_state("WXServiceUserSources", **{
    "0":  1,  # 代表其他合计
    "1":  1,  # 代表公众号搜索
    "17": 1,  # 代表名片分享
    "30": 1,  # 代表扫描二维码
    "43": 1,  # 代表图文页右上角菜单
    "51": 5,  # 代表支付后关注（在支付完成页
    "57": 1,  # 代表图文页内公众号名称
    "75": 1,  # 代表公众号文章广告
    "78": 1,  # 代表朋友圈广告
})


stateWXServiceSubscribeScene = new_state("WXServiceSubscribeScene", **{
    "ADD_SCENE_OTHERS":  1,  # 代表其他合计
    "ADD_SCENE_SEARCH":  1,  # 代表公众号搜索
    "ADD_SCENE_ACCOUNT_MIGRATION": 1,  # 公众号迁移
    "ADD_SCENE_PROFILE_CARD": 1,  # 代表名片分享
    "ADD_SCENE_QR_CODE": 1,  # 代表扫描二维码
    "ADD_SCENE_PROFILE_ITEM": 1,  # 代表图文页右上角菜单
    "ADD_SCENE_PAID": 5,  # 代表支付后关注（在支付完成页
    "ADD_SCENEPROFILE": 1,  # LINK 图文页内名称点击
})


stateWXServiceCountGenerator = new_state("WXServiceCountGenerator", **{
    "max": 0,
    "random": 10,
})


stateWXServiceSubscribe = new_state("WXServiceSubscribe", **{
    "1": 10,  # openid订阅了公众号
    "0": 1,  # openid未订阅公众号
})

stateWXServiceSex = new_state("WXServiceSex", **{
    "1": 10,  # 男性
    "2": 10,  # 女性
    "0": 1,  # 未知
})


__all__ = (
    stateWXServiceUserSources,
    stateWXServiceCountGenerator,
    stateWXServiceSubscribe,
    stateWXServiceSex,
    stateWXServiceSubscribeScene
)
