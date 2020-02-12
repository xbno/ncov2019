# Scraper for Ncov Cases

Scrapes [news.163.com]('https://news.163.com/special/epidemic/?spssid=7283291fcdba1d8c2d13ee3da2cfb760&spsw=7&spss=other#map_block')

1. Clone repo and cd into it: `git clone  && cd ncov`
2. To run, create conda env: `conda env create -f ncov_environment.yml -p xyz` (this is a bloated env)
3. Activate the environment: `conda activate xyz`
4. Run: `python ncov_scrape.py`
5. Find csv in current dir