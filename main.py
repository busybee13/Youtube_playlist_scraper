# %% %%

from driver.chrome_driver import ChromeDriver
from datetime import timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


import pandas as pd
#  %% %%
title_xpath= ".//h1[@id='title']"
inner_envelope_xpath= "//ytd-playlist-video-renderer"
position_xpath= ".//div[@id='index-container']"
video_title_xpath= ".//a[@id='video-title']"
duration_xpath= ".//span[contains(@class, 'time')]" 
id_xpath= ".//a[@id='thumbnail']"
playlist= {}
video= {}


email= 'team@clientconnect.ai'
password= 'Dmytro43*'

email_xpath= "//input[@id='login-email']"
password_xpath= "//input[@id='login-password']"
people_search_xpath= "//a[@id='people-tab']"
# el= driver.find_elements_by_xpath(people_search_xpathinput_fname_xpath= "//input[@id='fn6']")
input_fname_xpath= "//input[@id='fn6']"
input_lname_xapth= "//input[@id='ln6']"
input_city_xapth= "//input[@id='city6']"
input_age_xapth= "//input[@id='age-lg']"
input_city_xapth= "//input[@id='city6']"
input_state_xpath= "//select[@name='state']"
search_button_xapth= "//button[@id='person-search-btn-lg']"
search_results_xpath= "//div[@id='person_results']"
result_xpath= "//ul[@class='report-overview__section-summaries']"
results_xpaths= ["//div[@id='phone-numbers-section']", "//div[@id='email-addresses-section']"]


internal_elements_xpath= ".//div[contains(@class, 'data-card-component')]"

age_xpath= ".//div[@class='age']"
name_xpath= ".//div[@class='name ']"
address_xpath= ".//div[@class='address']"
a_xpath= './a'
# %%

no_years= 1

name_col= 'Name'
age_col= 'Age'
city_col= 'City/County'
state_col= 'State'


# %%
def login(email, password):
    driver = ChromeDriver.loadDriver()
    url= 'https://www.beenverified.com/app/login'
    driver.get(url)
    el= driver.find_elements_by_xpath(email_xpath)[0]
    el.click()
    el.send_keys(email)
    el= driver.find_elements_by_xpath(password_xpath)[0]
    el.click()
    el.send_keys(password)
    el.send_keys(Keys.RETURN)
    return driver

# %%

# def erase(el):
#     el.send_keys(Keys.CONTROL + "a")
#     el.send_keys(Keys.DELETE)

def search(row, driver):
    
    el=WebDriverWait(driver, 200).until(EC.presence_of_element_located((By.XPATH, people_search_xpath)))    
    
    el= driver.find_elements_by_xpath(people_search_xpath)[0]

    # print(driver.find_elements_by_xpath(people_search_xpath))
    try:
        el.click()
    except Exception as e:
        el= driver.find_elements_by_xpath("//input[@id='fauxInput']")[0]
        el.click()
    # WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "input_fname_xpath")))
    el= ''
    sleep(2)
    try:
        el= driver.find_elements_by_xpath(input_fname_xpath)[0]
        el.click()
    except Exception as e:
        el= driver.find_elements_by_xpath(input_fname_xpath)[0]
        el.click()
    el.clear()
    # # erase(el)
    el.send_keys(row[name_col].split(' ')[0])
    el= driver.find_elements_by_xpath(input_lname_xapth)[0]
    el.click()
    el.clear()
    # erase(el)
    el.send_keys(row[name_col].split(' ')[1])
    el= driver.find_elements_by_xpath(input_city_xapth)[0]
    el.click()
    el.clear()
    # erase(el)
    el.send_keys(row[city_col])
    el= driver.find_elements_by_xpath(input_age_xapth)[0]
    el.click()
    el.clear()
    # erase(el)
    el.send_keys(str(row[age_col]))
    input_state_select= Select(driver.find_element_by_xpath(input_state_xpath))
    input_state_select.select_by_visible_text(row[state_col])
    el= driver.find_elements_by_xpath(search_button_xapth)[0]
    el.click()
# %%
from time import sleep

def mk_int(s):
    s = s.strip()
    return int(s) if s else 0
