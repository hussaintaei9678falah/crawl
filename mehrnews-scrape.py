import requests
from bs4 import BeautifulSoup
from newspaper import Article
from tqdm import tqdm
import pandas as pd
import csv


def repetitive(links, urls):
    for link in links:
        if link.a['href'] in urls:
            return True
    return False

def scrap_year(year: int):
    page = 90
    push_data = []
    url_site = []

    while True:
        page += 1

        page_address = f"https://www.mehrnews.com/page/archive.xhtml?mn=3&wide=0&dy=1&ms=0&pi={page}&yr={year}"

        html = requests.get(page_address).text  

        soup = BeautifulSoup(html, features='lxml')

        links = soup.find_all('h4')

        if repetitive(links, url_site):
            break

        for link in tqdm(links):
            page_url = 'https://mehrnews.com/' + link.a['href']
            url_site.append(link.a['href'])
            try:
                essay = Article(page_url)
                essay.download()
                essay.parse()
                push_data.append({'url': page_url, 'text': essay.text, 'title': essay.title})
            except:
                print(f"Error to read page: {page_url}")

    save = pd.DataFrame(push_data)
    save.to_csv(f'mehrakhbar-{year}.csv')


if __name__ == '__main__':
    scrap_year(1400)

