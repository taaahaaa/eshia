import pandas as pd
from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0

df_books = pd.read_excel("../data/eshia_books_final.xlsx")

df_books["Language"] = ""

for i in range(len(df_books)):
    df_books["Language"][i] = detect(df_books["Book content"][i])

df_books.to_excel("../data/eshia_detect_lang.xlsx")