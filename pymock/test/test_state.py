import unittest
from pymock.lib.base import new_state


class StateTestCase(unittest.TestCase):
    def test_get_rate_of_val(self):
        """ 获取状态值的概率

        :return:
        """
        st = new_state("Name", **{
            "a": 1,
            "b": 1,
            "c": 2,
        })
        self.assertEqual(st.get_rate_of_val("c"), float(2/4))
        self.assertEqual(st.get_rate_of_val("a"), float(1/4))

    def test_single_instance_with_same_name(self):
        """ 创建状态值如果name相同则单实例

        :return:
        """
        s1 = new_state("A", a=1, b=2)
        s2 = new_state("A", c=1, d=1)
        self.assertEqual(s1, s2)

    def test_set_rate_of_val(self):
        """ 设置状态值权重

        :return:
        """
        st = new_state("Name", **{
            "a": 1,
            "b": 1,
            "c": 2,
        })
        st["a"] = 0
        self.assertEqual(st.get_rate_of_val("a"), 0)
        self.assertEqual(st.get_rate_of_val("c"), float(2/3))

    def test_pick_up(self):
        """ 根据权重识别

        :return:
        """
        st = new_state("A", a=1, b=2, c=1)
        l = [st.pick_up() for _ in range(40000)]
        # assert is not accurate
        self.assertTrue(int(l.count("a") + l.count("c") - l.count("b")) < 200)


class CollectionTestCase():
    def test_get_rate_of_val(self):
        pass