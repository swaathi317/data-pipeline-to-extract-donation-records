# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import json

# constants
site_name = "https://www.charitydata.ca"


def main():

    with open('./data_extraction/charity_list_metadata.json') as f:
        charity_metadata = json.load(f)

    driver = webdriver.Chrome()

    offset_increment = 100
    charities_arr = []

    for charity_obj in charity_metadata:
        i = 0

        offset_end = int(charity_obj['total_results'])

        url = charity_obj['url']
        employee_range = charity_obj['range_encoding']
        print(employee_range)

        while (i < offset_end):

            pagination_url = url + str(i)

            # Load the page from url
            driver.get(pagination_url)

            # Wait for all the article elements to be loaded
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_all_elements_located(
                (By.TAG_NAME, "article")))

            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Find all the article elements
            articles = soup.find_all('article')

            if(articles):
                for article in articles:
                    charity_data = {}
                    charity_data['charity_link'] = site_name + \
                        article.find('a').get('href')
                    charity_data['charity_name'] = article.find('h4').string
                    charity_data['full_time_employees'] = employee_range
                    charities_arr.append(charity_data)

            i = i + offset_increment

    charities_df = pd.DataFrame(charities_arr)
    charities_df.to_csv(
        './data_extraction/charity_list_employees.csv', index=False)


if __name__ == '__main__':
    main()
