import sys
import os
import requests
import hashlib
from bs4 import BeautifulSoup
from bs4 import Comment
import time
import shutil
from selenium import webdriver

def generate_hash(string):
    return hashlib.sha256(string.encode('utf-8')).hexdigest()

def scrape_page(link):

    # Request the page
    page = requests.get(r'{}'.format(link))

    # HTML Parser
    soup = BeautifulSoup(page.content, 'html.parser')

    title_selector = 'h1.pg-headline'
    content_selector = 'div.l-container div.pg-rail-tall__wrapper div.l-container .zn-body__paragraph'

    # Title
    article_title = ''
    title_elements = soup.select(title_selector)
    if len(title_elements) > 0:
        article_title = title_elements[0].get_text()

    # Get the article body content
    article_content = ''

    # Extracted data
    for data in soup.select(content_selector):

        # Remove unwanted tags
        [x.extract() for x in data.find_all('script')]
        [x.extract() for x in data.find_all('style')]
        [x.extract() for x in data.find_all('meta')]
        [x.extract() for x in data.find_all('noscript')]
        [x.extract() for x in data.find_all('div', class_="image")]
        [x.extract() for x in data.find_all(text=lambda text: isinstance(text, Comment))]

        # Extract content text
        content = data.get_text()
        content = content.replace('\r', ' ').replace('\n', ' ')
        article_content += content + ' '

    article = {
        "id": generate_hash(link),
        "article_link": link,
        "article_title": article_title,
        "article_content": article_content
    }

    return article

def run(category="politics"):
    print("download text...")
    start_time = time.time()

    # Firefox Options
    options = webdriver.FirefoxOptions()
    options.headless = True
    browser = webdriver.Firefox(options=options)

    try:
        url_template = "https://www.cnn.com/search?size=10&q=*&page={0}&category="+category+"&type=article"
        link_selector = "h3.cnn-search__result-headline a"

        links = []
        for page in range(200):
            url = url_template.format(page + 1)
            if page > 0:
                url = url + "&from={0}".format((page + 1) * 10)
            print("Browsing news page:", url)

            # Browse
            browser.get(url)

            # Get Links
            news_links = browser.find_elements_by_xpath('//h3[contains(@class, "cnn-search__result-headline")]/a')
            for link in news_links:
                #print(link)
                #print("href", link.get_attribute("href"))
                links.append(link.get_attribute("href"))

            # Wait
            time.sleep(5)

        print("Found links:",len(links))

        # Download content
        news_dir = os.path.join(downloads, category)
        if not os.path.exists(news_dir):
            os.makedirs(news_dir)

        count = 0
        for url in links:
            try:
                print("News page:", url)
                article = scrape_page(url)
                file_path = os.path.join(news_dir, '{0}.txt'.format(count))
                with open(file_path, 'w') as f:
                    f.write(article["article_title"]+" "+article["article_content"])

                count += 1
                # Wait
                time.sleep(5)
            except Exception as e:
                print("Error in url:", url)
                print(e)
                continue

    except Exception as e:
        print("Error")
        print(e)
    # Quit the browser
    browser.quit()

    execution_time = (time.time() - start_time) / 60.0
    print("Download execution time (mins)", execution_time)

# Setup download folder
downloads = "dataset"
if os.path.exists(downloads):
    shutil.rmtree(downloads)
os.mkdir(downloads)

#run(category="politics")
run(category="health")
#run(category="entertainment")
