import pandas as pd
import requests


class MovieAPI:
    def __init__(self, api_key):
        self.url = (
            "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1"
            "&sort_by=popularity.desc&primary_release_year=")

        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + api_key
        }

    def get_movies(self, year, title_mode, sort_by, num):
        response = requests.get(self.url + str(year), headers=self.headers)
        if response.status_code != 200:
            return None

        data = response.json()["results"]
        if len(data) == 0:
            return None

        movies_data = []
        for i in range(min(len(data), num)):
            movie_dict = {}
            title = data[i]["title"]
            if title_mode == 'Simplified':
                if title.startswith("The "):
                    title = title[4:] + ", The"
                elif title.startswith("A "):
                    title = title[2:] + ", A"

            movie_dict["Title"] = title
            movie_dict["Date"] = data[i]["release_date"]
            movie_dict["Votes"] = data[i]["vote_count"]

            movies_data.append(movie_dict)

        movies_df = pd.DataFrame(movies_data)

        movies_df = movies_df.sort_values(by=sort_by, ascending=False)
        movies_df = movies_df.reset_index(drop=True)

        return movies_df
