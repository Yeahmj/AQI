# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AqiItem(scrapy.Item):
    # define the fields for your item here like:
    # 城市
    city = scrapy.Field()
    # url
    url = scrapy.Field()
    # 数据采集时间
    timestamp = scrapy.Field()
    # 数据
    date = scrapy.Field()
    AQI = scrapy.Field()
    LEVEL = scrapy.Field()
    PM2_5 = scrapy.Field()
    PM10 = scrapy.Field()
    SO2 = scrapy.Field()
    CO = scrapy.Field()
    NO2 = scrapy.Field()
    O3_8h= scrapy.Field()
    pass
