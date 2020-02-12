from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import sys
import re
import pandas as pd

chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox) # linux only
# chrome_options.add_argument("--headless")

prefs = {
  "translate_whitelists": {"zh":"en"},
  "translate":{"enabled":'True'}
}
#   "intl.accept_languages": {"ja-jp,ja"}
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_experimental_option("prefs", {'--lang':'en'})
# options.add_experimental_option('prefs', {'intl.accept_languages': 'de_DE'})
# chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
# chrome_options.add_argument("--lang=en-US")

driver = webdriver.Chrome(executable_path='/Users/gcounihan/Downloads/chromedriver',options=chrome_options)
# driver = webdriver.Chrome(executable_path='/Users/gcounihan/Downloads/chromedriver')
import requests
from bs4 import BeautifulSoup
other_data_source = 'https://news.163.com/special/epidemic/?spssid=7283291fcdba1d8c2d13ee3da2cfb760&spsw=7&spss=other#map_block'
driver.get(other_data_source)
elem = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/ul[1]') #.click()

resp = requests.get(other_data_source)
resp.content

soup = BeautifulSoup(resp.text, 'html.parser')

from lxml import html
tree = html.fromstring(resp.text)


other_data_source = 'https://news.163.com/special/epidemic/?spssid=7283291fcdba1d8c2d13ee3da2cfb760&spsw=7&spss=other#map_block'
# chinese version
driver.get(other_data_source)
elem = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]')
tree = html.fromstring(elem.get_attribute('innerHTML'))
provinces = [i.text for i in tree.xpath('//ul//div//font//font')]#[:20]

everything = [i.strip() for i in tree.xpath('//ul//text()') if i.strip() != '']
# 2362

chinese_cities = [i.strip() for i in tree.xpath('//ul//li[@class="hasCities"]//ul//text()') if i.strip() != '']
chinese_provinces = [i.strip() for i in tree.xpath('//ul//div[@class="province"]//text()') if i.strip() != '']

chinese_everything = [i.text.strip() for i in tree.xpath('//ul//span')]
chinese_everything[-20:]

other_countries = [i for i in tree.xpath('//ul//li[@class="overseas"]//text()')]

if '待更新' in everything:
    incomplete = True


# english version if I can figure out how to translate
driver.get(other_data_source)
elem = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]')
tree = html.fromstring(elem.get_attribute('innerHTML'))
everything = [i.strip() for i in tree.xpath('//ul//text()') if i.strip() != '']
# 2362

import re
chinese_cities = [i.strip() for i in tree.xpath('//ul//li[@class="hasCities"]//ul//text()') if i.strip() != '']
chinese_city_names = [c for c in chinese_cities if len(re.findall('\d',c)) == 0]
# 2144
chinese_provinces = [i.strip() for i in tree.xpath('//ul//div[@class="province"]//text()') if i.strip() != ''] 
# 170
chinese_province_names = [p for p in chinese_provinces if len(re.findall('\d',p)) == 0]

chinese_everything = everything[:-len(other_countries)]

def province_details(chinese_everything,chinese_province_names,chinese_city_names):
    province_level = {}
    for i,r in enumerate(chinese_everything):
        if r in chinese_province_names:
            province_name = r
            province_level[province_name]['total'] = {
                'new_cases':chinese_everything[i+1],
                'diagnosed':chinese_everything[i+2],
                'deaths':chinese_everything[i+3],
                'recovered':chinese_everything[i+4]
                }
        if r in chinese_city_names:
            city_name = r
            province_level[province_name][city_name] = {
                'new_cases':chinese_everything[i+1],
                'diagnosed':chinese_everything[i+2],
                'deaths':chinese_everything[i+3],
                'recovered':chinese_everything[i+4]
                }
    return province_level


# chinese_cities = [i.text.strip() for i in tree.xpath('//ul//li[@class="hasCities"]//ul//font//font')] 
# chinese_provinces = [i.text.strip() for i in tree.xpath('//ul//div[@class="province"]//font//font')] 
# chinese_everything = [i.text.strip() for i in tree.xpath('//ul//li//font//font')] 

