from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import html5lib
def get_job_links(job_title, location):
    # Format the inputs for URL query
    formatted_job_title = job_title.replace(' ', '+')
    formatted_location = location.replace(' ', '+')

    # Construct Indeed search URL based on user input
    main_link = f'https://www.indeed.com/jobs?q={formatted_job_title}&l={formatted_location}'

    # Initialize WebDriver
    driver = webdriver.Chrome()  # Make sure ChromeDriver is properly set up
    driver.get(main_link)
    sleep(2)

    # Find job cards
    indeed_cards = driver.find_elements(By.XPATH, '//div[@class="job_seen_beacon"]')
    print(indeed_cards)

    # Initialize lists for storing job details
    my_card_link_list = []
    heads = "https://www.indeed.com"

    # Extract job links
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

# Prompt user for job title and location
job_title = input("Enter the job title you're looking for (e.g., 'data analyst entry level'): ")
location = input("Enter the job location (e.g., 'Remote' or 'New York'): ")

# Get job links
job_links = get_job_links(job_title, location)
print("Job Links:", job_links)
