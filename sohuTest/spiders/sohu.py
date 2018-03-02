# -*- coding: utf-8 -*-
import scrapy
from sohuTest.items import SohutestItem
import win_unicode_console
win_unicode_console.enable()
class SohuSpider(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ['sohu.com']
    start_urls = ['http://news.sohu.com/']
    # file = open('link.txt','w',encoding='utf-8')
    def parse(self, response):
        res = response.xpath("//div[@class='content-politics-society area public clearfix']//a/@href").extract()
        for link in res:
            if not link.startswith('http:'):  #有些链接是没有http的
                link = 'http:'+link
            if len(link.split('/'))>3 and link.split('/')[3] != 'a':      #把不是详情页的给去掉
                continue
            # self.file.write(link+'\n')
            # self.file.flush()
            # print('##########################################################', link)
            yield scrapy.Request(link+'depth=1', callback = self.detailPage)
    def detailPage(self,response):
        item = SohutestItem()
        title = response.xpath("//div[@class='text-title']/h1/text()").extract()
        if not len(title):
            title =''
        else:
            title = title[0]
        time = response.xpath("//div[@class='article-info']/span[@class='time']/text()").extract()
        if not len(time):
            time = ''
        else:
            time = time[0]
        source = response.xpath("//div[@class='article-info']/span/a/text()").extract()
        if  not len(source):
            source = ''
        editor = response.xpath("//article[@class='article' and @id='mp-editor']/p/span/text()").extract() #提取信息要全面
        if not len(editor):
            editor =''
        read_nums = response.xpath("//span[@class='read-num']/em/text()").extract()
        if not len(read_nums):
            read_nums = 0
        else:
            read_nums = read_nums[0]
        if title =='' and time =='' and source =='' and editor == '':
            return
        item ['title'] = title;item['time'] = time; item['source']=source;item['read_nums']=read_nums
        # print(title,'---->',time,'------>',source,'----->',editor)
        yield item
        if response.url.endswith('depth=2'):
            return
        links = response.xpath("//div[@data-role='news-item']/h4/a/@href").extract()
        for link in links:
            if not link.startswith('http:'):  #有些链接是没有http的
                link = 'http:'+link
            if len(link.split('/'))>3 and link.split('/')[3] != 'a':      #把不是详情页的给去掉
                continue
            # self.file.write(link + '\n')
            # self.file.flush()
            # print('##########################################################',link)
            yield scrapy.Request(link+'depth=2',callback=self.detailPage)