# /usr/bin/env python
# -*- coding: utf-8 -*-
# author__ = 'HanKai'
import queue
from queue import Queue
from random import choice
from locust import HttpUser, constant, between, task, TaskSet, tag, SequentialTaskSet


# 任务类
class ApiSeqTask(TaskSet):
    # @task
    # def http_get(self):
    #     # 有序请求参数化取值
    #     try:
    #         count_page = self.user.count_page.get()  # 获取唯一的配置信息
    #         print(count_page)
    #     except queue.Empty:
    #         print("数据已用完")
    #         exit(0)  # 无错误退出
    #     countpage = count_page.split(",")
    #     params = {
    #         "page": countpage[0],
    #         "count": countpage[1]
    #     }
    #     with self.client.get("/poetryFull", params=params, name="获取诗词")as res:
    #         print(res.text)

    @task
    def http_get(self):
        # 无序请求参数化取值
        p_c = choice(self.user.payload).split(",")
        print(p_c)
        params = {
            "page": p_c[0],
            "count": p_c[1]
        }
        self.client.get("/poetryFull", params=params, name="获取诗词")
        # with self.client.get("/poetryFull", params=params, name="获取诗词")as res:
        #     print(res.text)


# 用户类
# 定义一个类并继承locust下的HttpUser类
class ApiUser(HttpUser):
    host = "http://poetry.apiopen.top"  # 设置网站的根地址

    # 格式一
    # wait_time = constant(3)     # 每次请求的固定停顿时间（相当于性能测试的思考时间）
    # 格式二
    # wait_time = between(2, 5)     # 每次请求的停顿时间在2到5秒之间随机取值（也相当于性能测试的思考时间）
    # 格式三
    min_wait = 2000               # 模拟负载任务之间执行时的 最小/最大 停顿时间，单位毫秒
    max_wait = 5000

    tasks = [ApiSeqTask]             # 与第四种方式结合使用，执行一次get请求再执行十次post请求

    # 无序参数化
    payload = []
    with open("./../data/data.csv",'r')as file:
        for line in file.readlines():
            payload.append(line.strip())
    # print(payload) # ['1,2', '2,1', '3,5', '4,1', '5,3']

    # 有序参数化
    count_page = Queue()
    with open("./../data/data.csv",'r')as file:
        for line in file.readlines():
            count_page.put_nowait(line.strip())


