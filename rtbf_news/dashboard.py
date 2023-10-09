import streamlit as st


class RTBF_Dashboard:
    def describe_topic(self, topic):
        topic_title = topic[0][0]
        st.markdown(f"<h3>{topic_title}</h3>")

        for subtopic, value in topic:
            subtopic_col, value_col = st.columns(2)
            subtopic_col.write(subtopic)
            value_col.write(value)

    def describe_topics(self, topics):
        # Pretty-print a representation of each topic, based on their most important words

        st.write(topics.applymap(lambda x: f"{x[0]} - {str(round(x[1]*100, 3))}%"))

    def create_dashboard(self):
        st.set_page_config(page_title="Scoring Bancaire", layout="wide")
        st.header("RTBF news page analysis")
