"""
Could add while 'to be updated' wait..
"""


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import pandas as pd
from lxml import html
import time

def chinese_province_details(chinese_everything,chinese_province_names,chinese_city_names):
    "converts chinese char html"
    country_name = 'China'
    province_level = []
    for i,r in enumerate(chinese_everything):
    #     print(i,r)
        if r in chinese_province_names:
            province_name = r
            province_level.append({
                'as_of':date,
                'country':country_name,
                'province':province_name,
                'city':'',
                'new_cases':chinese_everything[i+1],
                'diagnosed':chinese_everything[i+2],
                'deaths':chinese_everything[i+3],
                'recovered':chinese_everything[i+4]
                })
        if r in unknown_areas:  # only have 3, might change, need to fix
            unknown_name = r 
            if len([i for i in chinese_everything[i+1:i+5] if re.findall('\d',i)]) == 3:
                province_level.append({
                    'as_of':date,
                    'country':country_name,
                    'province':province_name,
                    'city':unknown_name,
                    'new_cases':0,
                    'diagnosed':chinese_everything[i+1],
                    'deaths':chinese_everything[i+2],
                    'recovered':chinese_everything[i+3]
                    }) 
            elif len([i for i in chinese_everything[i+1:i+5] if re.findall('\d',i)]) == 4:
                province_level.append({
                    'as_of':date,
                    'country':country_name,
                    'province':province_name,
                    'city':unknown_name,
                    'new_cases':chinese_everything[i+1],
                    'diagnosed':chinese_everything[i+2],
                    'deaths':chinese_everything[i+3],
                    'recovered':chinese_everything[i+4]
                    })
        if r in chinese_city_names:
            city_name = r

            province_level.append({
                'as_of':date,
                'country':country_name,
                'province':province_name,
                'city':city_name,
                'new_cases':chinese_everything[i+1],
                'diagnosed':chinese_everything[i+2],
                'deaths':chinese_everything[i+3],
                'recovered':chinese_everything[i+4]
                })
    return pd.DataFrame(province_level)

def other_country_details(other_countries,other_country_names):
    "converts chinese char html"
    province_level = []
    for i,r in enumerate(other_countries):
    #     print(i,r)
        if r in other_country_names:
            country_name = r
            country_cases = re.findall('\d+',other_countries[i+1])
            if len(country_cases) == 1:
                diagnosed = country_cases[0]
                deaths = 0
                recovered = 0
                new_cases = 0
            elif len(country_cases) == 2:
                diagnosed = country_cases[0]
                deaths = country_cases[1]
                recovered = 0
                new_cases = 0
            
            province_level.append({
                'as_of':date,
                'country':country_name,
                'province':'',
                'city':'',
                'new_cases':new_cases,
                'diagnosed':diagnosed,
                'deaths':deaths,
                'recovered':recovered
                })

    return pd.DataFrame(province_level)


chrome_options = Options()
prefs = {
  "translate_whitelists": {"zh":"en"},
  "translate":{"enabled":'True'}
}
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(executable_path='/Users/gcounihan/Downloads/chromedriver',options=chrome_options)

url = 'https://news.163.com/special/epidemic/?spssid=7283291fcdba1d8c2d13ee3da2cfb760&spsw=7&spss=other#map_block'
driver.get(url)
time.sleep(5)  # load

# as_of date
elem = driver.find_element_by_xpath('/html')
tree = html.fromstring(elem.get_attribute('innerHTML'))
date = tree.xpath('//div[@class="cover_time"]/text()')
as_of = '截至'
date = date[0].strip(as_of)

# data
elem = driver.find_element_by_xpath('/html/body/div[3]/div[2]/div[2]')
tree = html.fromstring(elem.get_attribute('innerHTML'))
driver.close()
to_be_updated = ['to_be_updated','待更新']
unknown_areas = ['Unspecified area','Unclear area','Unspecified area','Foreign to Shanghai','未明确地区','未明确地区']

# chinese sub parts
everything = [i.strip() for i in tree.xpath('//ul//text()') if i.strip() != '']
chinese_cities = [i.strip() for i in tree.xpath('//ul//li[@class="hasCities"]//ul//text()') if i.strip() != '']
chinese_city_names = [c for c in chinese_cities if len(re.findall('\d',c)) == 0 and c not in to_be_updated]
chinese_city_names = set(chinese_city_names) - set(unknown_areas)  # remove 'Unspecified'
chinese_provinces = [i.strip() for i in tree.xpath('//ul//div[@class="province"]//text()') if i.strip() != ''] 
chinese_province_names = [p for p in chinese_provinces if len(re.findall('\d',p)) == 0 and p not in to_be_updated]

# other countries
other_countries = [i.strip() for i in tree.xpath('//ul//li[@class="overseas"]//text()') if i.strip() != ''] 
other_country_names = [o for o in other_countries if len(re.findall('\d',o)) == 0]
chinese_everything = everything[:-len(other_countries)]

# cat both together
c_df = chinese_province_details(chinese_everything,chinese_province_names,chinese_city_names)
oc_df = other_country_details(other_countries,other_country_names)
tot_df = pd.concat([c_df,oc_df])
tot_df[['as_of','country','province','city', 'new_cases', 'diagnosed', 'deaths', 'recovered']].to_csv(f"{date.replace(' ','_')}.csv",index=False,sep='|')