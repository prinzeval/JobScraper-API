from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import html5lib

def get_job_links(job_title, location):
    formatted_job_title = job_title.replace(' ', '+')
    formatted_location = location.replace(' ', '+')
    main_link = f'https://www.indeed.com/jobs?q={formatted_job_title}&l={formatted_location}'
    driver = webdriver.Chrome()
    driver.get(main_link)
    sleep(2)
    indeed_cards = driver.find_elements(By.XPATH, '//div[@class="job_seen_beacon"]')
    my_card_link_list = []
    heads = "https://www.indeed.com"
    for WebElement in indeed_cards:
        sleep(3)
        elementHTML = WebElement.get_attribute('outerHTML')
        elementsoup = BeautifulSoup(elementHTML, 'html5lib')
        card_link = elementsoup.find('a', href=True)
        if card_link:
            card_join = card_link['href']
            my_card_link = heads + card_join
            my_card_link_list.append(my_card_link)
    driver.quit()
    return my_card_link_list

def extract_job_details(job_title, location, file_path):
    # Get job links
    my_card_link_list = get_job_links(job_title, location)
    
    driver = webdriver.Chrome()
    position_list = []
    company_name_list = []
    location_list = []
    salary_list = []
    var_job_link_list = []
    benefit_list = []
    description_list = []
    employment_type_list = []
    
    for lines in my_card_link_list:
        driver.get(lines)
        sleep(2)
        html_content = driver.page_source
        sharksoup = BeautifulSoup(html_content, 'html5lib')
        
        linkz = sharksoup.find('div', {'class': 'jobsearch-InfoHeaderContainer jobsearch-DesktopStickyContainer css-zt53js eu4oa1w0'})
        position = linkz.find('h1').text.strip() if linkz and linkz.find('h1') else "NULL"
        position_list.append(position)
        
        company_name_element = linkz.find('span', {'class': "css-1saizt3 e1wnkr790"})
        company_name = company_name_element.text.strip() if company_name_element else "NULL"
        company_name_list.append(company_name)
        
        location = "NULL"
        location_1 = linkz.find('div', {'class': "css-waniwe eu4oa1w0"}).text.strip() if linkz and linkz.find('div', {'class': "css-waniwe eu4oa1w0"}) else "NULL"
        location_2 = linkz.find('div', {'class': "css-17cdm7w eu4oa1w0"}).text.strip() if linkz and linkz.find('div', {'class': "css-17cdm7w eu4oa1w0"}) else "NULL"
        if location_1 != "NULL" and location_2 != "NULL":
            location = f"{location_1}, {location_2}"
        elif location_1 != "NULL":
            location = location_1
        elif location_2 != "NULL":
            location = location_2
        location_list.append(location)
        
        salary = linkz.find('span', {'class': "css-19j1a75 eu4oa1w0"})
        salary_text = salary.text.strip() if salary else "NULL"
        salary_list.append(salary_text)
        
        apply_link_container = sharksoup.find('div', {'id': 'viewJobButtonLinkContainer', 'class': 'icl-u-lg-inlineBlock viewJobButtonLinkContainer css-aunbg2 eu4oa1w0'})
        job_link = None
        if apply_link_container:
            button_tag = apply_link_container.find('button', class_='css-1oxck4n e8ju0x51')
            job_link = button_tag.get('href') if button_tag else "No job link found"
            var_job_link_list.append(job_link)
        
        employment = sharksoup.find('div', {'class': 'css-1xkrvql eu4oa1w0'})
        employ = employment.find('span', {'class': "css-k5flys eu4oa1w0"}).text.strip() if employment and employment.find('span', {'class': "css-k5flys eu4oa1w0"}) else "NULL"
        employment_type_list.append(employ)
        
        benefit = sharksoup.find('div', {'id': "benefits", 'data-testid': "benefits-test", 'class': "css-eynugf eu4oa1w0"})  
        benefits_list = []
        if benefit:
            ul_element = benefit.find('ul', {'class': 'css-8tnble eu4oa1w0'})
            if ul_element:
                benefits_list = [li_element.text.strip() for li_element in ul_element.find_all('li')]
        benefit_list.append(benefits_list if benefits_list else "No benefits found.")
        
        description_div = sharksoup.find('div', {'id': "jobDescriptionText", 'class': "jobsearch-JobComponent-description css-16y4thd eu4oa1w0"})
        description = description_div.text.strip() if description_div else "NULL"
        description_list.append(description)
    
    Job_link_list = []
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    
    for job_link in var_job_link_list:
        try:
            driver.get(job_link)
            WebDriverWait(driver, 20).until(EC.url_changes(job_link))
            time.sleep(1)
            redirected_url = driver.current_url
            Job_link_list.append(redirected_url)
        except Exception as e:
            print(f"Error processing {job_link}: {e}")
    
    driver.quit()
    
    TABLE = {
        'POSITION': position_list,
        'COMPANY NAME': company_name_list,
        'LOCATION': location_list,
        'SALARY': salary_list,
        'JOB LINK': Job_link_list,
        'BENEFITS': benefit_list,
        'DESCRIPTION': description_list,
        'EMPLOYMENT TYPE': employment_type_list
    }
    daf = pd.DataFrame(TABLE)
    daf.to_csv(file_path, index=False)
    print("DataFrame successfully saved to CSV file.")

# Example usage:
job_title = input("Enter the job title you're looking for (e.g., 'data analyst entry level'): ")
location = input("Enter the job location (e.g., 'Remote' or 'New York'): ")
file_path = r'C:\Users\valen\Desktop\JOB-WEBSITE\output.csv'
extract_job_details(job_title, location, file_path)
