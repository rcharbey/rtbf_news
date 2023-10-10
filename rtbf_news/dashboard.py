from typing import Dict, Tuple

import matplotlib.pyplot as plt
import streamlit as st


class RTBF_Dashboard:
    def describe_topics(self, topics):
        """
        Pretty-print a representation of each topic, based on their most important words
        """

        st.header("Topic description")
        # rename columns as most important topic words
        topics.columns = [word[0] for word in topics.iloc[0, :].values]

        # drop duplicate topics
        topics = topics.loc[:, ~topics.columns.duplicated(keep="first")]

        # sort columns by clearest topics (higher score of the most important word)
        column_order = sorted(
            topics.columns, key=lambda x: topics.iloc[0, :][x][1], reverse=True
        )
        topics = topics.loc[:, column_order]

        st.write(topics.applymap(lambda x: f"{x[0]} - {str(round(x[1]*100, 3))}%"))

    def display_topic_representativity(
        self, news_to_topic: Dict[int, Tuple[int, float]]
    ):
        st.header("number of recent news per topic")
        # get number of appearances of each topic
        topic_count = {topic: 0 for topic in news_to_topic}
        for topic in news_to_topic:
            topic_count[topic] += 1

        # sort by number of appearances
        nb_news_by_topic = sorted(
            [(topic, topic_count[topic]) for topic in topic_count],
            key=lambda topic_count: topic_count[1],
        )
        topic_ticks = [x[0] for x in nb_news_by_topic]
        nb_news = [x[1] for x in nb_news_by_topic]

        # plot and send to dashboard
        fig, ax = plt.subplots()
        ax.barh(range(len(topic_ticks)), nb_news)
        ax.set_yticks(range(len(topic_ticks)), labels=topic_ticks)
        ax.set_ylabel("number of news by topic")
        st.pyplot(fig)

    def create_dashboard(self):
        st.set_page_config(page_title="Scoring Bancaire", layout="wide")
        st.header("RTBF news page analysis")
