import pandas as pd
import requests


class MovieAPI:
    def __init__(self, api_key, num_results):
        """
        Initialize MovieAPI instance.

        Parameters:
        - api_key (str): The API key for accessing the MovieDB API.
        - num_results (int): Desired number of results.
        """

        # Set up API url and header
        self.url = (
            "https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page=1"
            "&sort_by=popularity.desc&primary_release_year=")

        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + api_key
        }

        # Set desired number of results
        self.num_results = num_results

        # Year and response placeholders
        self.year = None
        self.response = None

    def get_movies(self, year, title_mode, sort_by):
        """
        Get a DataFrame of movies based on the specified parameters.

        Parameters:
        - year (int): The release year of the movies.
        - title_mode (str): Title mode ('Simplified' or 'Full').
        - sort_by (str): Sort by 'Votes' or 'Title'.

        Returns:
        - pd.DataFrame or None: DataFrame of movies or None if an error occurs.
        """

        # Check previous saved year to minimize API calls if year is unchanged
        if year != self.year:
            # Get response using year parameter, if year is unchanged, then use previously saved response
            self.response = requests.get(self.url + str(year), headers=self.headers)

        # Reset year
        self.year = year

        # Check status code
        if self.response.status_code != 200:
            return None

        data = self.response.json()["results"]

        # Validate length of data
        if len(data) == 0:
            return None

        movies_data = []
        # Iterate number of times specified, or through all data if length is less than number specified
        for i in range(min(len(data), self.num_results)):
            movie_dict = {}
            title = data[i]["title"]
            if title_mode == "Simplified":
                # Move "The" and "A" to end of title if "Simplified" mode
                if title.startswith("The "):
                    title = title[4:] + ", The"
                elif title.startswith("A "):
                    title = title[2:] + ", A"

            movie_dict["Title"] = title
            movie_dict["Date"] = data[i]["release_date"]
            movie_dict["Votes"] = data[i]["vote_count"]

            movies_data.append(movie_dict)

        # Convert array of dictionaries to dataframe
        movies_df = pd.DataFrame(movies_data)

        # Sort data based on "Votes" or "Title", and only sort ascending if by Title
        movies_df = movies_df.sort_values(by=sort_by, ascending=(sort_by == "Title"))
        movies_df = movies_df.reset_index(drop=True)

        return movies_df
