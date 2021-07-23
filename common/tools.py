# /usr/bin/env python
# -*- coding: utf-8 -*-
# author__ = 'HanKai'
"""
工具：正则匹配出想要的参数，可以用在关联中
"""
import re


def fetch_String(data, LB = None, RB = None):
    rule = LB + r"(.*?)" + RB
    slot_list = re.findall(rule, data)
    return slot_list

