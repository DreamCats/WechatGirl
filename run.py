# __author__: Mai feng
# __file_name__: run.py
# __time__: 2019:05:26:19:11


# from WechatService import BaseConfig, UserLogin
from UserAPI import UserAPI
from config import BaseConfig
from apscheduler.schedulers.blocking import BlockingScheduler
from EveryDayAPI import EveryDayAPI
import itchat
def run():
    '''主程序入口
    '''
    config = BaseConfig
    user = UserAPI(config)
    
    # 自动登陆
    if not user.is_online(auto_login=True):
        return
 
    # 定时任务
    scheduler = BlockingScheduler()
    # 每天9：30左右给女朋友发送每日一句
    # scheduler.add_job(d.start_today_info, 
    #                 'cron', 
    #                 hour=self.config.alarm_hour, 
    #                 minute=self.config.alarm_minute)
    # 每隔2分钟发送一条数据用于测试。
    scheduler.add_job(user.send, 'interval', seconds=30)
    scheduler.start()




if __name__ == "__main__":
    run()