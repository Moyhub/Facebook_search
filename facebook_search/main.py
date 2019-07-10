# -*- coding: utf-8 -*-

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import datetime
import time
import sys
# username = sys.argv[1]
# password = sys.argv[2]
# topic = sys.argv[3]

if __name__ == '__main__':
    #定时与重试
    # while(True):
    #     Try_count = 0
    #     success = False
    #     time.sleep(20)
    #     while(Try_count<3 and not success):
    #         try:
    #             if(int(datetime.datetime.now().strftime("%M")) != 1) or ( int(datetime.datetime.now().strftime("%M") == 30) ):
                    process = CrawlerProcess(get_project_settings())
                    process.crawl('facebook_crawl')
                    process.start()
            #         time.sleep(20)
            #         process.stop()
            #         break
            # except:
            #     print("重试次数为{}".format(Try_count+1))
            #     Try_count += 1
            #     if(Try_count == 3):
            #         break