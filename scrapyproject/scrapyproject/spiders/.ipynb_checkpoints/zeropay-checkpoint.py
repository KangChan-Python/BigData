# -*- coding: utf-8 -*-
import scrapy
import json
import math
from scrapyproject.items.zeropay_items import ScrapyprojectItem


class ZeropaySpider(scrapy.Spider):
    name = 'zeropay'
    

    def start_requests(self):
        # 첫 인덱스를 확인하면서 총 몇 건이 있는지 확인하기
        
        for i in range(1,18):
            url = "https://www.zeropay.or.kr/intro/frncSrchList_json.do?bztypName=%EC%9D%8C%EC%8B%9D&frc_se=%EC%9D%8C%EC%8B%9D&pageIndex=1&recordCountPerPage=10&firstIndex=1&lastIndex=10&tryCode="
            if i < 10:
                num = '0' + str(i)
            else:
                num = str(i)
            url = url + num
            print(url)
            # meta 는 callback 되는 함수에 변수 전달 기능
            yield scrapy.Request(url = url , callback = self.getTotalNum , meta = {'code' : num})

    def getTotalNum(self,response):
        # json 파일 로드
        js = json.loads(response.body)
        # item 객체
        
        # 첫 번째 페이지 미리 담기
        list1 = js['list']
        for tags in list1:
            doc = ScrapyprojectItem()
            doc['rownum'] = tags['rowNum']
            doc['bztype'] = tags['bztypName'] 
            doc['addr'] = tags['pobsBaseAddr']
            doc['tel'] = tags['pobsGnrlTelno']
            doc['name'] = tags['pobsDtlAddr']
            yield doc

        totalnum = math.ceil(float(js['totalCnt']) / 10.0) + 1
        for i in range(2,totalnum):
            f_idx = 1 + 10 *( i-1)
            l_idx = i*10
            url = "https://www.zeropay.or.kr/intro/frncSrchList_json.do?bztypName=%EC%9D%8C%EC%8B%9D&frc_se=%EC%9D%8C%EC%8B%9D&pageIndex={}&recordCountPerPage=10&firstIndex={}&lastIndex={}&tryCode={}".format(i, f_idx, l_idx, response.meta['code'])
            yield scrapy.Request(url = url , callback = self.parseTags)
        
    def parseTags(self, response):
        js = json.loads(response.body)
        list1 = js['list']
        for tags in list1:
            doc = ScrapyprojectItem()
            doc['rownum'] = tags['rowNum']
            doc['bztype'] = tags['bztypName'] 
            doc['addr'] = tags['pobsBaseAddr']
            doc['tel'] = tags['pobsGnrlTelno']
            doc['name'] = tags['pobsDtlAddr']
            yield doc
        