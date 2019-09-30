# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import logging
import pymongo


class FindchipdetailPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        ## pull in information from settings.py
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        ## initializing spider
        ## opening db connection
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        ## clean up when spider is closed
        self.client.close()

    # def __init__(self):
        # with open(self.filename, 'a') as f:
        #     writer = csv.DictWriter(f, fieldnames=item.keys())
        #     writer.writeheader()

    def process_item(self, item, spider):
        # with open(self.filename, 'rb') as f:
        #     sniffer = csv.Sniffer()
        #     has_header = sniffer.has_header(f.read(2048))
        #     if has_header:
        #         writer = csv.writer(open(self.filename, 'a'), lineterminator='\n')
        #         writer.writerow([item[key] for key in item.keys()])
        #     else:
        # with open(self.filename, 'a') as file:
        #     writer = csv.DictWriter(file, fieldnames=item.keys())
        #     writer.writeheader()
        # writer = csv.writer(open(self.filename, 'a'), lineterminator='\n')
        # writer.writerow([item[key] for key in item.keys()])

        # how to handle each post
        logging.info('>>>>' + item.get('MyConnection'))
        self.db[item.get('MyConnection')].insert(dict(item))
        return item
