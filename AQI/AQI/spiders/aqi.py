# -*- coding: utf-8 -*-
import scrapy
from AQI.items import AqiItem
import time

# 1 导入RedisSpider类
from scrapy_redis.spiders import RedisSpider

# 2 修改继承类
# class AqiSpider(scrapy.Spider):
class AqiSpider(RedisSpider):
    name = 'aqi'

    # 3. 注销允许的域名和起始的url
    # allowed_domains = ['www.aqistudy.cn']
    #
    # host = 'https://www.aqistudy.cn/historydata/'
    # start_urls = [host]

    # 4 .编写__init__()动态获取允许的域名
    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domains = list(filter(None, domain.split(',')))
        super(AqiSpider, self).__init__(*args, **kwargs)

    # 5. 编写redis_key
    redis_key = 'aqi'

    def parse(self, response):
        # 获取城市url列表
        url_list = response.xpath('//div[@class="bottom"]/ul[@class="unstyled"]/div/li/a/@href').extract()

        # 遍历列表
        for url in url_list:
            city_url = 'https://www.aqistudy.cn/historydata/' + url
            # 发起对城市详情页面的请求
            yield scrapy.Request(city_url, callback=self.parse_month)

    # 解析详情页面请求对应的响应
    def parse_month(self,response):
        # 获取每月详情url列表
        url_list = response.xpath('//ul[@class="unstyled1"]/li/a/@href').extract()
        # print(len(url_list))
        # 遍历url列表中的部分
        for url in url_list[30:35]:
            mouth_url = 'https://www.aqistudy.cn/historydata/' + url
        # print(mouth_url)
            # 发起详情页面请求
            yield scrapy.Request(mouth_url,callback=self.parse_day)

    # 在详情页面解析数据
    def parse_day(self,response):
        # 获取所有的数据节点
        node_list = response.xpath('//tr')

        city = response.xpath('//div[@class="panel-heading"]/h3/text()').extract_first().split('2')[0]
        # 遍历数据节点列表
        for node in node_list:
            # 创建存储数据的item容器
            item = AqiItem()
            # 先填写一些固定参数
            item['city'] = city
            item['url'] = response.url
            item['timestamp'] = time.time()

            # 数据
            item['date'] = node.xpath('./td[1]/text()').extract_first()
            item['AQI'] = node.xpath('./td[2]/text()').extract_first()
            item['LEVEL'] = node.xpath('./td[3]/span/text()').extract_first()
            item['PM2_5'] = node.xpath('./td[4]/text()').extract_first()
            item['PM10'] = node.xpath('./td[5]/text()').extract_first()
            item['SO2'] = node.xpath('./td[6]/text()').extract_first()
            item['CO'] = node.xpath('./td[7]/text()').extract_first()
            item['NO2'] = node.xpath('./td[8]/text()').extract_first()
            item['O3_8h'] = node.xpath('./td[9]/text()').extract_first()

            # 将数据返回给引擎
            yield item








































