
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
df2 = df[(df['year'] >= 2018) | (df["year"] == -1)]
df2 = df2[(df2['ccf_rank'].str.contains('CCF-A|CCF-B', case=False))]
# ------------- Field         -------------
df2 = df2[(df2['title'].str.contains('reinforcement|multi-armed', case=False))]
# ------------- Direction     -------------
df2 = df2[(df2['title'].str.contains('adversarial', case=False))]
# ------------- Conference / Journal   -------------
df2 = df2[(df2['ccf_name'].str.contains('USENIX|AAAI', case=False))]

df2 = df2.sort_values(['ccf_rank', 'year', 'abbreviation'], ascending=[True, False, False])
df3 = df2[["ccf_rank", "ccf_name", "year", "title", "authors"]].copy() # Show
df3.authors = df3['authors'].str[:32]
print('Count: ', len(df3))
display(df3.head(100).style)
display(pd.DataFrame(df2.groupby(['ccf_rank', 'ccf_name']).size().sort_values(ascending=False)).style)
```

**Output**

---

#### CCF-A (7)
##### Usenix Security Symposium (2)
1. 2021, [Adversarial Policy Training against Deep Reinforcement Learning](https://www.usenix.org/conference/usenixsecurity21/presentation/wu-xian)
2. 2020, [EcoFuzz: Adaptive Energy-Saving Greybox Fuzzing as a Variant of the Adversarial Multi-Armed Bandit](https://www.usenix.org/conference/usenixsecurity20/presentation/yue)
##### AAAI Conference on Artificial Intelligence (5)
1. 2021, [Resilient Multi-Agent Reinforcement Learning with Adversarial Value Decomposition](https://ojs.aaai.org/index.php/AAAI/article/view/17348)
2. 2021, [Reinforcement Based Learning on Classification Task Yields Better Generalization and Adversarial Accuracy (Student Abstract)](https://ojs.aaai.org/index.php/AAAI/article/view/17893)
3. 2020, [Finding Needles in a Moving Haystack: Prioritizing Alerts with Adversarial Reinforcement Learning](https://ojs.aaai.org/index.php/AAAI/article/view/5442)
4. 2020, [Stealthy and Efficient Adversarial Attacks against Deep Reinforcement Learning](https://ojs.aaai.org/index.php/AAAI/article/view/6047)
5. 2018, [OptionGAN: Learning Joint Reward-Policy Options Using Generative Adversarial Inverse Reinforcement Learning](https://dblp.uni-trier.de/rec/conf/aaai/0002CBMPP18.html?view=bibtex)

### Rank Server

Query CCF-rank of paper in website quickly.

Preview website: [ccf-rank.eonew.cn](http://ccf-rank.eonew.cn)

### paper_to_ccf_rank_example.ipynb

Same as `Rank Server`.
