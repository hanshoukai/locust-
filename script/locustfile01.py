# /usr/bin/env python
# -*- coding: utf-8 -*-
# author__ = 'HanKai'

import queue
from queue import Queue
from random import choice
from locust import HttpUser, constant, between, task, TaskSet, tag, SequentialTaskSet


# 第二种写在用户类外定义函数，@task表示任务
@task
def http_get(user):
    user.client.request(method='GET', url="/getAllUrl", name='打开首页')


# 用户类
# 定义一个类并继承locust下的HttpUser类
class ApiUser(HttpUser):
    host = "http://api.apiopen.top"  # 设置网站的根地址
    tasks = [http_get]               # 与第二种方式结合使用，ApiUser类继承了HttpUser，tasks任务集中也继承了user

    # 格式一
    # wait_time = constant(3)     # 每次请求的固定停顿时间（相当于性能测试的思考时间）
    # 格式二
    # wait_time = between(2, 5)     # 每次请求的停顿时间在2到5秒之间随机取值（也相当于性能测试的思考时间）
    # 格式三
    min_wait = 2000               # 模拟负载任务之间执行时的 最小/最大 停顿时间，单位毫秒.和between类似
    max_wait = 5000

    """
    # 第一种直接写在用户类下定义函数
    @task  # task括号内数值越大执行频率越高，默认标记为1
    def http_get(self):
        self.client.request(method='GET', url = "/getAllUrl", name='获取URL地址1')
        self.client.get("/getAllUrl", name="获取URL地址2")
    """


