# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from  selenium import webdriver
import time
from  scrapy.log import logger
from selenium.webdriver.support.ui import WebDriverWait
from scrapy.http import HtmlResponse
import win_unicode_console
win_unicode_console.enable()
driver = webdriver.PhantomJS(service_args=['--disk-cache=true','--load-images=false']) #设置缓存和禁止图片加载
wait = WebDriverWait(driver,1) #等待1秒浏览器进行加载
driver.set_window_size(100,1200)
class SohutestSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.
        # Must return only requests (not items).
        for r in start_requests:
            yield r
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

    def process_request(self,request,spider):
        try:
            if request.url.startswith("http://www.sohu.com"):
                if request.url.endswith('depth=1'):
                    try:
                        driver.get(request.url.rstrip('depth=1'))
                    except:
                        logger.info('出现异常1')
                    #chrome浏览器提速
                    # chrome_opt = webdriver.ChromeOptions()
                    # prefs = {"profile.managed_default_content_settings.images": 2}
                    # chrome_opt.add_experimental_option("prefs", prefs)
                    # #driver = webdriver.Chrome(service_args=['--disk-cache=true','--load-images=false'])
                    # driver = webdriver.Chrome( chrome_options=chrome_opt)
                    # driver.set_window_size(100, 1000)
                    # driver.get(request.url)
                    # js = "document.documentElement.scrollTop=document.documentElement.scrollHeight"  # 滚动条下拉1000px
                    # end = driver.find_elements_by_xpath("//div[@class='more-load' and @style='']")
                    # count = 1
                    # while not len(end):
                    #     print(count)
                    #     driver.execute_script(js)
                    #     time.sleep(1)
                    #     end = driver.find_elements_by_xpath("//div[@class='more-load' and @style='']")
                    #     count += 1
                    count = 0
                    while count<50:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                        count +=1
                        logger.info('正在加载')
                        time.sleep(0.5)
                    content = driver.page_source.encode('utf-8')
                    return HtmlResponse(request.url,body=content)
                else:
                    try:
                        driver.get(request.url.rstrip('depth=2'))
                    except:
                        logger.info('出现异常2')
                    content = driver.page_source.encode('utf-8')
                    return HtmlResponse(request.url, body=content)

        except:
            logger.info('出现异常')
