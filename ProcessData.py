import json
import os

from watson_developer_cloud import WatsonException

from RawData import RawData
from Watson import Watson


class ProcessData:
    def __init__(self, articles: RawData, watson: Watson, gather_data=False, use_static_data=False):
        self.articles = articles
        self.watson = watson
        self.data = {}
        self.gather_data = gather_data
        self.use_static_data = use_static_data

    def process_all(self):
        if self.use_static_data:
            self.get_static_results()
        else:
            for movie, url_list in self.articles.data.items():
                for item in url_list:
                    try:
                        analysis = self.watson.get_analysis(item)
                        self.data[movie].append(analysis)
                    except KeyError:
                        try:
                            self.data[movie] = []
                            analysis = self.watson.get_analysis(item)
                            self.data[movie].append(analysis)
                        except WatsonException as e:
                            print("\n\nWatson Exception {}\n\n".format(e))
                            if self.gather_data:
                                self.save_static_results()
                            else:
                                self.get_static_results()
                            return
                    except WatsonException as e:
                        print("\n\nWatson Exception {}\n\n".format(e))
                        if self.gather_data:
                            self.save_static_results()
                        else:
                            self.get_static_results()
                        return

    def process(self, movie):
        for item in self.articles.data[movie]:
            try:
                self.data[movie].append(self.watson.get_analysis(item))
            except KeyError:
                self.data[movie] = []
                self.data[movie].append(self.watson.get_analysis(item))

    def get_data(self, movie):
        reputation = self.get_sentiments(movie)
        total_sentiments = {}
        for item in reputation:
            for sent_item in item['sentiments']:
                try:
                    total_sentiments[sent_item['type']]['count'] += 1
                except KeyError:
                    total_sentiments[sent_item['type']] = {'count': 1, 'score': 0}

                try:
                    total_sentiments[sent_item['type']]['score'] += float(sent_item['score'])
                except KeyError:
                    pass
        return total_sentiments

    def get_sentiments(self, movie):
        result = []
        for item in self.data[movie]:
            info = {'sentiments': [], 'keywords': []}
            try:
                for senti_item in item["entities"]:
                    info['sentiments'].append(senti_item["sentiment"])
                info['keywords'] = item["keywords"]
                result.append(info)
            except KeyError:
                pass
        return result

    def get_static_results(self):
        full_file_name = os.path.join('D:\\', 'Projects', 'PRR101', 'ML docs', 'full_result_Jackie.json')
        with open(full_file_name) as results_file:
            info = json.load(results_file)
        self.data = info

    def save_static_results(self):
        full_file_name = os.path.join('D:\\', 'Projects', 'PRR101', 'ML docs', 'full_results.json')
        with open(full_file_name, mode='w') as results_file:
            results_file.write('{\n')
            for movie, watson_data in self.data.items():
                print_comma = False
                results_file.write('\t\"{}\": [\n'.format(movie))
                for item in watson_data:
                    if not print_comma:
                        print_comma = True
                    else:
                        results_file.write(',\n')
                    json.dump(item, results_file)
                results_file.write('],\n')
            results_file.write('}\n')

    def get_sentiment(self, sentiments):
        pass