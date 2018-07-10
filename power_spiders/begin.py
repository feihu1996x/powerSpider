"""
@file: begin.py
@brief: begin specific spider
@author: feihu1996.cn
@date: 18-7-10 下午10:32
@version: 1.0
"""

from scrapy import cmdline


spider = 'jobbole_spider'
cmdline.execute(["scrapy", "crawl", spider])
