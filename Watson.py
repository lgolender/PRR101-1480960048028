import json

import watson_developer_cloud
from watson_developer_cloud import AlchemyDataNewsV1
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import WatsonException


class Watson:
    def __init__(self, config):
        self.config = config

        self.alchemy_language = watson_developer_cloud.AlchemyLanguageV1(api_key=self.config['api_key'])
        self.alchemy_data_news = AlchemyDataNewsV1(api_key=self.config['api_key'])
        self.tone_analyzer = ToneAnalyzerV3(version='2016-05-19 ', username=self.config['username'], password=self.config['password'])

    def get_analysis(self, url):
        combined_result = self.alchemy_language.combined(
                url=url,
                extract='entities,keywords',
                sentiment=1,
                max_items=1)

        return combined_result

    def get_data_ai(self, search_show):
        search_txt = '|text={},type=Movie|'.format(search_show)
        results = self.alchemy_data_news.get_news_documents(
            start='now-7d',
            end='now',
            return_fields=['enriched.url.title',
                           'enriched.url.url',
                           'enriched.url.author',
                           'enriched.url.publicationDate']
            ,
            query_fields={'q.enriched.url.enrichedTitle.entities.entity': search_txt}
        )

        return results

    def get_tones(self, search_str):
        result = json.dumps(self.tone_analyzer.tone(text=search_str), indent=2)
        print(result)

if __name__ == "__main__":
    config = {
        "api_key" : 'c3701f52114fce9b3de6e4e3ef7505119ac7336f',
        "password": "78zYzMEv87Xf",
        "username": "2747da81-393b-4c7c-8e6b-6568f1983e3b"
    }
    mentions = Watson(config)

    search_movie = 'Applied'
    result = mentions.get_data_ai(search_movie)
    print(result)
    #mentions.get_tones(search_movie)

