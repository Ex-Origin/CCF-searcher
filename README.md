
# CCF Searcher

A paper tool that searches papers in CCF.

## Features

* Make your search results more precise

## How to Work

Crawling data from [dblp.com](https://dblp.uni-trier.de/), then processing these data with `pandas`.

## Usage

### dblp_crawler.py

It will take a long time to crawl the data.

```shell
python3 dblp_crawler.py
```

### ccf_searcher_example.ipynb

```shell
jupyter lab ccf_searcher_example.ipynb
```

Using more accurate searcher.

```python
# ------------- Paper Quality -------------
df2 = df[(df['year'] >= 2019) | (df["year"] == -1)]
df2 = df2[(df2['ccf-rank'].str.contains('CCF-A|CCF-B', case=False))]
# ------------- Field         -------------
df2 = df2[(df2['title'].str.contains('reinforcement|multi-armed', case=False))]
# ------------- Direction     -------------
df2 = df2[(df2['title'].str.contains('adversarial', case=False))]
# ------------- Conference / Journal   -------------
df2 = df2[(df2['ccf-name'].str.contains('USENIX|AAAI', case=False))]

df2 = df2.sort_values(['ccf-rank', 'year', 'abbreviation'], ascending=[True, False, False])
df3 = df2[["ccf-rank", "ccf-name", "year", "title", "authors"]].copy() # Show
df3.authors = df3['authors'].str[:32]
print('Count: ', len(df3))
display(df3.head(20).style)
display(pd.DataFrame(df2.groupby(['ccf-rank', 'ccf-name']).size().sort_values(ascending=False)).style)
```
