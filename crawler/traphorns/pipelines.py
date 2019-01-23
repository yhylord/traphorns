# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from scrapy.exceptions import DropItem


class TraphornsPipeline(object):

    table_name = 'links'

    def __init__(self, db_filename):
        self.db_filename = db_filename

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('DB_FILENAME', 'traps.db'))

    def open_spider(self, spider):
        self.conn = sqlite3.coneect(self.db_filename)
        self.db = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if item['source']:
            columns = (self.table_name,
                       item['source'], item['link'], item['dead'])
            statement = 'INSERT INTO ? (source, link, dead) VALUES (?,?,?)'
            self.db.execute(statement, columns)
            return item
        else:  # no source, must be one of start urls
            raise DropItem('Omit start url, item: {}'.format(item))
