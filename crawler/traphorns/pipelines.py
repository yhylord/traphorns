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
        self.conn = sqlite3.connect(self.db_filename)
        self.conn.row_factory = sqlite3.Row
        self.db = self.conn.cursor()

        self.start_urls = spider.start_urls

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        if not item['source'] and item['link'] in self.start_urls:
            # item returned when the crawler starts by visiting start_url
            # not really a link so drop it
            raise DropItem('Omit start url, item: {}'.format(item))

        params = item.copy()
        params['table'] = self.table_name

        finding_last_record = ('SELECT dead FROM links '
                               'WHERE source=:source AND link=:link '
                               'ORDER BY timestamp DESC')
        self.db.execute(finding_last_record, params)
        last_record = self.db.fetchone()

        if last_record and last_record['dead'] == item['dead']:
            raise DropItem('Status has not changed, item: {}'.format(item))
        else:
            # status different from last time, needs saving
            insertion = ('INSERT INTO links (source, link, dead) '
                         'VALUES (:source, :link, :dead)')
            self.db.execute(insertion, params)
            self.conn.commit()
            return item
