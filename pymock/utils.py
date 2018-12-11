# -*- coding: utf-8 -*-
import time
import random
import string
import hashlib
import threading
from datetime import datetime, timedelta


class SingletonIfSameParameters(type):

    def __init__(cls, *args, **kwargs):
        cls._instance = {}
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        k = make_sequence_key(*args, **kwargs)
        if cls._instance.get(k) is None:
            inst = super().__call__(*args, **kwargs)
            cls._instance[k] = inst
        return cls._instance[k]


class Counter(metaclass=SingletonIfSameParameters):
    """
    线程安全的计数器
    """
    def __init__(self, name=None):
        self.name = name
        self.lock = threading.RLock()
        self._offset = 0

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, steps=1):
        self.lock.acquire()
        self._offset += steps
        self.lock.release()

    def reset(self):
        self.lock.acquire()
        self._offset = 0
        self.lock.release()


def make_sequence_key(*args, **kwargs):
    """ 根据传入的参数，生成一个唯一的key

    :param args:
    :param kwargs:
    :return:
    """
    args = list(map(lambda s: str(s), args))
    args.sort()
    k1 = "".join(args)
    k2 = "".join([str(k) + str(v) for k, v in sorted(kwargs.items())])
    return k1 + k2


def day_timestamp(delta_days=0):
    """ 获取零点的unixtime 例如 2018-11-27 00:00:00

    :param delta_days:
    :return:
    """
    d = datetime.today() + timedelta(days=delta_days)
    return time.mktime(time.strptime(d.__format__("%Y-%m-%d"), "%Y-%m-%d"))


class Bunch(dict):
    """
    >>> d1 = dict(username='admin', password=123456, data={'code': 7788})
    >>> bunch = Bunch(d1)
    >>> bunch.username == d1['username']
    True
    >>> bunch.data.code == 7788
    True
    >>> bunch.name = 'hello'
    """

    def __getattr__(self, item):
        try:
            object.__getattribute__(self, item)
        except AttributeError:
            try:
                value = super(Bunch, self).__getitem__(item)
            except KeyError as e:
                raise AttributeError('attribute named {} was not found'.format(item)) from e
            else:
                if isinstance(value, dict):
                    return Bunch(value)
                return value

    def __setattr__(self, key, value):
        super(Bunch, self).__setitem__(key, value)


def md5_str(content, encoding='utf-8'):
    """计算字符串的MD5值

    :param content:输入字符串
    :param encoding: 编码方式
    :return:
    """
    m = hashlib.md5(content.encode(encoding))
    return m.hexdigest()


def md5_file(fp, block=1024):
    """计算文件的MD5值

    :param fp:文件路径
    :param block:读取的块大小
    :return:
    """
    m = hashlib.md5()
    with open(fp, 'rb') as f:
        while 1:
            c = f.read(block)
            if c:
                m.update(c)
            else:
                break
    return m.hexdigest()


def gen_rand_str(length=8, s_type='hex', prefix=None, postfix=None):
    """生成指定长度的随机数，可设置输出字符串的前缀、后缀字符串

    :param length: 随机字符串长度
    :param s_type:
    :param prefix: 前缀字符串
    :param postfix: 后缀字符串
    :return:
    """
    if s_type == 'digit':
        formatter = "{:0" + str(length) + "}"
        mid = formatter.format(random.randrange(10**length))
    elif s_type == 'ascii':
        mid = "".join([random.choice(string.ascii_letters) for _ in range(length)])
    elif s_type == "hex":
        formatter = "{:0" + str(length) + "x}"
        mid = formatter.format(random.randrange(16**length))
    else:
        mid = "".join([random.choice(string.ascii_letters+string.digits) for _ in range(length)])

    if prefix is not None:
        mid = prefix + mid
    if postfix is not None:
        mid = mid + postfix
    return mid