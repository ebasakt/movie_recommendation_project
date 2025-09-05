import pandas as pd

df = pd.read_csv("movies_metadata.csv", low_memory=False)


print(df.columns)