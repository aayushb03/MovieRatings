from movieAPI import MovieAPI
import streamlit as st

# Initialize constants
API_KEY = ("eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2ZjhjOTJjNjgyNzlmMjk1NGJmMmZlYzBkNDBmZWU3MCIsInN1YiI6IjY1OWRmNDgxNmQ5N2U2MD"
           "BmMDc4ZTQ2ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.J02giUhuBK_NjdwNyS2iOj_7BNhFsWpL2dd4YZ44ExY")
NUM_RESULTS = 10

# Initialize MovieAPI object with specified constants
md = MovieAPI(API_KEY, NUM_RESULTS)

# Header
st.header("Movie Ratings App")
st.write("Retrieve the top 10 movies from any given year:")

# Buttons/Selectors
wid1, wid2, wid3 = st.columns([1, 1, 1])
with (wid1):
    year = st.number_input(
        label="Year:",
        min_value=1000,
        max_value=2024,
        value=2024,
        step=1
    )
with (wid2):
    title_option = st.radio(
        label="Title:",
        options=["Full", "Simplified"],
        horizontal=True
    )
with (wid3):
    sort_option = st.radio(
        label="Sort By:",
        options=["Votes", "Title"],
        horizontal=True
    )

# Retrieve movie data
movies_data = md.get_movies(year, title_option, sort_option)

# Show results or error message
if movies_data is not None:
    st.write("*Table Preview:*")
    st.table(movies_data)

    st.download_button(
        label="Download CSV",
        data=movies_data.to_csv(index=False).encode("utf-8"),
        file_name="movie_ratings_" + str(year) + ".csv",
        mime="text/csv"
    )
else:
    st.write("No Results Exist!")
