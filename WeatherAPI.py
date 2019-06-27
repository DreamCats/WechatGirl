# __author__: Mai feng
# __file_name__: WeatherAPI.py
# __time__: 2019:06:27:20:20

from config import WeatherConfig
import requests
# 天气api
class WeatherAPI:
    def __init__(self, config):
        # 配置
        self.config = config
        # requests
        self.s = requests.session()

    def getInfo(self):
        '''获取天气信息
        '''
        res = self.s.get(url=self.config.weatherUrl)
        if res.status_code == 200:
            data = res.json()['data']
            # 今日天气
            todayWeather = data.get('forecast')[1]

            # 今日天气注意事项
            notice = todayWeather.get('notice')

            # 温度
            high = todayWeather.get('high')
            highC = high[high.find(' ') + 1:]
            low = todayWeather.get('low')
            lowC = low[low.find(' ') + 1:]
            temperature = f"温度 : {lowC}/{highC}"

            # 风
            fx = todayWeather.get('fx')
            fl = todayWeather.get('fl')
            wind = f"{fx} : {fl}"

            # 空气指数
            aqi = todayWeather.get('aqi')
            aqi = f"空气 : {aqi}"
            weatherWsg = f'{notice}。' \
                    + f'\n{temperature}\n{wind}\n{aqi}' 
            return weatherWsg

        else:
            raise 'getInfo->error->200'
            

if __name__ == "__main__":
    wapi = WeatherAPI(WeatherConfig)
    msg = wapi.getInfo()
    print(msg)