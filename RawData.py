import csv
import requests
from bs4 import BeautifulSoup
import os


class RawData:
    def __init__(self):
        self.data = {}

    def get_data_1(self, search_show):
        url = 'http://www.metacritic.com/movie/{}'.format(search_show)
        headers = {
            'Host': 'www.metacritic.com',
            'Cache - Control': 'max - age = 0',
'Connection' : 'keep-alive',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'DNT': '1',
'Referer': 'http://www.metacritic.com/search/all/jackie/results',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'en-US,en;q=0.8,he;q=0.6,ru;q=0.4,uk;q=0.2'
        }
        cookies = { 'Cookie': 'ctk=NTg0MDNiMDY0NTdhM2E1YWJiYTVlZjVhNTYzNg%3D%3D; optimizelyEndUserId=oeu1480604423225r0.15406607862763222; CBS_INTERNAL=0; LDCLGFbrowser=20b71627-9720-4854-86a3-e71ce994cf7b; AMCVS_10D31225525FF5790A490D4D%40AdobeOrg=1; hycw4hSBtd=true; JYaH5Y2vxL=true; gebDnVVAmj=1113561511153; XCLGFbrowser=FYsE6lhAOw3YZKg3Pas; s_vnum=1483196431891%26vn%3D2; s_sq=%5B%5BB%5D%5D; tmpid=1480611597547113; optimizelySegments=%7B%222318000158%22%3A%22gc%22%2C%222326220374%22%3A%22false%22%2C%222339730210%22%3A%22none%22%2C%222366140006%22%3A%22referral%22%7D; optimizelyBuckets=%7B%7D; __utmt=1; __utma=15671338.200706095.1480604425.1480604425.1480610761.2; __utmb=15671338.3.10.1480610761; __utmc=15671338; __utmz=15671338.1480604428.1.1.utmcsr=imdb.com|utmccn=(referral)|utmcmd=referral|utmcct=/title/tt1619029/; utag_main=v_id:0158bae69c9a00161a9d16aa0ca905066001a05e009d8$_sn:2$_ss:0$_st:1480613401353$_pn:3%3Bexp-session$ses_id:1480610764117%3Bexp-session; s_invisit=true; s_getNewRepeat=1480611606634-Repeat; s_lv_undefined=1480611606634; s_lv_undefined_s=Less%20than%201%20day; prevPageType=product_overview; AMCV_10D31225525FF5790A490D4D%40AdobeOrg=-227196251%7CMCMID%7C69885763409951256247375154331258557981%7CMCAAMLH-1481216407%7C7%7CMCAAMB-1481216407%7CNRX38WO0n5BH8Th-nqAG_A%7CMCOPTOUT-1480618807s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C1484479201; QSI_HistorySession=http%3A%2F%2Fwww.metacritic.com%2F~1480604431794%7Chttp%3A%2F%2Fwww.metacritic.com%2Ftv~1480604442838%7Chttp%3A%2F%2Fwww.metacritic.com%2Fsearch%2Fall%2Fjackie%2Fresults~1480604515331%7Chttp%3A%2F%2Fwww.metacritic.com%2Fmovie%2Fjackie~1480611595950%7Chttp%3A%2F%2Fwww.metacritic.com%2Fmovie%2Fallied~1480611607133; sq4YFvJMK2=1; s_cc=true; aam_uuid=69659117608908523527353891351054930789'
}

        r = requests.get(url, headers=headers, cookies=cookies)

        return r

    def get_data_2(self):
        url = 'http://www.imdb.com/title/tt1619029/externalreviews?ref_=tt_ov_rt'

        r = requests.get(url)

        return r

    def get_data_3(self):
        url = 'http://www.imdb.com/title/tt1619029/externalreviews?ref_=tt_ov_rt'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        return soup.prettify()

    def  get_data_file(self):
        full_file_name = os.path.join('D:\\', 'Projects', 'PRR101', 'ML docs', 'imdb2.csv')
        with open(full_file_name) as csvfile:
            data_reader = csv.DictReader(csvfile)
            next(data_reader)

            for row in data_reader:
                if row['Movie'] is not None and row['Movie'] != '':
                    try:
                        self.data[row['Movie']].append(row['url'])
                    except KeyError:
                        self.data[row['Movie']] = []
                        self.data[row['Movie']].append(row['url'])


if __name__ == "__main__":
    rd = RawData()
    rd.get_data_file()
