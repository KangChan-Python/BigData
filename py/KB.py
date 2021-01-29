from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import datetime, pyperclip, time, os, re


td= str(datetime.date.today())
td = td.replace('-','.')

download_dir = r"C:\Users\82107\Desktop\Research\KB\%s"%td #
path = r'https://rc.kbsec.com/report/reportList.able'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option("prefs", {
  "download.default_directory": download_dir,
  "download.prompt_for_download": False,
  "plugins.always_open_pdf_externally": True,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
options.add_argument('--headless')
chromedriver_path= r"C:\Users\82107\Desktop\Workspace\myGit\selenium\chromedriver.exe"
driver = webdriver.Chrome(chromedriver_path, options=options)

driver.get(path)
#로그인
login = driver.find_element_by_css_selector('#unionLoginId')
login.send_keys('kch961203')
password = driver.find_element_by_css_selector('#pw')
password.send_keys('pepsi1602&')
btn = driver.find_element_by_css_selector('#loginBtn')
btn.click()

#데이토 조회 대기 및 조회
time.sleep(5)
reportList = driver.find_element_by_css_selector('#reportList')
li_list = reportList.find_elements_by_css_selector('li')#reportList > 

soup = BeautifulSoup(driver.page_source, 'html')



name_list =[]
f = open(r'C:\Users\82107\Desktop\Research\KB\log\%s.txt'%td.replace('.','_') ,'a')
for txt in driver.find_elements_by_css_selector('#reportList > li > a > span'):
    text =txt.find_element_by_css_selector('i.scr_tx1.tcrop').text
    date =txt.find_element_by_css_selector('i.scr_tx5 > i.r_txt.scr_tx5_2').text

    year, month, day = date.split('.')
    if int(month) < 10:
        month = '0' +month
    if int(day) < 10:
        day = '0' + day
    date= '.'.join([year,month,day])
    if 'Buy' in text and date ==td:
        f.write(txt.text.split(')')[0]+')'+'\n')
        name_list.append(txt.text.split(')')[0]+')')

f.close()

today_list =[]
buy_hold = []
txt = []
time.sleep(1.5)
for li in soup.select('#reportList > li'):
    b = li.select('i.scr_tx5 > i.r_txt.scr_tx5_2')[0].text
    year, month, day = b.split('.')
    if int(month) < 10:
        month = '0' +month
    if int(day) < 10:
        day = '0' + day
    b= '.'.join([year,month,day])

    if td ==b:
        today_list.append(li)
#     if 'buy' in str(li.select('a')[0]):
#         print(True)
        try:
            buy_hold.append(li.select('i.ibtn')[0].text)
            txt.append(li.select('i.scr_tx1.tcrop')[0].text[:-4])

        except:
            buy_hold.append('')


href_list = []
for li in today_list:
    detail = li.select('a')[0].attrs['href']
    href_list.append('https://rc.kbsec.com/'+detail)


with open(r"C:\Users\82107\Desktop\Workspace\데이터\forMyGit\KB.txt") as f:
    key =f.readlines()

#발송 이메일
fromaddress = key[0].replace('\n','')
pw =  key[1]

#수신 이메일
toaddress = 'kch961203@gmail.com'
text = '{} KB 리서치 보고서2'.format(td)

headlist = []
table ='<strong id="content" style=" color: rgb(249, 88, 96); font-weight: bold; font-size: 28px;">목차</strong>'
# 내용 만들기
total = ''
i= 0
td = td.replace('.','_')
print(name_list)
for href, bhn in zip(href_list,buy_hold):
    driver.get(href)
    soup = BeautifulSoup(driver.page_source, 'html')
    name = soup.select('div.viewTop > div.top_txt > div > span')[0].text
    head_for_table =soup.select('body > div.wrap > div > div.content.view > div.viewTop > div.top_txt > div')[0].text

    head_for_table = head_for_table+'   ' + bhn 
    headlist.append(r'<div style="margin:5px;" ><a href ="#content%s" style="font-size:15px; color:black;" >'%i +head_for_table+r'</a></div>')
    head = str(soup.select('body > div.wrap > div > div.content.view > div.viewTop > div.top_txt > div')[0])
    a =str(soup.select('body > div.wrap > div > div.content.view > div.viewCon > div.viewCon1 > dl.viewCon1_tx1')[0])
    html_head = head
    html_body = a.replace('dt','strong').replace('\n','''<p>\n</p>''')
    html_head= html_head.replace('span','p')
    html_head= html_head.replace('class="top_txt1"','style="font-size: 15px; color:black;"')
    html_head= html_head.replace('class="top_txt2 fB"','id="content%s" style=" color: rgb(249, 88, 96); font-weight: bold; font-size: 28px;"'%i)
    html_body= html_body.replace('<strong', '<strong style="font-size:23px; font-weight:bold;color:black;"')
    html_body= html_body.replace('<dd', '<dd style=" font-size:18px;color:black;"')
    print(name)
    total = total + html_head+'<hr>'+ html_body 
    if name in name_list:
        
        name2, code =name.split('(')[0], name.split('(')[1][:-1]
        
        total = total + '<div style="margin:5px;"><a href="https://finance.naver.com/item/main.nhn?code=%s" style="font-size:15px; color:black;">%s</a></div>'%(code,name2)
    
    
    total = total +'<p><a href="#content" style="font-size:15px; color:black;" >목차</a></p> <hr>'
    
    i+=1
total = '<!DOCTYPE html><div style="width:80%; margin-right:100px; margin-left:100px; background-color:#f1efed">' + table+"".join(headlist) + total+'</div></html>'

if '{}'.format(td.replace('.','_')) not in os.listdir(r'C:/Users/82107/Desktop\Research/KB/'):
    os.makedirs(r'C:/Users/82107/Desktop\Research/KB/{}'.format(td.replace('.','_')))

f = open(r'C:/Users/82107/Desktop\Research/KB/{}/{}.html'.format(td.replace('.','_'),td.replace('.','_')),'w')
f.write(total)
f.close()
print('끝1')

td = str(datetime.date.today()).replace('-','_')

f = open(r'C:\Users\82107\Desktop\Research\KB\log\%s.txt'%td.replace('.','_') ,'r')
buy_list =[]
for line in f.readlines():
    buy_list.append(line.replace('\n',''))
f.close()


download_dir = r"C:\Users\82107\Desktop\Research\KB\%s"%td #

hankyung = r'http://consensus.hankyung.com/apps.analysis/analysis.list'
driver.get(hankyung)
driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
driver.execute("send_command", params)

during_ = driver.find_element_by_css_selector('#sdate')
during_.click()
driver.find_element_by_css_selector('body > div.ui-daterangepickercontain > div > ul > li.ui-daterangepicker-1개월.ui-corner-all').click()


name_dict= {}
time.sleep(2)
for key in buy_list:
    download_dir = r"C:\Users\82107\Desktop\Research\KB\%s"%td
    download_dir=download_dir.replace('\\','/')
    file_path =r"C:\Users\82107\Desktop\Research\KB\%s\%s"%(td,key)
    file_path=file_path.replace('\\','/')
    
    if key not in os.listdir(r"C:\Users\82107\Desktop\Research\KB\%s"%td):
        os.mkdir(file_path)
    else:
        continue
    while_condition =len(os.listdir(r"C:\Users\82107\Desktop\Research\KB\%s"%td))
    input_ = driver.find_element_by_css_selector('#search_text')
    input_.clear()
    input_.send_keys(key)
    search = driver.find_element_by_css_selector('#f_search > div > div.hd_top > div.btn_r > a:nth-child(1)')
    search.click()
    time.sleep(1)
    name_dict[key]= {}
    soup = BeautifulSoup(driver.page_source, 'html')
    tr_tag_list =soup.select('#contents > div.table_style01 > table > tbody > tr')
    for tr_tag in tr_tag_list:
        pdf_tag =tr_tag.select('td:nth-child(6) > div > a')[0].attrs['href'].split('=')[1]
        name_tag =tr_tag.select('td.text_l > a')[0].get_text()
        if '...' in name_tag:
            name_tag = tr_tag.select('#content_%s > strong'%pdf_tag)[0].get_text()
        name_dict[key][pdf_tag]=name_tag
    tr_tag_list = driver.find_elements_by_css_selector('#contents > div.table_style01 > table > tbody > tr')

    for tr_tag in tr_tag_list:
        tr_tag.find_element_by_css_selector('td:nth-child(6) > div > a').click()
        time.sleep(1)


for key in buy_list:
    try:
        for k,v in name_dict[key].items():
            download_dir = r"C:\Users\82107\Desktop\Research\KB\%s"%td
            download_dir=download_dir.replace('\\','/')
            file_path =r"C:\Users\82107\Desktop\Research\KB\%s\%s"%(td,key)
            file_path=file_path.replace('\\','/')
            
            if '%s.pdf'%k in  os.listdir(download_dir):
                v=  re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘’|\(\)\[\]\<\>`\'…》]', '',v)
                os.replace(download_dir+r'/%s.pdf'%k, file_path+r'/%s.pdf'%v)
                time.sleep(0.5)
    except:
        print("이미 있는 경우")

driver.quit()
td= str(datetime.date.today())
td = td.replace('-','.')

kiwoom = r'https://www3.kiwoom.com/nkw.templateFrame.do?m=m0600000000&&xdr=&'

download_dir=r'C:\Users\82107\Desktop\Research\Kiwoom'
if td not in os.listdir(download_dir):
    os.mkdir(download_dir+'\\'+td)
download_dir += '\\' +td
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_experimental_option("prefs", {
  "download.default_directory": download_dir,
  'profile.default_content_setting_values.automatic_downloads': 1,
  "download.prompt_for_download": False,
  "plugins.always_open_pdf_externally": True,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
driver = webdriver.Chrome(chromedriver_path,options= options)
driver.get(kiwoom)
driver.refresh()
driver.fullscreen_window()
# driver.find_element_by_css_selector('#gnbList07 > a').click()


driver.switch_to.frame(driver.find_element_by_xpath('html / frameset / frame[1]'))

driver.find_element_by_css_selector('#gnb7menu > li.on > a').click()


driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="cross_ifm"]'))

driver.find_element_by_css_selector('body > div.tbWrap01 > table > tbody > tr:nth-child(1) > td.cdata.p0 > a').click()


driver.switch_to.parent_frame()

driver.find_element_by_css_selector('#gnb7menu > li:nth-child(5) > a').click()

driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="cross_ifm"]'))

tables = driver.find_elements_by_css_selector('body > div.tbWrap01 > table > tbody > tr')



name_dict ={}
for table in tables:
    date = table.find_element_by_css_selector('td:nth-child(7)').text
    if td == date:
        table.find_element_by_css_selector('td.cdata.p0 > a').click()
        key = table.find_element_by_css_selector('td.cdata > a').get_attribute('onclick').split("','")[1]
        value = table.find_element_by_css_selector('td.ldata > a').text
        name_dict[key] =value

for k,v in name_dict.items():
    if '%s'%k in  os.listdir(download_dir):
        v=  re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘’|\[\]\<\>`\'…》]', '',v)
        os.replace(download_dir+r'/%s'%k, download_dir+r'/%s.pdf'%v)
        print(k,v)
        time.sleep(0.5)
driver.quit()

# time.sleep(3600*2)