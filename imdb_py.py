from imdb import Cinemagoer, IMDbError


def get_rating(title, movie_year, is_year_present):
    try:
        ia = Cinemagoer()

        movie_search = ia.search_movie(title)
        movie_id, title_from_imdbPy, year = get_movie_id(
            movie_search, movie_year, is_year_present)
        if movie_id == None:
            return movie_id, title_from_imdbPy, year

        movie = ia.get_movie(movie_id, info=['vote details'])
        # print('median', movie.get('median'))
        # print('arithmetic mean', movie.get('arithmetic mean'))
        # print('number of votes', movie.get('number of votes'))
        return movie.get('demographics').get('ttrt fltr imdb users').get('rating'), title_from_imdbPy, year
    except IMDbError as e:
        # print(e)
        return None, None, None


def get_movie_id(movie_search, movie_year, is_year_present):
    if is_year_present:
        for i in range(len(movie_search)):
            if str(movie_search[i]['year']) == str(movie_year) and movie_search[i]['kind'] == 'movie':
                return movie_search[i].movieID, movie_search[i]['title'], str(movie_year)
    else:
        for i in range(len(movie_search)):
            if movie_search[i]['kind'] == 'movie':
                try:
                    return movie_search[i].movieID, movie_search[i]['title'], str(movie_search[i]['year'])
                except:
                    return None, None, None
    return None, None, None


def use_imdbpy(extracted_name, is_year_present, year_from_folder):
    fetched_rating = None
    title = extracted_name
    rating, title, year = get_rating(
        title, str(year_from_folder), is_year_present)
    year = str(year_from_folder) if is_year_present else year
    rating = 'R-' + str(rating)
    return title, year, rating
