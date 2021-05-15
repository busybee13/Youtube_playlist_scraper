# %% %%

from driver.chrome_driver import ChromeDriver
from datetime import timedelta



#  %% %%
title_xpath= ".//h1[@id='title']"
inner_envelope_xpath= "//ytd-playlist-video-renderer"
position_xpath= ".//div[@id='index-container']"
video_title_xpath= ".//a[@id='video-title']"
duration_xpath= ".//span[contains(@class, 'time')]" 
id_xpath= ".//a[@id='thumbnail']"
playlist= {}
video= {}
# %%
driver = ChromeDriver.loadDriver()

# %% %%
url= 'https://www.youtube.com/playlist?list=PL6gx4Cwl9DGBkvpSIgwchk0glHLz7CQ-7'
driver.get(url)

# %%
import re
regex = re.compile(r'((?P<hours>\d+?):)?((?P<minutes>\d+?):)?((?P<seconds>\d+?))?')


def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)

# %% %%

playlist['title']= driver.find_element_by_xpath(title_xpath).text
elements= driver.find_elements_by_xpath(inner_envelope_xpath)

playlist['videos']= []
for element in driver.find_elements_by_xpath(inner_envelope_xpath):
    print(element)
    video= {}
    video['position']= element.find_element_by_xpath(position_xpath).text
    print(video['position'])
    video['video_title']= element.find_element_by_xpath(video_title_xpath).text
    video['duration']= parse_time(element.find_element_by_xpath(duration_xpath).get_attribute('innerHTML').strip())
    video['id']= element.find_element_by_xpath(id_xpath).get_attribute("href").split('v=')[1].split('&')[0]
    playlist['videos'].append(video)

# %%
print(playlist)

# %%
