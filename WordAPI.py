# __author__: Mai feng
# __file_name__: WordAPI.py
# __time__: 2019:06:27:20:31

from config import WordConfig
import requests
from pyquery import PyQuery as pq
class WordAPI:
    def __init__(self, config):
        self.config = config
        self.s = requests.session()


    def getCiBa(self):
        '''从金山词霸中获取每日一句
        '''
        res = self.s.get(self.config.cibaUrl)
        if res.status_code == 200:
            datas = res.json()
            content = datas.get('content')
            note = datas.get('note')
            return f"{content}\n{note}"
        else:
            raise 'getCiBa->error->200'

    def getMotto(self):
        '''获取格言
        '''
        res = self.s.get(url=self.config.dictumUrl)
        if res.status_code == 200:
            doc = pq(res.text)
            today_dictum = doc('.fp-one-cita').eq(0).text()
            return today_dictum
        else:
            raise 'getMotto->error->200'


if __name__ == "__main__":
    wapi = WordAPI(WordConfig)
    msg = wapi.getCiBa()
    msg = wapi.getMotto()
    print(msg)