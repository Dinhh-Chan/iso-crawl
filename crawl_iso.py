from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import geckodriver_autoinstaller
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
def Log_in_ISO():
    driver.get('https://www.iso.org/home.html')
    time.sleep(5)
    driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()  
    standard= input("Enter your standard: ")
    link_sum_standard= 'https://www.iso.org/search.html?q='
    link_sum_standard += standard
    driver.get(link_sum_standard)
def res():
    label_for_standards = 'Standards'
    label_for_Pages='Pages'
    label_for_news= 'News'
    label_for_Publications='Publications'
    label_for_Committees='Committees'
    res= driver.find_elements(By.ID, 'facets')
    for i in res:
        print(i.text)
    print("Below are the types of results that can be filtered. Which type would you like to choose?")
    choosen =input()
    if choosen == 'Standards':
        driver.find_element(By.CSS_SELECTOR, f'label[for="{label_for_standards}"]').click()
        crawl_data()
    # elif choosen == 'Pages':
    #     driver.find_element(By.CSS_SELECTOR, f'label[for="{label_for_Pages}"]').click()
    #     crawl_data()
    # elif choosen =='News':
    #     driver.find_element(By.CSS_SELECTOR, f'label[for="{label_for_news}"]').click()
    #     crawl_data()
    # elif choosen == 'Publications':
    #     driver.find_element(By.CSS_SELECTOR, f'label[for="{label_for_Publications}"]').click()
    #     crawl_data()
    # elif choosen =='Committees':
    #     driver.find_element(By.CSS_SELECTOR, f'label[for="{label_for_Committees}"]').click()
    #     crawl_data()
def crawl_data():
    Last_page= int(driver.find_element(By.CLASS_NAME, 'total').text)
    for page in range(1,Last_page):
        data = pd.DataFrame(columns=(['Link','Main title','Abstract', 'General informarion', 'Link read sample','File Read sample' ]))
        div_get_link= driver.find_element(By.ID, 'search-results')
        a_tag_link = div_get_link.find_elements(By.TAG_NAME,'a')
        arr_link=[]
        index= 0
        for link in a_tag_link:
            arr_link.append(link.get_attribute("href"))
        for link in arr_link:
            arr=[]
            arr.append(link)
            driver.get(link)
            time.sleep(2)
            main_title = driver.find_elements(By.TAG_NAME,'nav')
            arr.append(main_title[3].text)
            Abstract = driver.find_element(By.CSS_SELECTOR, 'div[itemprop="description"]').text
            arr.append(Abstract)
            inf = driver.find_element(By.CLASS_NAME, 'refine').text
            arr.append(inf)
            Link_Read_sampler= driver.find_elements(By.LINK_TEXT,'Read sample')
            if len(Link_Read_sampler)==0:
                arr.append(0)
                arr.append(0)
            else :
                link = Link_Read_sampler[0].get_attribute( "href")
                arr.append(link)
                driver.get(link)
                time.sleep(3)
                content= driver.find_element(By.CLASS_NAME, 'sts-standard')
                arr.append(content.text)
            data.loc[index] = arr[:6]
            index+=1 
            if index == 5 :
                break
        break 
    print(data)
    data.to_excel('./data.xlsx', index= False )
if __name__ == "__main__":
    Log_in_ISO()
    res()
    
        
        
