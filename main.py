from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd


def extract_list(url, xpath):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--lang=it")
    driver = webdriver.Chrome('/home/imrie/Downloads/chromedriver', options=options)
    driver.get(url)
    table = []
    # get the list of terms
    words = driver.find_element_by_xpath(xpath).text
    table.extend(words.split('\n'))
    driver.close()
    return table


pages = ['Comunit%C3%A0_ebraiche_italiane', 'Cimiteri_ebraici_in_Italia',
         'Musei_ebraici_in_Italia', 'Ghetti_ebraici_in_Italia', 'Sinagoghe_in_Italia']

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

df = pd.read_csv('data/raw_data.csv')
index_na = 83


def is_active(x, index_na):
    if x < index_na:
        return True
    return False


df['is_active'] = df['Unnamed: 0'].apply(lambda x: is_active(x, index_na))
bag_words = [
    'Comunità ebraica di', '(Provinc', '(Region', ' Provinc', 'ex circondario', 'Cimitero ebraico di',
    'Museo ebraico di', 'Ghetto di', 'Sinagoga di', 'Cimitero israelitico di',
    'Cimitero monumentale ebraico di'
]


def is_locality(x):
    for bag in bag_words:
        if bag in x:
            return True
    return False


df['is_locality'] = df['value'].apply(lambda x : is_locality(x))
df = df[df['is_locality'] == True]
df.reset_index(inplace = True)
