# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from redis import StrictRedis
from logoSpider.utils.userAgents import agents
import random
import base64

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = ""
proxyPass = ""
# for Python3
proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")
class ProxyMiddleWare(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        print("\n出现异常，正在使用代理重试....\n")
        request.meta["proxy"] = proxyServer

        request.headers["Proxy-Authorization"] = proxyAuth
        return request


# db = StrictRedis(host='10.0.100.93', port=6379, db=1, password='epwk')
# # db = StrictRedis(db=1)
# ip_list = db.lrange('http', 0, -1)
# class ProxyMiddleWare(object):
#     def process_request(self, request, spider):
#         proxy = random.choice(ip_list)
#         request.meta['PROXY'] = proxy.decode()
#         # request.meta['PROXY'] = 'http://96.9.69.164:53281'


class UserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers['User-Agent'] = agent


class CheckProxy(object):
    def process_response(self, request, response, spider):
        print(request.meta['proxy'])
        print(request.headers['User-Agent'])
        return response
