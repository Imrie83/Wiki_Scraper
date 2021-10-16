from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

def extract_list(url, xpath):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--lang=it");
    driver = webdriver.Chrome('/home/imrie/Downloads/chromedriver', options=options)
    driver.get(url)
    table = []
    # get the list of terms
    words = driver.find_element_by_xpath(xpath).text
    table.extend(words.split('\n'))
    driver.close()
    return table

pages = ['Comunit%C3%A0_ebraiche_italiane', 'Cimiteri_ebraici_in_Italia',
         'Musei_ebraici_in_Italia','Ghetti_ebraici_in_Italia','Sinagoghe_in_Italia']

df_dict = {}
xpath = '//*[@id="mw-content-text"]'
table = {}
base_url = 'https://it.wikipedia.org/wiki/'
for page in pages:
    name = page.replace('_', ' ').title().replace('%C3%A0', 'à')
    print(name)
    url = base_url + page
    table[page] = extract_list(url,xpath)
    df_dict[page] = pd.DataFrame(table[page], columns=['value'])
    df_dict[page]['category'] = name

df = pd.DataFrame(df_dict[pages[0]])
for i in range(1,len(pages)):
    df = pd.concat([df, df_dict[pages[i]]])

df.to_csv('data/raw_data.csv')