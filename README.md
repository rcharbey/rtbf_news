# rtbf_news

## Overview
This pipe 
- reads the most recent news from the RTBF continuous news page
- detect the various topics (from [LDA algorithm]([url](https://radimrehurek.com/gensim/models/ldamodel.html))) among them
- build a dashboard presenting the topics and the number of news per topic from this news selection.

  
In the rtbf_news/main.py file, you can change [NB_NEWS] (the number of news to scrap) and [NB_TOPICS] (the number of topics the LDA will detect) 

## Installation
requirements are to be found in `requirements.txt`.
you can install them all at once by running `pip install -r requirements.txt`

## How to run
In a terminal, run:
`streamlit run rtbf_news/main.py`