set(chinese_provinces) - set(chinese_everything)
set(chinese_everything) - set(chinese_provinces)
set(set(chinese_everything) - set(other_countries)) 
set(chinese_everything) ^ set(chinese_cities)

# other_countries = [i.text.strip() for i in tree.xpath('//ul//li[@class="overseas"]//font//font')] 
other_countries = [i.strip() for i in tree.xpath('//ul//li[@class="overseas"]//text()') if i.strip() != ''] 

if 'to be updated ' in everything:
    incomplete = True

incomplete



print(h)
soup.find('li')
class="province_th_wrap"
chrome_options = Options()
# chrome_options.add_argument("--lang=en")
# chrome_options.add_argument("--enable-translate")
prefs = {
  "translate_whitelists": {"zh":"en"},
  "translate":{"enabled":True}
}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(
    executable_path='/Users/gcounihan/Downloads/chromedriver',
    options=chrome_options
)
driver.get(other_data_source)

driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]/ul[1]')
# driver.close()

url = "https://www.google.com/maps/d/u/0/viewer?mid=1a04iBi41DznkMaQRnICO40ktROfnMfMx&ll=22.543096000000013%2C114.05786499999999&z=8"
sleep_time = 1

# other_data_source = 'https://docs.google.com/spreadsheets/d/1yZv9w9zRKwrGTaR-YzmAqMefw4wMlaXocejdxZaTs6w/htmlview?usp=sharing&sle=true#'

def go_to_google_map(url):
    driver.get(url)
    time.sleep(5)

map_lists = {
    'cities_with_deaths':'/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[2]/div/div',
    'cities':'/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div',
    'regions':'/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[3]/div/div[3]/div[2]/div/div'
}

def expand_city_list():
    print('cities with deaths')
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[2]/div/div').click()
    time.sleep(sleep_time)

def open_city_details(id):
    driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/div/div[3]/div[{id+3}]').click()
    time.sleep(sleep_time)

def expand_region_list():
    print('regions')
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/div/div').click()
    time.sleep(sleep_time)

def open_region_details(id):
    driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[2]/div/div/div[2]/div/div/div[2]/div[2]/div/div[3]/div[{id+3}]').click()
    time.sleep(sleep_time)

def scrape_details():
    try: 
        name = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div/div[4]/div[1]/div[1]/div[2]').text
    except:
        name = ''
    try:
        desc = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div/div[4]/div[1]/div[2]/div[2]').text
    except:
        desc = ''
    try:
        google_loc = driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div/div[4]/div[2]/div[2]').text
    except:
        google_loc = ''
    return name, desc, google_loc

def close_details():
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[4]/div/div/div[3]/div[1]/div/span/span/span').click()
    time.sleep(2)

def parse_name(name):
    # current_cases, current_deaths = re.findall('\[[A-Z]* - (.*) / (.*)\]',name)[0]
    # current_cases = current_cases.replace(',','')
    # current_deaths = current_deaths.replace(',','')
    # print(current_cases)
    # print(current_deaths)
    print(name)
    name = name.lower()
    count = re.findall('\[[a-z]* - (.*)\]',name)
    # count = re.findall('\[[A-Z]* - (.*)\]',name)
    city_region = re.findall('\[.*\] (.*)',name)
    return city_region, count

def parse_desc(desc):
    odesc = desc
    desc = desc.lower()
    nums = {
        '1':['first','second','third','fourth','one','1st','2nd','3rd','4th','5th'],
        '2':['two'],
        '3':['three'],
        '4':['four'],
        '5':['five'],
        '6':['six'],
        '7':['seven'],
        '8':['eight'],
        '9':['nine'],
        '10':['ten']
    }
    for num, word_nums in nums.items():
        for word_num in word_nums:
            desc = desc.replace(word_num,num)

    for d in desc.split('\n'):
        date = re.findall('(.*):',d)
        # cases = re.findall('.*:.* ([1-9,]+.+case[s]?).*',d)
        # deaths = re.findall('.*:.* ([1-9,]+.+death[s]?).*',d)
        cases = re.findall('\d+[^:]+?case[s]?',d)
        deaths = re.findall('\d+[^:]+?death[s]?',d)
        print(d)
        print(date)
        print(cases)
        print(deaths)
    return date, cases, deaths



