# __author__: Mai feng
# __file_name__: run.py
# __time__: 2019:05:26:19:11

from UserAPI import UserAPI
from config import BaseConfig
from apscheduler.schedulers.blocking import BlockingScheduler

def run():
    '''主程序入口
    '''
    config = BaseConfig
    user = UserAPI(config)
    
    # 自动登陆
    if not user.is_online():
        return
 
    # 定时任务
    scheduler = BlockingScheduler()
    # 每天9：30左右给女朋友发送每日一句
    scheduler.add_job(user.send, 
                    'cron', 
                    hour=config.alarmHour, 
                    minute=config.alarmMinute)
    # 每隔2分钟发送一条数据用于测试。
    # scheduler.add_job(user.send, 'interval', seconds=30)
    scheduler.start()




if __name__ == "__main__":
    run()
