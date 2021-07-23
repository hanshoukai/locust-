# /usr/bin/env python
# -*- coding: utf-8 -*-
# author__ = 'HanKai'
"""
1、locust特别适合做接口侧性能测试
2、如果要测试的接口不多，也没有执行顺序上的要求，可以单独的写成一个方法即可，如下第一种和第二种方式
3、如果要测试的接口多，有权重的执行要求，这时候就需要写在一个或多个任务集中，如下第三种方式
写在一个任务集中权重分配：task标记
写在多个任务集中权重分配：
按比例分配A类名是B类名下任务的3倍
tasks = {A: 3, B: 1}
4、第一种，第二种、第三种都是并行执行，多个类【任务集】运行：tasks = [A, B]
5、第四种按一定的顺序执行[TaskSet.SequentialTaskSet]

6、参数化取值方式：
循环取数据，数据可重复使用 list(无序)
保证并发测试数据唯一性，循环取值 queue（有序）
保证并发测试数据唯一性，不循环取值 queue（有序）
7、关联可采用common中正则提取所要的字符串
8、思考时间：constant、between、min_wait/max_wait
9、检查点
10、事务：没有事务的概念，时间统计是按照接口统计，与事务无法，无法直接体现出事务的耗时
11、集合点：实现参考https://www.cnblogs.com/grandlulu/p/9455794.html

12、分布式压测：协程在Linux下性能要比windows好很多的，可以设置windows为master，Linux下为worker节点
"""
import queue
from queue import Queue
from random import choice
from locust import HttpUser, constant, between, task, TaskSet, tag, SequentialTaskSet
from locust import HttpLocust  # 1.0版本之前在使用HttpLocust
# ======================
# #第二种写在用户类外定义函数
# @task
# def http_get(user):
#     user.client.request(method='GET', url="/getAllUrl", name='打开首页')


# ======================
# #第三种写在任务类中
# 任务类
class ApiTask(TaskSet):
    @task
    def http_get(self):
        self.client.get("/getAllUrl")

    @task(5)
    def http_post(self):
        header = {"Content-Type": "application/json"}
        payload = {
            "page": 1,
            "count": 200
        }
        with self.client.post("/getWangYiNews", headers=header, data=payload, verify=False, name="获取200条信息")as res:
            print(res.text)


# ======================
# #第四种写在任务类中并按一定顺序执行,SequentialTaskSet是TaskSet类下的按顺序执行的一个函数
# 任务类
class ApiSeqTask(SequentialTaskSet):
    # @task
    # def http_get(self):
    #     self.client.get("/getAllUrl", name="获取所有URL")

    # @task(10)
    # def http_post(self):
    #     # post请求无序参数化取值
    #     p_c = choice(self.user.payload).split(",")
    #     print(p_c)
    #     header = {"Content-Type": "application/json"}
    #     payload = {
    #         "page": p_c[0],
    #         "count": p_c[1]
    #     }
    #     with self.client.post("/getWangYiNews", headers=header, data=payload, verify=False, name="获取200条信息")as res:
    #         print(res.text)

    # @task
    # def http_get(self):
    #     # 无序请求参数化取值
    #     p_c = choice(self.user.payload).split(",")
    #     print(p_c)
    #     params = {
    #         "page": p_c[0],
    #         "count": p_c[1]
    #     }
    #     with self.client.get("/poetryFull", params=params, name="获取诗词")as res:
    #         print(res.text)

    @task
    def http_get(self):
        # 有序请求参数化取值
        try:
            count_page = self.user.count_page.get()  # 获取唯一的配置信息
            print(count_page)
        except queue.Empty:
            print("数据已用完")
            exit(0)  # 无错误退出
        countpage = count_page.split(",")
        params = {
            "page": countpage[0],
            "count": countpage[1]
        }
        with self.client.get("/poetryFull", params=params, name="获取诗词")as res:
            print(res.text)


# 用户类
# 定义一个类并继承locust下的HttpUser类
class ApiUser(HttpUser):
    # host = "http://api.apiopen.top"  # 设置网站的根地址
    host = "http://poetry.apiopen.top"  # 设置网站的根地址

    # 格式一
    # wait_time = constant(3)     # 每次请求的固定停顿时间（相当于性能测试的思考时间）
    # 格式二
    # wait_time = between(2, 5)     # 每次请求的停顿时间在2到5秒之间随机取值（也相当于性能测试的思考时间）
    # 格式三
    min_wait = 2000               # 模拟负载任务之间执行时的 最小/最大 停顿时间，单位毫秒
    max_wait = 5000

    # tasks = [http_get]            # 与第二种方式结合使用，ApiUser类继承了HttpUser，tasks任务集中也继承了user
    # tasks = [ApiTask]             # 与第三种方式结合使用，tasks任务集后也可以是类
    tasks = [ApiSeqTask]             # 与第四种方式结合使用，执行一次get请求再执行十次post请求

    # ======================
    # 第一种直接写在用户类下定义函数
    # @task  # task括号内数值越大执行频率越高，默认标记为1
    # def http_get(self):
    #     self.client.request(method='GET', url = "/getAllUrl", name='打开首页')

    # 无序参数化
    payload = []
    with open("data/id.csv",'r')as file:
        for line in file.readlines():
            payload.append(line.strip())
    # print(payload) # ['1,200', '2,100', '3,50', '4,10', '5,5']

    # 有序参数化
    count_page = Queue()
    with open("data/id.csv",'r')as file:
        for line in file.readlines():
            count_page.put_nowait(line.strip())


