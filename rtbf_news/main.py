from dashboard import RTBF_Dashboard
from scraper import RTBF_Scraper
from topic_analysis import TopicAnalyzer

url = "https://www.rtbf.be/en-continu"

scraper = RTBF_Scraper(url=url, nb_news=2000)
data = scraper.scrap()

analyzer = TopicAnalyzer(data, num_topics=25)
analyzer.preprocess()
analyzer.get_topics()
topics = analyzer.topics
news_to_topic = analyzer.news_to_topic

dash = RTBF_Dashboard()
dash.create_dashboard()
dash.describe_topics(topics)
dash.display_topic_representativity(news_to_topic)
