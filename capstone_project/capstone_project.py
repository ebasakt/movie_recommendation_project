import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import ast


pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 50)

df = pd.read_csv("movies_metadata.csv", low_memory=False)

df['overview'] = df['overview'].fillna('')
df['genres'] = df['genres'].fillna('')
df['budget'] = df['budget'].fillna(0)
df['revenue'] = df['revenue'].fillna(0)
df['runtime'] = df['runtime'].fillna(0)
df['production_countries'] = df['production_countries'].fillna('')
df['original_title'] = df['original_title'].fillna('')


def parse_genres(genres_str):
    try:
        genres_list = ast.literal_eval(genres_str)
        return ' '.join([g['name'] for g in genres_list])
    except:
        return ''

df['genres'] = df['genres'].apply(parse_genres)

df['features'] = df['overview'] + ' ' + df['genres']

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['features'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)


def recommend_movie(title, top_n=5):
    df_lower = df['title'].str.lower()
    if title.lower() not in df_lower.values:
        return f"Movie '{title}' not found in dataset."

    idx = df_lower[df_lower == title.lower()].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n + 1]
    movie_indices = [i[0] for i in sim_scores]


    columns_to_display = ['title', 'genres', 'release_date', 'revenue', 'vote_average', ]
    return df.iloc[movie_indices][columns_to_display]



if __name__ == "__main__":
    movie_name = input("Enter a movie title: ")
    top_n = input("How many recommendations do you want? ")
    try:
        top_n = int(top_n)
    except ValueError:
        print("Invalid number. Defaulting to 5.")
        top_n = 5

    recommendations = recommend_movie(movie_name, top_n=top_n)
    print(recommendations)