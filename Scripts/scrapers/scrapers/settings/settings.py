# -*- coding: utf-8 -*-
'''
Settings for scraper.
'''

from os import path

# Scrapy settings for scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'hp-scraper'

SPIDER_MODULES = ['scrapers.spiders']
NEWSPIDER_MODULE = 'scrapers.spiders'

ROBOTSTXT_OBEY = True

DOWNLOAD_DELAY = 1
DOWNLOAD_TIMEOUT = 180

CONCURRENT_REQUESTS_PER_DOMAIN = 8