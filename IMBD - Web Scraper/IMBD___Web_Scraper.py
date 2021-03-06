"""
Web Scraping Movie ratings from IMDB (Publicly known website)
#Language - Python
"""

from warnings import warn
from time import sleep
from time import time
from random import randint
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from IPython.core.display import clear_output

URL = 'https://www.imdb.com/search/title?title_type=feature,tv_movie&release_date=2017-01-01,2017-12-31&count=100'

RESPONSE = get(URL)
print(RESPONSE.text[:500])

HTML_SOUP = BeautifulSoup(RESPONSE.text, 'html.parser')
type(HTML_SOUP)

MOVIE_CONTAINERS = HTML_SOUP.find_all('div', class_='lister-item mode-advanced')
print(type(MOVIE_CONTAINERS))
print(len(MOVIE_CONTAINERS))

FIRST_MOVIE = MOVIE_CONTAINERS[0]

FIRST_IMDB = float(FIRST_MOVIE.strong.text)

FIRST_VOTES = FIRST_MOVIE.find('span', attrs={'name':'nv'})
FIRST_VOTES['data-value']
FIRST_VOTES = int(FIRST_VOTES['data-value'])

EIGHTH_MOVIE_MSCORE = MOVIE_CONTAINERS[7].find('div', class_='ratings-metascore')
type(EIGHTH_MOVIE_MSCORE)

# Lists to store the scraped data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

# Extract data from individual movie container
for container in MOVIE_CONTAINERS:

    # If the movie has Metascore, then extract:
    if container.find('div', class_='ratings-metascore') is not None:

        # The name
        name = container.h3.a.text
        names.append(name)

        # The year
        year = container.h3.find('span', class_='lister-item-year').text
        years.append(year)

        # The IMDB rating
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        # The Metascore
        m_score = container.find('span', class_='metascore').text
        metascores.append(int(m_score))

        # The number of votes
        vote = container.find('span', attrs={'name':'nv'})['data-value']
        votes.append(int(vote))

movies_df = pd.DataFrame({'movie': names,
                          'year': years,
                          'imdb': imdb_ratings,
                          'metascore': metascores,
                          'votes': votes})
print(movies_df.info())
print(movies_df)

headers = {"Accept-Language": "en-US, en;q=0.5"}

pages = [str(i) for i in range(1, 5)]
years_URL = [str(i) for i in range(2000, 2015)]

start_time = time()
requests = 0

for _ in range(5):
    # A request would go here
    requests += 1
    sleep(randint(1, 3))
    elapsed_time = time() - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))

for _ in range(5):
    # A request would go here
    requests += 1
    sleep(randint(1, 3))
    current_time = time()
    elapsed_time = current_time - start_time
    print('Request: {}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
    clear_output(wait=True)

warn("Warning Simulation")

# Redeclaring the lists to store data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

# Preparing the monitoring of the loop
start_time = time()
requests = 0

# For every year in the interval 2000-2015
for year_URL in years_URL:

    # For every page in the interval 1-4
    for page in pages:

        # Make a get request
        response = get('http://www.imdb.com/search/title?release_date=' + year_URL +
                       '&sort=num_votes,desc&page=' + page, headers=headers)

        # Pause the loop
        sleep(randint(8, 15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait=True)

        # Throw a warning for non-200 status codes
        if response.status_code != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status_code))

        # Break the loop if the number of requests is greater than expected
        if requests > 40:
            warn('Number of requests was greater than expected.')
            break

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response.text, 'html.parser')

        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_='lister-item mode-advanced')

        # For every movie of these 50
        for container in mv_containers:
            # If the movie has a Metascore, then:
            if container.find('div', class_='ratings-metascore') is not None:

                # Scrape the name
                name = container.h3.a.text
                names.append(name)

                # Scrape the year
                year = container.h3.find('span', class_='lister-item-year').text
                years.append(year)

                # Scrape the IMDB rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # Scrape the Metascore
                m_score = container.find('span', class_='metascore').text
                metascores.append(int(m_score))

                # Scrape the number of votes
                vote = container.find('span', attrs={'name':'nv'})['data-value']
                votes.append(int(vote))

movie_ratings = pd.DataFrame({'movie': names,
                              'year': years,
                              'imdb': imdb_ratings,
                              'metascore': metascores,
                              'votes': votes})
print(movie_ratings.info())
movie_ratings.head(10)

movie_ratings = movie_ratings[['movie', 'year', 'imdb', 'metascore', 'votes']]
movie_ratings.head()

movie_ratings['year'].unique()

movie_ratings.loc[:, 'year'] = movie_ratings['year'].str[-5:-1].astype(int)

movie_ratings['year'].head(3)

movie_ratings['n_imdb'] = movie_ratings['imdb'] * 10
movie_ratings.head(3)

#Creates csv of data scraped
movie_ratings.to_csv('movie_ratings.csv')
