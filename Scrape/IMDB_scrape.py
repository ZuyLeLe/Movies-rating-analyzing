import time

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

df = pd.DataFrame(
    columns=['title', 'num-of-voters', 'release-year', 'certificate', 'length', 'genres', 'director', 'writer', 'cast',
             'language', 'company', 'origin', 'budget', 'domestic-gross', 'worldwide-gross', 'rating', 'metascore', 'metauser', 'metacritic'])

try:
    chrome_drive = 'C:\chromedriver-win64\chromedriver.exe'
    option = webdriver.ChromeOptions()
    option.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(chrome_drive), options=option)
    imdb_link = "https://www.imdb.com/search/title/?title_type=feature&sort=alpha,asc&num_votes=50000,&count=250"
    driver.get(imdb_link)

    time.sleep(2)
    html_content = driver.execute_script("return document.body.innerHTML")
    soup = BeautifulSoup(html_content, "html.parser")
    try:
        n = 1
        while True:
            driver.find_element(By.CLASS_NAME, 'ipc-see-more__button').click()
            time.sleep(10)
            movies = soup.find('div', attrs={'class': 'sc-54d06b29-3 dnPppq'})
    except:
        html_content = driver.execute_script("return document.body.innerHTML")
        soup = BeautifulSoup(html_content, "html.parser")
        links = []
        vote_num = []
        for movie in soup.find_all('div', attrs={'class': 'ipc-metadata-list-summary-item__c'}):

            link = movie.find('a', attrs={'class': "ipc-title-link-wrapper"})['href']
            links.append(link)
            voters = movie.find('div', attrs={'class': "sc-53c98e73-0 kRnqtn"}).text.replace('Votes', '')
            vote_num.append(voters)
        print(len(links), len(vote_num))
        for link, voter in zip(links, vote_num):
            driver.get("https://www.imdb.com/" + link)
            num_of_voters = voter
            html_content = driver.execute_script("return document.body.innerHTML")
            soup = BeautifulSoup(html_content, "html.parser")
            time.sleep(2)
            title = soup.find('span', attrs={'class': "hero__primary-text"}).text
            try:
                meta_user = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[1]/a/span/span[1]").text
            except:
                meta_user = np.NaN

            try:
                meta_critic = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[2]/a/span/span[1]").text
            except:
                meta_critic = np.NaN

            try:
                metascore = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[2]/ul/li[3]/a/span/span[1]").text
            except:
                metascore = np.NaN



            try:
                certificate = driver.find_element(By.XPATH,
                                                  "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]/a").text
                length = driver.find_element(By.XPATH,
                                             "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[3]").text
            except:
                certificate = np.NaN
                length = driver.find_element(By.XPATH,
                                             "/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[2]").text

            rating = soup.find("span", attrs={'class': 'sc-bde20123-1 cMEQkK'}).text
            genres_ele = driver.find_elements(By.CLASS_NAME, "ipc-chip__text")
            genres = []
            for genre in genres_ele:
                genres.append(genre.text)

            director_data = soup.find_all('div', attrs={"class": "ipc-metadata-list-item__content-container"})[0].find_all("a")
            directors = []
            for director in director_data:
                directors.append(director.text)

            writer_data = soup.find_all('div', attrs={"class": "ipc-metadata-list-item__content-container"})[1].find_all("a")
            writers = []
            for writer in writer_data:
                writers.append(writer.text)

            cast_data = soup.find_all('a', attrs={"class": "sc-bfec09a1-1 gCQkeh"})
            try:
                casts = [cast_data[0].text, cast_data[1].text]
            except:
                try:
                    casts = [cast_data[0].text]
                except:
                    casts=np.NaN

            language_data = soup.find("li", attrs={"data-testid": "title-details-languages"}).find_all("li", attrs={
                'class': 'ipc-inline-list__item'})
            languages = []
            for language in language_data:
                languages.append(language.text)

            company_data = soup.find("li", attrs={"data-testid": "title-details-companies"}).find_all("li", attrs={
                'class': 'ipc-inline-list__item'})
            companies = []
            for company in company_data:
                companies.append(company.text)

            origin_data = soup.find("li", attrs={"data-testid": "title-details-origin"}).find_all("li", attrs={
                'class': 'ipc-inline-list__item'})
            origins = []
            for origin in origin_data:
                origins.append(origin.text)

            try:
                budget_data = soup.find("li", attrs={"data-testid": "title-boxoffice-budget"}).find_all("li", attrs={
                    'class': 'ipc-inline-list__item'})
                budgets = []
                for budget in budget_data:
                    budgets.append(budget.text)
            except:
                budgets = []

            try:
                gross_domestic_data = soup.find("li", attrs={"data-testid": "title-boxoffice-grossdomestic"}).find_all("li",
                                                                                                                       attrs={
                                                                                                                           'class': 'ipc-inline-list__item'})
                gross_domestics = []
                for gross_domestic in gross_domestic_data:
                    gross_domestics.append(gross_domestic.text)
            except:
                gross_domestics = []
            try:
                gross_worldwide_data = soup.find("li", attrs={"data-testid": "title-boxoffice-cumulativeworldwidegross"}).find_all("li",
                                                                                                                 attrs={
                                                                                                                     'class': 'ipc-inline-list__item'})
                gross_worldwides = []
                for gross_worldwide in gross_worldwide_data:
                    gross_worldwides.append(gross_worldwide.text)
            except:
                gross_worldwides = []

            release_date_data = soup.find("li", attrs={"data-testid": "title-details-releasedate"}).find_all("li", attrs={
                'class': 'ipc-inline-list__item'})
            release_dates = []
            for release_date in release_date_data:
                release_dates.append(release_date.text)
            time.sleep(1)
            movie_data = {
                "title": title,
                "num-of-voters": num_of_voters,
                "release-year": ', '.join(n for n in release_dates),
                "certificate": certificate,
                "length": length,
                "genres": ', '.join(n for n in genres),
                "director": ', '.join(n for n in directors),
                "writer": ', '.join(n for n in writers),
                "cast": ', '.join(n for n in casts),
                'language': ', '.join(n for n in languages),
                "company": ', '.join(n for n in companies),
                "origin": ', '.join(n for n in origins),
                "budget": ', '.join(n for n in budgets),
                "domestic-gross": ', '.join(n for n in gross_domestics),
                "worldwide-gross": ', '.join(n for n in gross_worldwides),
                "rating": rating,
                "metascore": metascore,
                "metauser": meta_user,
                "metacritic": meta_critic
            }
            print(movie_data)
            row_df = pd.DataFrame(movie_data, index=[0])
            df = pd.concat([df, row_df], ignore_index=True, axis=0)
finally:
    df.to_csv('raw_movies_data.csv')

