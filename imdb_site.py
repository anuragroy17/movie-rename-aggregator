import requests
from bs4 import BeautifulSoup


def imdb_url(path):
    url = 'http://www.imdb.com/find?q=' + '+'.join(path.split(' '))
    return url


def parse_search_results(page_contents):
    doc = BeautifulSoup(page_contents, 'html.parser')
    parent = doc.find_all('td', {'class': 'result_text'})
    base_url = 'https://www.imdb.com'
    for item in parent:
        a = item.find('a')
        movie_title = item.text
        movie_url = base_url + item.find('a')['href']
        break
    return movie_url, movie_title


def parse_rating(page_contents):
    doc = BeautifulSoup(page_contents, 'html.parser')
    # This is to fetch the rating of the movie
    rating = doc.find('span', {'class': 'sc-7ab21ed2-1'})
    if rating == None:
        rating = 'NA'
    else:
        rating = rating.text


def fetch_movie(name):
    url = imdb_url(name)
    response = requests.get(url)
    url, title_year = parse_search_results(response.text)
    response = requests.get(url)
    rating = parse_rating(response.text)
    return title_year, rating


def use_imdb_scrapping(extracted_name):
    title_year, rating = fetch_movie(extracted_name)
    rating = 'R-' + str(rating)
    return title_year, '', rating
