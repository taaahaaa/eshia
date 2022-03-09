import pandas as pd

df_books = pd.read_excel("../data/eshia_books.xlsx")
df_books_pages = pd.read_excel("../data/eshia_books_page_merge.xlsx")

df_books["Book content"] = ""

for i in range(len(df_books)):
    for j in range(len(df_books_pages)):
        if df_books["Book id"][i] == df_books_pages["Book id"][j]:
            df_books["Book content"][i] = df_books_pages["Page content"][j]
            break


df_books.to_excel("../data/eshia_books_merged.xlsx")