# -*- coding: utf-8 -*-
import scrapy
from sohuTest.items import SohutestItem
import win_unicode_console
win_unicode_console.enable()
headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Encoding':	'gzip, deflate',
  'Accept-Language	':'en-US,en;q=0.5',
  'Cache-Control':'max-age=0',
  'Connection'	:'keep-alive',
  'Upgrade-Insecure-Requests':'1',
'Host':'www.sohu.com',
'Referer:':'http://news.sohu.com/',
  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/59.0'
}
class SohuSpider(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ['sohu.com']
    start_urls = ['http://news.sohu.com/']
    # file = open('link.txt','w',encoding='utf-8')
    def call_request(self,res):
        for link in res:
            if not link.startswith('http:'):  #有些链接是没有http的
                link = 'http:'+link
            if len(link.split('/'))>3 and link.split('/')[3] != 'a':      #把不是详情页的给去掉
                continue
            # self.file.write(link+'\n')
            # self.file.flush()
            # print('##########################################################', link)
            yield scrapy.Request(link+'depth=1',headers=headers, callback = self.detailPage)
    def parse(self, response):
        #时政新闻
        res = response.xpath("//div[@class='content-politics-society area public clearfix']//a/@href").extract()
        self.call_request(res)
        res = response.xpath("//div[@class='//div[@class='contentA public area clearfix']//a/@href").extract()
        self.call_request(res)
        #军事文化
        res = response.xpath("//div[@class='//div[@class='content-military-culture area public clearfix']//a/@href").extract()
        self.call_request(res)
        #财经金融
        res = response.xpath("//div[@class='//div[@class='content-business-finance area public clearfix']//a/@href").extract()
        self.call_request(res)
        #娱乐新闻
        res = response.xpath("//div[@class='//div[@class='content-sports-yule area public clearfix']//a/@href").extract()
        self.call_request(res)
        #时尚生活
        res = response.xpath(
            "//div[@class='//div[@class='content-fashion-life area public clearfix']//a/@href").extract()
        self.call_request(res)
        #房产汽车
        res = response.xpath(
            "//div[@class='//div[@class='content-focus-auto area public clearfix']//a/@href").extract()
        self.call_request(res)
        #数码科技
        res = response.xpath(
            "//div[@class='//div[@class='content-it-digital area public clearfix']//a/@href").extract()
        self.call_request(res)
    def detailPage(self,response):
        depth = response.url.split('=')[len(response.url.split('='))-1]
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
        url = response.url
        url = url.split('?')
        if len(url)>1:
            url = url[0]
        else:
            url = url[0].split('depth')[0]
        item['url'] = url
        yield item
        if depth == '3': #深度为三的时候返回
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
            yield scrapy.Request(link+'depth='+str(int(depth)+1),headers=headers,callback=self.detailPage)