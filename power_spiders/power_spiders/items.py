# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import datetime
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

from power_spiders.utils.common_functions import get_md5


def clear_string(string):
    return re.sub('\s|\·|,', '', string)


def get_date(string):
    string = clear_string(string)
    try:
        date_value = datetime.datetime.strptime(string, "%Y/%m/%d").date()
    except Exception:
        date_value = datetime.datetime.now().date()

    return date_value


def get_num(string):
    string = clear_string(string)
    res = re.match(".*?(\d+).*", string)
    if res:
        nums = int(res.group(1))
    else:
        nums = 0

    return nums


def get_value(string):
    return string


class ArticleSpiderItemLoader(ItemLoader):
    # 自定义item loader
    default_output_processor = TakeFirst()
    default_input_processor = MapCompose(clear_string)


class ArticleSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 文章标题
    post_title = scrapy.Field()

    # 发表时间
    create_time= scrapy.Field(
        input_processor=MapCompose(get_date)
    )

    # 点赞数
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_num)
    )

    # 收藏数
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_num)
    )

    # 评论数
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_num)
    )

    # 文章标签
    post_tag = scrapy.Field(
        output_processor=Join(',')
    )

    # 文章内容
    post_content = scrapy.Field(
        input_processor=MapCompose(get_value)
    )

    # 封面图片
    post_image = scrapy.Field(
        output_processor=MapCompose(get_value)
    )

    # 封面图片保存路径
    post_image_store_path = scrapy.Field()

    # url md5 hash
    url_object_id = scrapy.Field(
        input_processor=MapCompose(get_md5)
    )

    # 文章网址
    post_url = scrapy.Field()

