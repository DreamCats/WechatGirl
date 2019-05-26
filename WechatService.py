# __author__: Mai feng
# __file_name__: WechatService.py
# __time__: 2019:05:26:16:12
import requests
import itchat
from yaml import load
import time
from datetime import datetime
from CityInfo import city_dict

'''基本配置'''
class BaseConfig:

    # 女友信息
    girl_infos = {
        'girl_name':'xxx',
        'girl_city':'成都',
    }
    pass

class WeatherConfig:
    girl_city_code = city_dict[BaseConfig.girl_infos['girl_city']]
    weather_url = f'http://t.weather.sojson.com/api/weather/city/{girl_city_code}'
    pass

class PowerWordConfig:
    ciba_url = 'http://open.iciba.com/dsapi'
    dictum_url = 'http://wufazhuce.com/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    pass

class Weather:
    '''天气业务逻辑类
    '''
    def __init__(self, config):
        '''初始化
        '''
        self.config = config
        self.s = requests.session()

    
    def get_weather_info(self):
        '''获取女友所在地的天气信息
        :reuturn: msg
        '''
        try:
            res = self.s.get(url=self.config.weather_url)
            if res.status_code == 200:
                data = res.json()['data']
                # 今日天气
                today_weather = data.get('forecast')[1]
                # 今日日期
                today_time = datetime.now().strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年', m='月', d='日')
                # 今日天气注意事项
                notice = today_weather.get('notice')
                 # 温度
                high = today_weather.get('high')
                high_c = high[high.find(' ') + 1:]
                low = today_weather.get('low')
                low_c = low[low.find(' ') + 1:]
                temperature = f"温度 : {low_c}/{high_c}"

                # 风
                fx = today_weather.get('fx')
                fl = today_weather.get('fl')
                wind = f"{fx} : {fl}"

                # 空气指数
                aqi = today_weather.get('aqi')
                aqi = f"空气 : {aqi}"
                
                weather_msg = f'{today_time}\n{notice}。' \
                    + f'\n{temperature}\n{wind}\n{aqi}\n' 
                return weather_msg

            else:
                return None
        except Exception as e:
            print('get_weather_info:', e)
            return None

class PowerWord:
    def __init__(self, config):
        self.config = config
        self.s = requests.session()

    def get_ciba_info(self):
        '''从词霸中获取每日一句，带英文
        :return: msg
        '''
        try:
            res = self.s.get(self.config.ciba_url)
            if res.status_code == 200:
                conent_json = res.json()
                content = conent_json.get('content')
                note = conent_json.get('note')
                return f"{content}\n{note}\n"
            else:
                return None
        except Exception as e:
            print('get_ciba_info:', e)
            return None
    

if __name__ == "__main__":
    w = Weather(WeatherConfig)
    w.get_weather_info()

    ciba = PowerWord(PowerWordConfig)
    msg = ciba.get_ciba_info()
    print(msg)
    # print(wc.girl_city_code)