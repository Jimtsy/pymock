# -*- coding: utf-8 -*-
from threading import RLock
from utils import SingletonIfSameParameters
from .response import bad_request
from log import logger
import random


class _StateCreatable(type):
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls._instance_cached = {}

    def __call__(cls, *args, **kwargs):
        name = kwargs.get("name")
        if name not in cls._instance_cached:
            instance = super().__call__(*args, **kwargs)
            cls._instance_cached[name] = instance
        return cls._instance_cached[name]


class _State(dict, metaclass=_StateCreatable):
    def __init__(self, name, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.lock = RLock()

        self._initial = True
        for _, val in kwargs.items():
            if not isinstance(val, int):
                raise ValueError("weight value expected to an int val")

    @property
    def total_weights(self):
        return sum([val for _, val in self.items()])

    @property
    def sorted_items(self):
        return sorted(self.items(), key=lambda item: item[1])

    def pick_up(self):
        self.lock.acquire()
        total_weight = self.total_weights
        if total_weight < 0:
            raise ValueError("invalid status: {}".format(self))
        si = self.sorted_items
        self.lock.release()
        index = random.randint(1, total_weight)
        current = 0
        for v, w in si:
            current += w
            if current >= index:
                return v

    def __setitem__(self, val, weight):
        if val not in self:
            pass
        else:
            super().__setitem__(val, int(weight))

    def get_ratio_of_val(self, val):
        weight = self.get(val, 0)
        return float(weight / self.total_weights)

    @property
    def distribution(self):
        return {k: v for k, v in self.sorted_items}

    def set_whitelist(self, val):
        self.lock.acquire()
        for v, _ in self.items():
            if v == val:
                self[v] = 1
            else:
                self[v] = 0

        self.lock.release()


class StateCollection(metaclass=SingletonIfSameParameters):
    """
    状态集合
    """
    def __init__(self):
        self._collection = {}
        self.lock = RLock()
        self._config = {}

    def __check_exist(self, state_name):
        if state_name not in self._collection:
            return bad_request(msg="{} 不存在".format(state_name))

    def receive(self, state: _State):
        self.lock.acquire()
        if state.name in self._collection:
            raise KeyError("republication key of {}".format(state.name))
        self._collection[state.name] = state
        self.lock.release()

    def set_ratio_of_val(self, state_name, val, weight):
        """

        :param state_name:
        :param val:
        :param weight:
        :return:
        """

        self.__check_exist(state_name)
        self.lock.acquire()
        state = self._collection[state_name]
        before_ratio = state.get_ratio_of_val(val)
        state[val] = weight
        after_ratio = state.get_ratio_of_val(val)
        self.lock.release()
        return {"before": before_ratio, "after": after_ratio, "distribution": state.distribution}

    def get_state_info(self, state_name):
        self.__check_exist(state_name)
        return self._collection[state_name].distribution

    def whitelist(self, state_name, val):
        self.__check_exist(state_name)
        state = self._collection[state_name]
        state.set_whitelist(val=val)
        return {"distribution": state.distribution}

    @property
    def config(self):
        return self._config

    def set_config(self, **kwargs):
        self.lock.acquire()
        if kwargs.get("clear", False):
            self._config = {}
        self._config = {**self._config, **kwargs}
        self.lock.release()
        return self._config


def new_state(name, **kwargs):
    """

    :param name:
    :param kwargs:
    :return:
    """
    state = _State(name=name, **kwargs)
    collection.receive(state)
    return state


# collection instance
collection = StateCollection()