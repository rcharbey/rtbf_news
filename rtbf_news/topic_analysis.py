import re
from typing import List

import gensim
import nltk
import pandas as pd
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("wordnet")
nltk.download("stopwords")


class TopicAnalyzer:
    def __init__(
        self, data: List[str], model_name: str = "camembert-base", num_topics: int = 20
    ):
        self.data = data
        self.model_name = model_name
        self.num_topics = num_topics
        self.preprocess()

    def preprocess(self):
        self.preprocessed_data = []

        lemmatizer = WordNetLemmatizer()

        for datum in self.data:
            # lower text
            datum = datum.lower()

            # replace special characters by space
            pattern = r"[^a-zàâçéèêëîïôûùüÿæœ]+"
            datum = re.sub(pattern, " ", datum)

            # trasform datum to word list
            datum = datum.split()

            # remove small words
            datum = [word for word in datum if len(word) > 3]

            # remove stop words
            stop_words = set(stopwords.words("french")).union(
                set(["vidéo", "tipik", "audio"])
            )
            datum = [word for word in datum if not word in stop_words]

            # Lemmatize words
            datum = map(lambda word: lemmatizer.lemmatize(word), datum)

            self.preprocessed_data.append(list(datum))

        # Compute dictionary and bow corpus of the news corpus
        self.dictionary = gensim.corpora.Dictionary(self.preprocessed_data)
        self.bow_corpus = [
            self.dictionary.doc2bow(doc) for doc in self.preprocessed_data
        ]

    def get_topics(self):
        # Build topics
        lda_model = LdaModel(
            self.bow_corpus,
            num_topics=self.num_topics,
            id2word=self.dictionary,
            passes=10,
        )

        # Create a dataframe of topics as columns
        self.topics = pd.DataFrame(
            [
                sorted(lda_model.show_topic(topic), key=lambda x: x[1], reverse=True)
                for topic in range(self.num_topics)
            ]
        ).T
        self.topics.index = [f"Word n°{i+1}" for i in range(len(self.topics))]

        # topics are names depending on their most important word
        self.topic_names = self.topics.iloc[0, :].apply(lambda x: x[0])

        # Get topic by news
        self.news_to_topic = []
        for news in self.bow_corpus:
            topic_name = (
                "" if not lda_model[news] else self.topic_names[lda_model[news][0][0]]
            )
            self.news_to_topic.append(topic_name)
