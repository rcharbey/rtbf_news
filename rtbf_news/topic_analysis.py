import re
from typing import List

import gensim
import nltk
import pandas as pd
from gensim.models import LdaModel
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


class TopicAnalyzer:
    def __init__(
        self, data: List[str], model_name: str = "camembert-base", num_topics: int = 20
    ):
        self.data = data
        self.model_name = model_name
        self.num_topics = num_topics
        nltk.download("wordnet")
        nltk.download("stopwords")
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
            self.dictionary = gensim.corpora.Dictionary(self.preprocessed_data)
            self.bow_corpus = [
                self.dictionary.doc2bow(doc) for doc in self.preprocessed_data
            ]

    def get_topics(self):
        # Build topics
        lda_model = LdaModel(
            self.bow_corpus, num_topics=self.num_topics, id2word=self.dictionary
        )

        # Create a dataframe of topics as columns
        self.topics = pd.DataFrame(
            [
                sorted(lda_model.show_topic(topic), key=lambda x: x[1], reverse=True)
                for topic in range(self.num_topics)
            ]
        ).T
        self.topics.columns = self.topics.iloc[0, :].apply(lambda x: x[0])
        self.topics.index = [f"Word n°{i+1}" for i in range(len(self.topics))]

        # drop duplicate topics
        self.topics = self.topics.loc[:, ~self.topics.columns.duplicated(keep="first")]

        # sort columns by clearest topics (higher score of the most important word)
        column_order = [
            x[0]
            for x in sorted(
                self.topics.loc["Word n°1", :].values, key=lambda x: x[1], reverse=True
            )
        ]
        self.topics = self.topics.loc[:, column_order]
