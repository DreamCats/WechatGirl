# __author__: Mai feng
# __file_name__: WechatService.py
# __time__: 2019:05:26:16:12
import requests
import itchat
from yaml import load
import time
from datetime import datetime
from CityInfo import city_dict
from pyquery import PyQuery as pq
from apscheduler.schedulers.blocking import BlockingScheduler

'''基本配置'''
class BaseConfig:
    # 定时
    alarm_hour = '8'
    alarm_minute = '30'
    # 女友信息
    girl_infos = {
        'girl_name':'xxx', # 女朋友名字 很重要
        'girl_city':'成都', # 女朋友位置
        'sweet_words':'追梦直到永远！',
        'start_date':'2015-10-10', # 和女朋友什么时候在一起的
        'name_uuid':'' # 可以为空
    }
    
    # 选择词霸还是dictum
    dictum_channel = 2 # 1是dict
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
                
                weather_msg = f'{notice}。' \
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
    
    def get_dictum_info(self):
        ''' 获取格言信息（从『一个。one』获取信息 http://wufazhuce.com/）
        :return: msg
        '''
        try:
            res = self.s.get(url=self.config.dictum_url, headers=self.config.headers)
            if res.status_code == 200:
                doc = pq(res.text)
                today_dictum = doc('.fp-one-cita').eq(0).text()
                return today_dictum + '\n'
            else:
                return None
        except Exception as e:
            print('get_dictum_info:', e)
            return None


# hour, minute = [int(x) for x in alarm_timed.split(':')]

class UserLogin:
    def __init__(self, config):
        self.config = config
        pass

    def is_online(self, auto_login=False):
        '''判断是否还在线
        :param auto_login:True,如果掉线了则自动登录。
        :return: True ，还在线，False 不在线了
        '''
        def online():
            '''
            通过获取好友信息，判断用户是否还在线
            :return: True ，还在线，False 不在线了
            '''
            try:
                if itchat.search_friends():
                    return True
            except:
                return False
            return True
        
        if online():
            return True
        # 仅仅判断是否在线
        if not auto_login:
            return online()

                # 登陆，尝试 5 次
        for _ in range(5):
            # 命令行显示登录二维码
            itchat.auto_login(enableCmdQR=2)
            itchat.auto_login()
            if online():
                print('登录成功')
                return True
        else:
            print('登录成功')
            return False

    def start_today_info(self, is_test=False):
        '''
        每日定时开始处理。
        :param is_test: 测试标志，当为True时，不发送微信信息，仅仅获取数据。
        :return:
        '''
        # 每日一句
        ciba = PowerWord(PowerWordConfig)
        if self.config.dictum_channel == 1:
            dictum_msg = ciba.get_dictum_info()
        elif self.config.dictum_channel == 2:
            dictum_msg = ciba.get_ciba_info()
        else:
            dictum_msg = ''

        # 天气
        w = Weather(WeatherConfig)
        weather_msg = w.get_weather_info()

        # 甜蜜话语
        sweet_words = self.config.girl_infos['sweet_words']

        # 天数
        start_date = self.config.girl_infos['start_date']
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        day_delta = (datetime.now() - start_datetime).days
        delta_msg = f'宝贝这是我们在一起的第 {day_delta} 天。\n'

        # 个人信息
        name_uuid = self.config.girl_infos['name_uuid']
        girl_name = self.config.girl_infos['girl_name']

        # 今日日期
        today_time = datetime.now().strftime('%Y{y}%m{m}%d{d} %H:%M:%S').format(y='年', m='月', d='日')

        # 拼接
        today_msg = f'{today_time}\n{delta_msg}{weather_msg}{dictum_msg}{sweet_words}'
        print(today_msg)
        if not is_test:
            if self.is_online(auto_login=True):
                itchat.send(today_msg, toUserName=name_uuid)
            # 防止信息发送过快。
            time.sleep(5)

        print('发送成功..\n')

    def run(self):
        '''主程序入口
        '''
        # 自动登录
        if not self.is_online(auto_login=True):
            return
        wechat_name = self.config.girl_infos['girl_name']
        friends = itchat.search_friends(name=wechat_name)
        if not friends:
            print('昵称错误')
            return
        self.config.girl_infos['name_uuid'] = friends[0].get('UserName')
        
        # 定时任务
        scheduler = BlockingScheduler()
        # 每天9：30左右给女朋友发送每日一句
        scheduler.add_job(self.start_today_info, 'cron', hour=self.config.alarm_hour, minute=self.config.alarm_minute)
        # 每隔2分钟发送一条数据用于测试。
        # scheduler.add_job(self.start_today_info, 'interval', seconds=30)
        scheduler.start()


if __name__ == "__main__":
    user = UserLogin(BaseConfig)
    # user.start_today_info(is_test=True)
    user.run()