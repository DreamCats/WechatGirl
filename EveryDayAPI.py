# __author__: Mai feng
# __file_name__: EveryDayAPI.py
# __time__: 2019:06:27:20:49

from WeatherAPI import WeatherAPI
from WordAPI import WordAPI
from config import WordConfig, WeatherConfig, BaseConfig
from datetime import datetime
class EveryDayAPI:
    def __init__(self, baseConfig):
        self.config = baseConfig
        self.ciba = WordAPI(WordConfig)
        self.w = WeatherAPI(WeatherConfig)

    def start_today_info(self):
        '''
        每日定时开始处理。
        :param is_test: 测试标志，当为True时，不发送微信信息，仅仅获取数据。
        :return:
        '''
        # 每日一句
        if self.config.dictumChannel == 1:
            dictumMsg = self.ciba.getMotto()
        elif self.config.dictumChannel == 2:
            dictumMsg = self.ciba.getCiBa()
        else:
            dictumMsg = ''

        # 天气
       
        weatherMsg = self.w.getInfo()

        # 甜蜜话语
        sweetWords = self.config.girlInfos['sweetWords']

        # 天数
        startDate = self.config.girlInfos['startDate']
        startDatetime = datetime.strptime(startDate, "%Y-%m-%d")
        dayDelta = (datetime.now() - startDatetime).days
        deltaMsg = f'宝贝这是我们在一起的第 {dayDelta} 天。\n'


        # 今日日期
        todayTime = datetime.now().strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年', 
        m='月', d='日')

        # 拼接
        todayMsg = f'{todayTime}\n{deltaMsg}{weatherMsg}\n{dictumMsg}\n{sweetWords}'

        return todayMsg


if __name__ == "__main__":
    dapi = EveryDayAPI(BaseConfig)
    todayMsg = dapi.start_today_info()
    print(todayMsg)