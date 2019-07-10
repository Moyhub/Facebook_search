# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FacebookSearchItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    facebook_name = scrapy.Field()
    facebook_date = scrapy.Field()
    facebook_content = scrapy.Field()
    facebook_recommond_all = scrapy.Field()
    facebook_comment_number = scrapy.Field()
    facebook_share_number = scrapy.Field()
    pass
