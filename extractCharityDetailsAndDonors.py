# import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time


def main():

    driver = webdriver.Chrome()

    charities_arr = []
    charity_df = pd.read_csv('./data_extraction/charity_list_employees.csv')
    start = 4509
    end = 4600
    for i in range(start, end):
        print(i)
        row = charity_df.loc[i]
        charity_link = row['charity_link']
        charity_name = row['charity_name']
        charity_employee_range = row['full_time_employees']
        # Load the page from url
        driver.get(charity_link)

        # Wait for all the article elements to be loaded
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located(
            (By.TAG_NAME, "rect")))

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        charity_details = soup.find('div', {'class': 'c_1-2'})
        charity_data_arr = charity_details.findChildren('dd')
        charity_address_arr = charity_data_arr[5].findChildren('span')
        charity_city_split = charity_address_arr[1].string.split(", ")

        link = driver.find_element(By.CSS_SELECTOR, 'a[href="#fundraising"]')
        # Select Fundraisin tab
        link.click()

        # get charity details
        charity_type = charity_data_arr[1].string
        charity_sub_category = charity_data_arr[2].string
        charity_description = charity_data_arr[0].string
        charity_registration_number = charity_data_arr[3].string
        charity_website = charity_data_arr[4].string
        charity_country = charity_address_arr[3].string
        charity_province = charity_city_split[1]
        charity_city = charity_city_split[0]

        # get gifts table data
        time.sleep(1)
        gifts_table = soup.find('table', {'class': 'gift'})
        if(gifts_table):
            gift_rows = gifts_table.find('tbody').findChildren('tr')

            for row in gift_rows:
                columns_data = row.find_all('div')

                charity_data = {}
                charity_data['donation_year'] = columns_data[0].string
                charity_data['donor_name'] = columns_data[1].string
                charity_data['donor_city'] = columns_data[2].string
                charity_data['donor_province'] = columns_data[3].string
                charity_data['donation_amount'] = columns_data[4].string
                charity_data['donation_in_kind'] = columns_data[5].string
                charity_data['charity_link'] = charity_link
                charity_data['charity_name'] = charity_name
                charity_data['charity_type'] = charity_type
                charity_data['charity_sub_category'] = charity_sub_category
                charity_data['charity_description'] = charity_description
                charity_data['charity_registration_number'] = charity_registration_number
                charity_data['charity_website'] = charity_website
                charity_data['charity_country'] = charity_country
                charity_data['charity_province'] = charity_province
                charity_data['charity_city'] = charity_city
                charity_data['charity_employee_range'] = charity_employee_range

                charities_arr.append(charity_data)

    charities_df = pd.DataFrame(charities_arr)
    charities_df.to_csv(
        './data_extraction/donor_details/charity_donor_details_'+str(start)+'.csv', index=False)


if __name__ == '__main__':
    main()
