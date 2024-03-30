from bs4 import BeautifulSoup
import requests
import re

search_term = str(input("What product do you want to search for? (e.g., series-model -> rtx-2060-super): "))


def scrape_page(url):
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    product_containers = soup.find_all('div', class_='product-title-rating')
    found_at_least_one_result = False
    for container in product_containers:
        title_element = container.find('h3', class_='product-title')
        if title_element:
            title = title_element.string.strip()

            if re.search(search_term, title, re.IGNORECASE):
                found_at_least_one_result = True
                print("Title", title)

                price_element = soup.find('span', class_='price')
                if price_element:
                    price = price_element.text.strip()
                    print("Price:", price)
                    
                
                link_element = title_element.find('a')
                if link_element and 'href' in link_element.attrs:
                    link = link_element['href']
                    print("Link:", link)
                
    if not found_at_least_one_result:
        print(f"{search_term} not found on url {url}")

    return get_next_page_url(soup)


    
def get_next_page_url(soup):
    next_button = soup.find('a', string='Next')
    if next_button:
        return next_button['href']
    else:
        return None
    
url = "https://www.primeabgb.com/buy-online-price-india/graphic-cards-gpu/?filters=_stock_status[instock]|graphic-card-series"

while url:
    # print("Scraping page:", url)
    url = scrape_page(url)
