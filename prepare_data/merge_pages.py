import pandas as pd


df_books_pages = pd.read_excel("../data/eshia_books_page_trim_html.xlsx")
df = pd.DataFrame()

df = df_books_pages.sort_values(by=['Book id'], ignore_index=True)

for i in range(1, len(df)):
    if df["Book id"][i] == df["Book id"][i-1]:
        df["Page content"][i] = df["Page content"][i] + " " + df["Page content"][i-1]
        df.drop([i-1], inplace = True )

df.to_excel("../data/eshia_books_page_merge.xlsx")