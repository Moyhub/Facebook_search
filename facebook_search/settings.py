# -*- coding: utf-8 -*-

# Scrapy settings for facebook_search project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'facebook_search'

SPIDER_MODULES = ['facebook_search.spiders']
NEWSPIDER_MODULE = 'facebook_search.spiders'

# Obey robots.txt rules
#不遵循robots.txt 规则
ROBOTSTXT_OBEY = False  #robots.txt 是遵循Robot协议的一个文件，它保存网站服务器中，它的作用是告诉爬虫本网站哪些目录下的网页不希望你进行爬取。在Scrapy启动后会在第一时间访问网站的这个文件，然后决定该网站的爬取范围。当然，在某些情况下我们想要获取的内容恰恰是被robots.txt 所禁止访问的。所以我们就要将此配置项设置为 False 拒绝遵守 Robot协议 ！

#启用过滤过滤掉重复的信息
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

PROXIES = [
    {'ip_port': '127.0.0.1:8118', 'user_pass': None},
]
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32
#开启随机延迟
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = True
COOKIES_DEBUG = True

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
RETRY_ENABLED = True
RETRY_TIMES = 10

DOWNLOADER_MIDDLEWARES = {
    #解决代理等问题here
    #前三个为官方的下载中间键一定添加否则GG
    'scrapy.downloadermiddlewares.downloadtimeout.DownloadTimeoutMiddleware': 106,
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 800,
    'facebook_search.middlewares.ProxyMiddleware':810, #代理
    'facebook_search.middlewares.UserAgentMiddleware':820
}
DOWNLOAD_TIMEOUT = 200000
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}
# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#         'Referer': "https://www.facebook.com/"
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'facebook_search.pipelines.FacebookSearchPipeline': 100,
}
#这是走的虚拟交换机的接口
SPLASH_URL = 'http://10.0.75.1:8050'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