go_to_google_map(url)
expand_city_list()

i = 0
records = []
date = datetime.now().strftime('%Y-%m-%d')
while True:
    record = {}
    try:
        open_city_details(i)
    except:
        break
    
    name, desc, loc = scrape_details()
    city, count = parse_name(name)
    
    record['date'] = date
    record['name'] = name
    record['desc'] = desc
    record['city'] = city
    record['count'] = count
    record['loc'] = loc
    records.append(record)
    
    try:
        close_details()
    except:
        break
    i += 1
    # if i == 5: break

expand_city_list()
expand_region_list()

i = 0
while True:
    record = {}
    try:
        open_region_details(i)
    except:
        break
    
    name, desc, loc = scrape_details()
    region, count = parse_name(name)
    
    record['date'] = date
    record['name'] = name
    record['desc'] = desc
    record['region'] = region[0]
    record['count'] = count[0]
    record['loc'] = loc
    records.append(record)
    
    try:
        close_details()
    except:
        break
    i += 1
    # if i == 5: break



driver.close()

print('number of records:',len(records))
pd.DataFrame(records).to_csv(f'{date}_ncov.csv',sep='|')

# l = [{'date': '2020-01-31', 'name': '[CHN - 2,639 / 159] Wuhan, Hubei', 'desc': 'Dec. 30: "Urgent notice on the treatment of pneumonia of unknown cause" - Wuhan\nDec. 31: 27 people with pneumonia of unknown cause reported to the WHO.\nJan. 9: WHO confirmed that a novel coronavirus had been isolated from one person who was hospitalised. 41 cases confirmed.\nJan. 19: 198 cases, 3 deaths\nJan. 20: 1 more death confirmed.\nJan. 21: 60 more cases, 2 deaths.\nJan. 22: City put on lockdown.\nJan. 23: 62 new cases, 8 deaths. * Hubei reported 17 deaths, all in Wuhan.\nJan. 24: 70 new cases. (Changing number from 390 to 495 due to official number given by Hubei). * 6 new deaths.\nJan. 24: 77 new cases, 15 new deaths.\nJan. 25: Death of a doctor confirmed. * 46 new cases, 6 new deaths.\nJan. 26: 80 new cases and 18 new deaths.\nJan. 28: 892 new cases and 22 new deaths.\nJan. 29: 315 new cases. 19 new deaths.\nJan. 30: 356 new cases and 25 deaths.\nJan. 31: 378 new cases. 30 new deaths.', 'city': 'Wuhan, Hubei', 'count': '2,639 / 159'}, {'date': '2020-01-31', 'name': '[THA - 5] Bangkok, Central Region (Capital)', 'desc': 'Jan. 13: First confirmed case of Wuhan resident visiting Bangkok since Jan. 8th.\nJan. 17: Second confirmed case at airport, person arrived from Wuhan. Transferred to Nonthaburi.\nJan. 19: Third confirmed case at airport. (Imported - transferred to Nonthaburi)\nJan. 24: One more case, wife of 4th case. Might have been locally transmitted, waiting for more info.\nJan. 26: One more case.', 'city': 'Bangkok, Central Region (Capital)', 'count': '5'}, {'date': '2020-01-31', 'name': '[CHN - 110] Shenzhen, Guangdong', 'desc': 'Jan. 19: First confirmed case in Guangdong of man that visited relatives in Wuhan.\nJan. 20: Eight more cases confirmed.\nJan. 21: One more case.\nJan. 22: 4 more cases.\nJan. 23: 1 more case.\nJan. 25: 5 more cases. Total 20 cases (red).\nJan. 26: 6 more cases. * 4 more cases. One case added from previous update.\nJan. 27: 5 more cases.\nJan. 28: 13 new cases. * 8 new cases.\nJan. 29: 6 new cases. \nJan. 30: 23 new cases. 4th city with 100+ cases outside Hubei. \nJan. 31: 24 new cases. ', 'city': 'Shenzhen, Guangdong', 'count': '110'}, {'date': '2020-01-31', 'name': '[CHN - 121 / 1] Beijing municipality (capital)', 'desc': 'Jan. 19: First two confirmed cases of people that visited Wuhan.\nJan. 20: Three more imported cases.\nJan. 21: Five new imported cases.\nJan. 22: Four new cases, imported.\nJan. 23: Eight confirmed cases. 2 locally transmitted. * 4 more cases.\nJan. 24: 3 more cases. * 5 more cases.  * 2 more cases.\nJan. 25: 5 more cases. * 10 more cases.\nJan. 26: 3 more cases, locally transmitted. * 9 more cases, 3 locally transmitted. * 5 more cases.\nJan. 27: 4 more cases. * First death and 8 more cases.\nJan. 28: 11 new cases.\nJan. 29: 11 new cases. 2nd city with over a 100 cases outside Hubei. * 9 new cases.\nJan. 30: 3 new cases. * 7 new cases.', 'city': 'Beijing municipality (capital)', 'count': '121 / 1'}, {'date': '2020-01-31', 'name': '[CHN - 26] Zhuhai, Guangdong', 'desc': 'Jan. 20: Three cases confirmed. Transmission among family members. First human-to-human transmission reported outside Wuhan.\nJan. 21: One more case.\nJan. 24: Four more cases.\nJan. 25: Two more cases.\nJan. 26: Two more cases.\nJan. 29: 2 new cases. \nJan. 30: 4 new cases. 22 total (red). \nJan. 31: 8 new cases. ', 'city': 'Zhuhai, Guangdong', 'count': '26'}, {'date': '2020-01-31', 'name': '[CHN - 11] Zhanjiang, Guangdong', 'desc': 'Jan. 20: First confirmed case.\nJan. 21: Second confirmed case.\nJan. 26: Two more cases.\nJan. 27: One more case.\nJan. 28: 2 new cases.\nJan. 29: 2 new cases.\nJan. 30: 2 new cases. \nJan. 31: 2 new cases. 2 cases have been removed to match with the official numbers.', 'city': 'Zhanjiang, Guangdong', 'count': '11'}, {'date': '2020-01-31', 'name': '[CHN - 17] Huizhou, Guangdong', 'desc': 'Jan. 20: First confirmed case.\nJan. 24: Four more cases.\nJan. 25: Two more cases.\nJan. 26: One more case.\nJan. 28: 3 new cases.\nJan. 29: 1 new case.\nJan. 30: 5 new cases.', 'city': 'Huizhou, Guangdong', 'count': '17'}, {'date': '2020-01-31', 'name': '[CHN - 128 / 1] Shanghai municipality', 'desc': 'Jan. 20: First confirmed case (imported).\nJan. 21: Second confirmed case, 4 suspected.\nJan. 21: 4 more cases, 3 imported and one transmitted. \nJan. 22: 3 more cases.\nJan. 23: 7 more cases.\n* 4 more cases.\nJan. 25: 13 new cases.\n* First death reported, 7 new cases.\nJan. 27: 13 new cases, 12 of the 53 cases were locally transmitted and 20 cases were foreigners. \nJan. 28: 13 new cases.\nJan. 29: 14 new cases. * 16 new cases.\nJan. 30: 5 new cases. 3rd city outside Hubei reaching 100+ cases. * 11 new cases.\nJan. 31: 16 new cases.', 'city': 'Shanghai municipality', 'count': '128 / 1'}, {'date': '2020-01-31', 'name': '[KOR - 2] Incheon, SCA', 'desc': 'Jan. 20: First confirmed case, detected at Incheon International Airport (imported).\nJan. 24: Second confirmed case, detected at Incheon Int. Airport. (Transferred to Seoul).\nJan. 26: Third confirmed case, according to officials the man engaged in normal activities after flying into Incheon International Airport. (Transferred to Goyang).\nJan. 31: One new case identified at Incheon Airport.', 'city': 'Incheon, SCA', 'count': '2'}, {'date': '2020-01-31', 'name': '[CHN - 1] Guiyang, Guizhou', 'desc': 'Jan. 21: First confirmed case.', 'city': 'Guiyang, Guizhou', 'count': '1'}]
# d = 'Jan. 26: 6 more cases. * 4 more cases. One case added from previous update.'
# date = re.findall('(.*: )',d)
# date
# d = d.replace(date[0],'')
# re.findall('[:]? ([1-9,]+.+?case[s]?)',d)
# re.findall('\d+[^:]+?case[s]?',d)
# re.findall('[:]?\d+[.^:]+?case[s]?',d)
# list(re.finditer('([1-9,]+.+?case[s]?)',d))

