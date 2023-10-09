import re
from typing import List

import gensim
import nltk
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

    def preprocess(self):
        self.preprocessed_data = []

        for datum in self.data:
            # lower text
            datum = datum.lower()

            # replace special characters by space
            pattern = r"[^a-zàâçéèêëîïôûùüÿæœ]+"
            datum = re.sub(pattern, " ", datum)

            # trasform datum to word list
            datum = datum.split()

            # remove stop words
            stop_words = set(stopwords.words("french"))
            datum = [word for word in datum if not word in stop_words]

            # Lemmatize words
            datum = map(lambda word: WordNetLemmatizer().lemmatize(word), datum)

            self.preprocessed_data.append(list(datum))

    def topic_clustering(self):
        # Build bows of words
        dictionary = gensim.corpora.Dictionary(self.preprocessed_data)
        bow_corpus = [dictionary.doc2bow(doc) for doc in self.preprocessed_data]

        # Build topics
        lda_model = LdaModel(
            bow_corpus, num_topics=self.num_topics, id2word=dictionary, passes=1000
        )

        topics = []
        for idx, topic in lda_model.print_topics(-1):
            print("Topic: {} -> Words: {}".format(idx, topic))
            topics.append(topic)
