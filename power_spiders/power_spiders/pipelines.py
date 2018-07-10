# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if 'post_image' in item:
            for ok, value in results:
                post_image_store_path = value["path"]
            item["post_image_store_path"] = post_image_store_path
        return item


class ArticleJsonPipeline:
    def __init__(self):
        self.target = open('article.json', 'wb')
        self.exporter = JsonItemExporter(self.target, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.target.close()


class MysqlTwistedPipeline:
    # 借助Twisted网络框架实现数据的异步存储
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DB'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASS'],
            charset = 'utf8mb4',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)
        return cls(dbpool)

    def do_insert(self, cursor, item):
        insert_sql = '''
            insert into article(post_title, post_url, url_object_id) values(%s, %s, %s);
        '''
        cursor.execute(insert_sql, (item["post_title"], item["post_url"], item["url_object_id"]))

    def handle_error(self, failure, item, spider):
        print(failure)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)
