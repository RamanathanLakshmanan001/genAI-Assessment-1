# edgedriver path:
# C:\\Users\\RamanathanL\\Downloads\\edgedriver_win64\\msedgedriver.exe

# websites:
# https://www.siemensgamesa.com
# https://www.us.hsbc.com
# https://slack.com
# https://zoom.us
# https://www.spotify.com
# https://us.pg.com
# https://www.pepsico.com
# https://www.airbus.com
# https://www.ge.com
# https://corporate.walmart.com


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
import time


edge_driver_path = "C:\\Users\\RamanathanL\\Downloads\\edgedriver_win64\\msedgedriver.exe"
service = Service(edge_driver_path) 


driver = webdriver.Edge(service=service)

def scrape_page_text(driver):
    """Scrape all text from the current page."""
    return {"URL": driver.current_url, "Content": driver.find_element(By.TAG_NAME, "body").text}

def scrape_website_with_nav_links(start_url, output_file):
    """Scrape the main page and navbar links for a given website."""
    driver.get(start_url)
    time.sleep(2)


    data = [scrape_page_text(driver)]

    
    navbar_links = driver.find_elements(By.CSS_SELECTOR, "nav a")  # Modify selector if needed
    links_to_visit = [link.get_attribute("href") for link in navbar_links if link.get_attribute("href")]
    visited = set()

    for href in links_to_visit:
        if href not in visited:
            visited.add(href)
            try:
                driver.get(href)
                time.sleep(2) 
                data.append(scrape_page_text(driver))
            except Exception as e:
                print(f"Error visiting {href}: {e}")

    
    pd.DataFrame(data).to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")


websites = [
    {"url": "https://www.siemensgamesa.com", "output_file": "./scraped_data_folder/website_1.csv"},
    {"url": "https://www.us.hsbc.com", "output_file": "./scraped_data_folder/website_2.csv"},
    {"url": "https://slack.com", "output_file": "./scraped_data_folder/website_3.csv"},
    {"url": "https://zoom.us", "output_file": "./scraped_data_folder/website_4.csv"},
    {"url": "https://www.spotify.com", "output_file": "./scraped_data_folder/website_5.csv"},
    {"url": "https://us.pg.com", "output_file": "./scraped_data_folder/website_6.csv"},
    {"url": "https://www.pepsico.com", "output_file": "./scraped_data_folder/website_7.csv"},
    {"url": "https://www.airbus.com", "output_file": "./scraped_data_folder/website_8.csv"},
    {"url": "https://www.ge.com", "output_file": "./scraped_data_folder/website_9.csv"},
    {"url": "https://corporate.walmart.com", "output_file": "./scraped_data_folder/website_10.csv"}
]


for site in websites:
    print(f"Scraping {site['url']}...")
    scrape_website_with_nav_links(site["url"], site["output_file"])


driver.quit()

