import re
import pandas as pd

df = pd.read_excel("./data/eshia_book_pages.xlsx")
CLEANR = re.compile("<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});")
def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, "", raw_html)
    return cleantext

for i in range(len(df["Page content"])):
    df["Page content"][i] = cleanhtml(df["Page content"][i])

df.to_excel("./data/eshia_books_page_trim_html.xlsx")