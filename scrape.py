from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager  # Use this to automatically manage Firefox driver

from bs4 import BeautifulSoup
import time
import numpy as np
import json

# Update this with the correct Firefox profile path
firefox_profile_path = "/home/mpho/snap/firefox/common/.mozilla/firefox/bj65b1k9.mphomoila"

# Getting links to articles
options = Options()
#options.set_preference("profile", firefox_profile_path)

article_links = []
article_dictionary_list = []

# Use Firefox instead of Edge
driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

# Define URLs
url_gen_1 = "https://www.isolezwe.co.za/ezokungcebeleka"

print(f"Navigating to: {url_gen_1}")
driver.get(url_gen_1)

# Wait for elements to load
driver.implicitly_wait(10)

# Loop through pages to collect article links
for i in range(50):
    print(f"THE CURRENT COUNT IS {i}")
    article_section = driver.find_elements(By.CLASS_NAME, 'sections')
    for elements in article_section:
        anchors = elements.find_elements(By.TAG_NAME, "a")
        for link in anchors:
            article_links.append(link.get_attribute("href"))

    # Find and click the 'View More' button to load more articles
    try:
        view_more = driver.find_element(By.ID, 'viewMoreButton')
        view_more.click()
    except:
        print("No more articles to load.")
        break
    time.sleep(10)

# Close the browser
driver.quit()

# Remove duplicate links
article_links = np.array(article_links)
article_links = np.unique(article_links)
print(f"THE NUMBER OF ARTICLES TO BE RETRIEVED IS {len(article_links)}")

# Parse articles and store in a dictionary
article_body = ""
print("WRITING DATA TO THE TEXT FILE")
for url in article_links:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    article_section = soup.find("div", class_="articleBodyMore")
    if article_section:
        results = article_section.find_all("p")
        article_info = {}
        article_body = ""
        for content in results:
            try:
                article_body += content.text
            except:
                print("An error occurred, skipping the article")

        try:
            article_info["class"] = 0  # Assuming class 0 for the article category
            article_info["content"] = article_body
            article_dictionary_list.append(article_info)
        except:
            print("Error occurred")

# Convert to JSON and save
print(article_dictionary_list)
json_data = json.dumps(article_dictionary_list, ensure_ascii=False, indent=4)
print(json_data)

with open('ezokungcebeleka.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)
