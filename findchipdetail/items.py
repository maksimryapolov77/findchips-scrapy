# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FindchipdetailItem(scrapy.Item):
    # define the fields for your item here like:
    def __setitem__(self, key, value):
        self._values[key] = value
        self.fields[key] = {}
    pass

