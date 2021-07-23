# 性能测试
## 性能测试四大模块
### 脚本编写
  - 协议
    - http
    - websocket
  - 工具选型：
    - LR - C
    - jmeter - Java
    - Locust - Python
  - 脚本设计（Locust）
    - 参数化
      - 参数化取值方式：
        - 循环取数据，数据可重复使用 list(无序)
        - 保证并发测试数据唯一性，循环取值 queue（有序）
        - 保证并发测试数据唯一性，不循环取值 queue（有序）
    - 关联
      - 定义一个方法取值后 待其他方法引用
      - 可采用common中正则提取所要的字符串【是不是很像LR关联函数的操作，确认左右边界提取需要的字符串】
    - 检查点
      - assert/if
    - 思考时间
      - constant、between、min_wait/max_wait
    - 事务
      - locust没有事务的概念，时间统计是按接口统计，与事务无关，无法直接体现出事务的耗时
    - 集合点
      - 基于gevent并发得机制，引入gevent中锁的概念，代入到locust的钩子函数中，实现集合点统一并发概念
      - 性能测试中很少使用到集合点，更多是在场景设计中进行并发数的设置
### 场景设计及监控
  - 场景
    - 单场景
    - 混合场景 
    - 先单后混
  - 画图（压力曲线图）
    - 评估性能如何的操作步骤：
      - 1、多长时间加一批用户：尽量长些。看清每批用户对系统造成的负载
      - 2、一批用户加多少：不要太多。定位是哪批用户造成的系统资源问题 
      - 3、时间越长越好，充分预热后的系统才可以看出系统资源的使用情况
  - 监控
    - 监控原则：
      - 压测工具只做发压，不要做监控。监控交给监控工具
      - 避免过度监控
    - 监控设计：
      - 被测系统节点比较少
        - 基本性能指标：响应时间，吞吐量，资源利用率
          - 响应时间和吞吐量：压测工具自带的监控功能即可【locust：图形化&非图形化；jmeter中的聚合报告】
          - 资源利用率：os自带的监控工具：vmstat，top，nmon
      - 被测系统节点比较多
        - 除了基本性能指标外，还要有 后端监控【瓶颈和优化】：代码（jvm）、中间件、数据库
      
    - jmeter压测监控平台       
      - 基本性能指标：influxdb+jmeter+grafana
      - 后段数据监控：promethues+grafana
        - 注：influxdb、promethues、grafana可以部署在docker中，exporter直接运行在被测服务器上即可
  - 压力
    - 相同资源locust可以实现几万并发量，jmeter几百的线程并发量
    - 分布式压测：协程在Linux下性能要比windows好很多，可以设置windows为master，Linux下为worker节点
  - 设置
    - 基本设置参数设置完成后可以启动进行发压
### 结果分析
### 性能调优
<br>&nbsp;
# Locust特别适合做接口侧性能测试
## 代码编写
- 1、如果要测试的接口不多，也没有执行顺序上的要求，可以单独的写成一个方法即可，如第一种和第二种方式
  - locustfile01.py
- 2、如果要测试的接口多，有权重的执行要求，这时候就需要写在一个或多个任务集中，如第三种方式
  - locustfile02.py
    - 写在一个任务集中权重分配：task标记
    - 写在多个任务集中权重分配：
        - 按比例分配A类名是B类名下任务的3倍
        - tasks = {A: 3, B: 1}
- 3、第四种按一定的顺序执行[TaskSet.SequentialTaskSet]
  - locustfile03.py
- 4、参数化+思考时间脚本
  - locustfile04.py
  
#说明：locustfile.py为01、02、03、04的合集