def get_links(row, driver):
    links= []
    el_div=WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, search_results_xpath)))
    sleep(2)
    try:
        el_div= driver.find_element_by_xpath(search_results_xpath)
    
        for el in el_div.find_elements_by_xpath(a_xpath):
            name= el.find_element_by_xpath(name_xpath).text.replace('unmarried', '').strip()
            try:
                age= el.find_element_by_xpath(age_xpath).text.strip()
            except Exception as e:
                age= ''
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, address_xpath)))
            
            address= el.find_element_by_xpath(address_xpath).text
            print(row[name_col].split(' ')[0], '*', row[name_col].split(' ')[1])
            print(mk_int(str(row[age_col]).strip()), row[city_col],'*' ,row[state_col])
            print(name, age, address)
            if row[name_col].split(' ')[0].strip() in name.strip() and \
                row[name_col].split(' ')[1].strip() in name.strip() and \
                mk_int(str(row[age_col]).strip()) -no_years<= mk_int(age.strip())  and \
                mk_int(str(row[age_col]).strip()) +no_years >= mk_int(age.strip())  and \
                row[city_col].strip() in address.strip() and \
                row[state_col].strip() in address.strip() :
                links.append(el.get_attribute("href"))
            # if row[name_col].split(' ')[0].strip() in name.strip() and \
            #     row[name_col].split(' ')[1].strip() in name.strip() and \
            #     mk_int(str(row[age_col]).strip()) -no_years<= mk_int(age.strip())  and \
            #     mk_int(str(row[age_col]).strip()) +no_years >= mk_int(age.strip())  and \
            #     row[state_col].strip() in address.strip() :
            #     links.append(el.get_attribute("href"))                
            print(row[name_col].split(' ')[0] in name, row[name_col].split(' ')[1] in name, \
                str(row[age_col]) in age, row[city_col] in address, row[state_col] in address
                )
        print(links)
    except Exception as e:
        links.extend([])
    return links

def get_items(row, links, driver):
    xpaths_title= ['phone_numbers', 'emails']

        
    if len(links)==0:
        for idx, el_xpath in enumerate(results_xpaths):
            row[xpaths_title[idx]]=''

    # data= {}
    for link in links:
        driver.get(link)
        for idx, el_xpath in enumerate(results_xpaths):
            el_div = WebDriverWait(driver, 100).until(EC.presence_of_element_located((By.XPATH, el_xpath)))
            # el_div= driver.find_element_by_xpath(phone_no_xpath)
            for el in el_div.find_elements_by_xpath(internal_elements_xpath)[:3]:
                # print(el.text)
                try:
                    print(row)
                    print(row[xpaths_title[idx]])
                    row[xpaths_title[idx]].append(el.find_element_by_xpath('.//p').text)
                    # row[xpaths_title[idx]]=el.find_element_by_xpath('.//p').text
                except Exception as e:
                    print(e)
                    try:
                        row[xpaths_title[idx]]=[el.find_element_by_xpath('.//p').text]
                    except Exception as e:
                        row[xpaths_title[idx]]=''
    print(row)
    return row


def get_data(row, driver):
    search(row, driver)
    links= get_links(row, driver)
    return get_items(row, links, driver)
# %% %

driver= login(email, password)

# %%
import os

df= pd.read_csv(os.path.join(os.path.dirname(__file__), 'input', 'Los Angeles County, California-06_06_2021.csv'))
result= None
result= pd.DataFrame()
for idx, row in df.iterrows():
    try:
        test= get_data(row, driver)
        print(test)
        print('*'*100)
        
        result= result.append(test)
        result.to_csv(os.path.join(os.path.dirname(__file__), 'output', 'output.csv'))
        print('-'*100)
    except Exception as e:
        print(e)
    
dir= os.path.join(os.path.dirname(__file__), 'output')




# %% output

# result

# el= driver.find_elements_by_xpath(input_fname_xpath)[0]
# el.click()
# # # erase(el)
# el.send_keys(row[name_col].split(' ')[0])
# %%

# row= {
#     'first_name': 'James',
#     'last_name': 'Smith',
#     'age': '30',
#     'city': 'Los Angeles',
#     'state': 'CA'
# }
# # %% 

# # %%
# els= person_results