# re.findall('(\d+.+case[s]?)',d)

# l = desc.split('\n')
# d = l[2]; d

# re.findall('.*:.* ([1-9,]+.+case[s]?).*',d)

# for d in desc.split('\n'):
#     date = re.findall('(.*):',d)
#     cases = re.findall('.*:.* ([1-9,]+.+case[s]?).*',d)
#     deaths = re.findall('.*:.* ([1-9,]+.+death[s]?).*',d)

#     # re.findall('.*:.* ([1-9,]+.+case[s]?).*',d)
#     # re.findall('.*:.* ([1-9,]+.+death[s]?).*',d)

#     # re.findall('.*:.*([0-9]+[0-9]+[0-9]+.*death[s]?)',d)
#     # re.findall('.*:.*([1-9]*.*death[s]?)',d)  # good but not there
#     # print(re.findall('.*: ([1-9]+.*),([1-9]+.*)',d))

#     # re.findall('.*: ([1-9]*.*),.*',d)

# d



# re.findall('\[.*\] (.*)',name)
# re.findall('\[[A-Z]* - (.*) / (.*)\]',name)




# driver.close()

# try:
#     # find elements and input
#     element_username = driver.find_element_by_xpath("//input[@name='username']")
#     element_username.send_keys(username)
#     element_password = driver.find_element_by_xpath("//input[@name='password']")
#     element_password.send_keys(password)
#     element_password.send_keys(Keys.RETURN)

