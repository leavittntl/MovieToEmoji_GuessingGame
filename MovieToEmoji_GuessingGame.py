# Import resources
import streamlit as st
import random
import time

# Sample Movie to Emoji dictionary
MOVIE_EMOJI_DATA = {
    "Alice": [("The Shawshank Redemption", "🔒🏃‍♂️💼"),
              ("Inception", "👨‍🎓🌃🧩"),
              ("The Dark Knight", "🦇🃏🌆")],
    "Bob": [("The Godfather", "🤵🍊👑"),
            ("Pulp Fiction", "💉💼🍔"),
            ("Goodfellas", "🔫🍝💰")],
    "Charlie": [("Fight Club", "👨🥊🤖"),
                ("The Matrix", "🕶️👾💊"),
                ("Blade Runner", "🤖🏃‍♂️🌆")],
    # Add more individuals, movies, and emojis
}

def flatten_data(data):
    result = []
    for person, movies in data.items():
        for movie in movies:
            result.append((person, movie))
    return result

def get_random_movie(remaining_data):
    return random.choice(remaining_data)

st.title("🎬 Guess the Favorite Movie Game")
st.markdown("Try to guess the individual's favorite movie based on the emojis displayed. You have 3 attempts per movie title.")

player_name = st.text_input("Enter your name:")

if not player_name:
    st.warning("Please enter your name to start the game.")
    st.stop()

if 'remaining_movies' not in st.session_state:
    st.session_state.remaining_movies = flatten_data(MOVIE_EMOJI_DATA)

if 'score' not in st.session_state:
    st.session_state.score = 0

if 'movie' not in st.session_state:
    st.session_state.movie = get_random_movie(st.session_state.remaining_movies)

if 'attempts' not in st.session_state:
    st.session_state.attempts = 0

total_movies = len(flatten_data(MOVIE_EMOJI_DATA))
remaining_attempts = 3 - st.session_state.attempts

#st.write(f"Score: {st.session_state.score}")
#st.write(f"Movies left: {len(st.session_state.remaining_movies)}")
#st.write(f"Remaining attempts for this title: {remaining_attempts}")
st.write(f"Guess {st.session_state.movie[0]}'s favorite movie based on the emojis: {st.session_state.movie[1][1]}")
guess = st.text_input("Guess the Movie:")

if not guess:
    st.warning("Please enter your guess to continue.")
    st.stop()

if st.button("Submit"):
    st.session_state.attempts += 1
    remaining_attempts -= 1

    if guess.lower() == st.session_state.movie[1][0].lower():
        st.success(f"Congratulations {player_name}! You correctly guessed {st.session_state.movie[0]}'s favorite movie '{st.session_state.movie[1][0]}'.")
        st.session_state.score += 1
        st.session_state.remaining_movies.remove(st.session_state.movie)

        if len(st.session_state.remaining_movies) == 0:
            st.write("🎉 Game Over 🎉")
            st.write(f"{player_name}, your final score is: {st.session_state.score}/{total_movies}! Good Job! 🎉")
            st.balloons()
            st.stop()
        else:
            time.sleep(2.0)
            st.session_state.attempts = 0
            st.session_state.movie = get_random_movie(st.session_state.remaining_movies)
            st.experimental_rerun()
    else:
        if st.session_state.attempts < 3:
            st.error(f"Wrong guess, {player_name}. You have {remaining_attempts} remaining attempts.")
        else:
            st.warning(f"You've used all your attempts. The correct answer was {st.session_state.movie[0]}'s favorite movie '{st.session_state.movie[1][0]}'.")
            time.sleep(2.0)
            st.session_state.remaining_movies.remove(st.session_state.movie)

            if len(st.session_state.remaining_movies) > 0:
                st.session_state.attempts = 0
                st.session_state.movie = get_random_movie(st.session_state.remaining_movies)
                st.experimental_rerun()
            else:
                st.write("🎉 Game Over 🎉")
                st.write(f"{player_name}, your final score is: {st.session_state.score}/{total_movies}! Good Job! 🎉")
                st.balloons()
                st.stop()