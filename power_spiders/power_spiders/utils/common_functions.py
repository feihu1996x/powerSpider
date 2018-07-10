"""
@file: common_functions.py
@brief: common functions
@author: feihu1996.cn
@date: 17-07-07
@version: 1.0
"""
import hashlib


def get_md5(string):
    """
    :param string:
    :return string md5 hash value:
    :给定一个字符串，返回它对应的md5 hash值:
    """
    if isinstance(string, str):
        string = string.encode("utf-8")
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()


if __name__ == '__main__':
    string = 'Hello, World!'
    print(get_md5(string))
