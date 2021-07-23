# /usr/bin/env python
# -*- coding: utf-8 -*-
# author__ = 'HanKai'
import queue
from queue import Queue
from locust import User
from random import choice
from locust import HttpUser, constant, between, task, TaskSet, tag, SequentialTaskSet


# ======================1============================
# 任务类
class Api_One_Task(TaskSet):
    @task
    def http_get(self):
        self.client.get("/getAllUrl", name="获取所有的url")

    @task(5)
    def http_post(self):
        header = {"Content-Type": "application/json"}
        payload = {
            "page": 1,
            "count": 20
        }
        with self.client.post("/getWangYiNews", headers=header, data=payload, verify=False, name="获取20条新闻")as res:
            print(res.text)

# ======================2============================

@task
def get_images(self):
    header = {"Content-Type": "application/json"}
    payload = {
        "page": 1,
        "count": 10
    }
    with self.client.post("/getImages", headers=header, data=payload, verify=False, name="获取10张图片")as res:
        print(res.text)


@task
def get_tangPoetry(self):
    header = {"Content-Type": "application/json"}
    payload = {
        "page": 1,
        "count": 5
    }
    with self.client.post("/getTangPoetry", headers=header, data=payload, verify=False, name="获取唐朝古诗词")as res:
        print(res.text)


# 用户类
# 定义一个类并继承locust下的HttpUser类
class ApiUser(HttpUser):
    host = "http://api.apiopen.top"  # 设置网站的根地址

    # 格式一
    # wait_time = constant(3)     # 每次请求的固定停顿时间（相当于性能测试的思考时间）
    # 格式二
    # wait_time = between(2, 5)     # 每次请求的停顿时间在2到5秒之间随机取值（也相当于性能测试的思考时间）
    # 格式三
    min_wait = 2000               # 模拟负载任务之间执行时的 最小/最大 停顿时间，单位毫秒
    max_wait = 5000

    # 1、tasks任务集后可以是类也可以是函数【如locustfile01.py】，一个任务集中权重分配：task标记，值越大执行次数越多
    # tasks = [Api_One_Task]
    # 2、运行大概次数：get_images是get_tangPoetry的3倍
    tasks = {get_tangPoetry: 1, get_images: 3}



