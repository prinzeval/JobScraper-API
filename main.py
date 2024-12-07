
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from supabase import create_client, Client
import os

app = FastAPI()

# Supabase credentials
url = "https://qfwipzqywzjqoxzvrlxt.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmd2lwenF5d3pqcW94enZybHh0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjAyNzQ1NzksImV4cCI6MjAzNTg1MDU3OX0.067C1RDQsklIyPs8Hr8eH5N-pu5jJ2pqV4wTZkcrbkM"
supabase: Client = create_client(url, key)

# Model for input data
class JobSearch(BaseModel):
    job_title: str
    location: str

def initialize_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def scrape_job_links(driver, job_title, location):
    formatted_job_title = job_title.replace(' ', '+')
    formatted_location = location.replace(' ', '+')
    main_link = f'https://www.indeed.com/jobs?q={formatted_job_title}&l={formatted_location}'
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
    return my_card_link_list

def scrape_job_details(driver, my_card_link_list):
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
        sharksoup = BeautifulSoup(html_content, 'html.parser')
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
    return {
        'position': position_list,
        'company_name': company_name_list,
        'location': location_list,
        'salary': salary_list,
        'job_link': var_job_link_list,
        'benefits': benefit_list,
        'description': description_list,
        'employment_type': employment_type_list
    }

def save_to_csv(data, file_path):
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)
    return file_path

def upload_to_supabase(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"Error: The file '{file_path}' does not exist.")
    df = pd.read_csv(file_path)
    if df.empty:
        raise ValueError("Error: The CSV file is empty.")
    df.columns = ['POSITION', 'COMPANY NAME', 'LOCATION', 'SALARY', 'JOB LINK', 'BENEFITS', 'DESCRIPTION', 'EMPLOYMENT TYPE']
    df = df.astype(str).replace('nan', '')
    records = df.to_dict(orient='records')
    response = supabase.table('Job_listing').insert(records).execute()
    return response.data

@app.post("/search_jobs")
def search_jobs(job: JobSearch):
    driver = initialize_driver()
    try:
        job_links = scrape_job_links(driver, job.job_title, job.location)
        job_details = scrape_job_details(driver, job_links)
        file_path = save_to_csv(job_details, 'output.csv')
        uploaded_data = upload_to_supabase(file_path)
        return {"uploaded_data": uploaded_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        driver.quit()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
# Run the FastAPI app with: uvicorn script_name:app --reload

