# __author__: Mai feng
# __file_name__: config.py
# __time__: 2019:06:27:19:45

from CityInfo import cityDict

class BaseConfig:
    # 定时
    alarmHour = '8'
    alarmMinute = '30'
    # 女友信息
    girlInfos = {
        'girlName':'xxx', # 女朋友名字 很重要
        'girlCity':'成都', # 女朋友位置
        'sweetWords':'追梦直到永远！',
        'startDate':'2015-10-10', # 和女朋友什么时候在一起的
    }
    
    # 选择词霸还是dictum
    dictumChannel = 2 # 1是dict
    

# 天气配置
class WeatherConfig:
    girlCityCode = cityDict[BaseConfig.girlInfos['girlCity']]
    weatherUrl = f'http://t.weather.sojson.com/api/weather/city/{girlCityCode}'
    pass

# 每日一句配置
class WordConfig:
    cibaUrl = 'http://open.iciba.com/dsapi'
    dictumUrl = 'http://wufazhuce.com/'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
    }
    pass

if __name__ == "__main__":
    print(WeatherConfig.weatherUrl)

    
