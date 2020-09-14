# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import json
from scrapyproject.items.naverPlace_items import ScrapyprojectItem


class NaverplaceSpider(scrapy.Spider):
    name = 'naverPlace'
    df = pd.read_excel('C:\\Users\\jye12\\Python\\BigData\\BD_file\\scrapy용/시군구정리_마지막.xlsx')    

    def start_requests(self):
        for loc in self.df['addr1'].values:
            if len(loc.split()) == 1:
                search = loc + ' 여행'
            else:
                search = loc.split()[1][:-1] + ' 여행'
            url = "https://map.naver.com/v5/api/search?caller=pcweb&query={}&type=all%page=1&displayCount=20&isPlaceRecommendationReplace=true&lang=ko".format(search)
            yield scrapy.Request(url=url, callback=self.parsejs)

    def parsejs(self, response):
        js = json.loads(response.body)
        for i in range(20):
            doc = ScrapyprojectItem()
            doc['id1'] = js['result']['place']['list'][i]['id']
            doc['name'] = js['result']['place']['list'][i]['name']
            doc['category'] = js['result']['place']['list'][i]['category']
            doc['context'] = js['result']['place']['list'][i]['context']
            doc['addr'] = js['result']['place']['list'][i]['address']
            doc['rank'] = js['result']['place']['list'][i]['rank']
            yield doc
