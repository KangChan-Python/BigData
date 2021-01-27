# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import json
from scrapyproject.items.naverPlace_items import ScrapyprojectItem


class NaverplaceSpider(scrapy.Spider):
    name = 'naverPlace'
    df = pd.read_csv('../../BD_file\\ETC/시군구_최종정리.csv')    

    def start_requests(self):
        for loc in self.df['시도_시군구'].values:
            if len(loc.split()) == 1:
                search = loc + ' 음식점'
            else:
                search = loc.split()[1][:-1] + '  음식점'
            url = "https://map.naver.com/v5/api/search?caller=pcweb&query={}&type=all%page=1&displayCount=50&isPlaceRecommendationReplace=true&lang=ko".format(search)
            yield scrapy.Request(url=url, callback=self.parsejs)

    def parsejs(self, response):
        js = json.loads(response.body)
        for i in range(20):
            doc = ScrapyprojectItem()
            doc['id1'] = js['result']['place']['list'][i]['id']
            doc['name'] = js['result']['place']['list'][i]['name']
            doc['category'] = js['result']['place']['list'][i]['category']
            doc['context'] = js['result']['place']['list'][i]['context']
            doc['addr'] = js['result']['place']['list'][i]['roadAddress']
            doc['rank'] = js['result']['place']['list'][i]['rank']
            doc['x'] = js['result']['place']['list'][i]['y']
            doc['y'] = js['result']['place']['list'][i]['x']
            yield doc
