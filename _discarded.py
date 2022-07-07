import urllib.request
import unicodedata
import re


def imdb_url(path):
    url = 'http://www.imdb.com/find?q=' + '+'.join(path.split(' '))
    url = unicodedata.normalize('NFKD', url).encode(
        'ascii', errors='ignore').decode('ascii')
    return url


def crawl_imdb(url):
    request = urllib.request.Request(
        url, None, {'Accept-Language': 'en-US,en;q=0.8,de;q=0.6'})
    response = urllib.request.urlopen(request)
    content = response.read()
    text = content.decode('utf-8-sig', errors='ignore')
    return text


def fetch_movie(name):
    url = imdb_url(name)
    html = crawl_imdb(url)
    title = parse_title(html)
    year = parse_year(html)
    return title, year


def parse_title(html):
    matches = re.search('"result_text">[^>]+>(?P<title>[^<]*)', html)
    if not matches:
        return None
    title = matches.group('title')
    title = title.strip()
    if len(title) > 3 and re.match('[0-9A-Za-z-,!?]+', title):
        return title
    return None


def parse_year(html):
    matches = re.search('"result_text">[^>]+>[^>]+> (?P<text>[^<]+) <', html)
    if not matches:
        return None
    text = matches.group('text')
    matches = re.search('(?P<year>[12][0-9]{3})', text)
    if matches:
        return matches.group('year')
    return None


def get_movie_details(extracted_name, is_year_present, year_from_folder):
    fetched_rating = None
    if is_year_present:
        # print('fetching from imdbpy...')
        title = extracted_name
        year = str(year_from_folder)
        # fetched_rating, title = get_rating(title, year)

    if fetched_rating == None:
        # print('fetching from imdb url...')
        title, year = fetch_movie(extracted_name)
        # fetched_rating, title_from_imdbpy = get_rating(title, year)

    rating = 'R-' + str(fetched_rating)
    return title, year, rating