#     time.sleep(2)
#     driver.find_element_by_xpath('//button[normalize-space()="Not Now"]').click()
#     driver.find_element_by_xpath("/html/body/div[2]/div/div[2]/div/div/button").click()

#     print('past button clicking')
#     time.sleep(3)

#     # print('scrolling')
#     # html = driver.find_element_by_tag_name('html')
#     # html.send_keys(Keys.END)

#     driver.execute_script("window.open('https://www.instagram.com/natgeo/', 'new_window')")
#     time.sleep(2)
#     print(driver.find_element_by_xpath("//section/main/div/ul/li[1]/span/span").text)
#     #driver.find_element_by_link_text(" likes").click()


#     driver.find_element_by_xpath("//span[@class='uDNXD']").click()

#     # time.sleep(2)
#     # print('trying click')
#     # driver.find_element_by_xpath("//a[contains(@class, 'zV_Nj')]").click()
#     # time.sleep(2)
#     #
#     # print('next click')
#     # driver.find_element_by_xpath("//a[@class='zV_Nj']").click()
#     # #driver.execute_script("window.open('http://google.com', 'new_window')")
#     # time.sleep(2)
#     # time.sleep(2)
#     # print('writing')
#     # with open('source.txt','w') as text:
#     #     text.write(driver.page_source)

# except Exception as e:
#     print(e)
#     #driver.close()