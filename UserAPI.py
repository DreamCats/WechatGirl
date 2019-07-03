# __author__: Mai feng
# __file_name__: UserAPI.py
# __time__: 2019:05:26:16:12
import itchat
import time

from config import BaseConfig
from EveryDayAPI import EveryDayAPI

class UserAPI:
    def __init__(self, config):
        self.config = config
        self.d = EveryDayAPI(config)
        # 个人信息
        self.nameUuid = None
        self.girlName = self.config.girlInfos['girlName']
        pass

    def is_online(self):
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
        
        if online():
            return True

        # 登陆，尝试 5 次
        for _ in range(5):
            # 命令行显示登录二维码
            itchat.auto_login(enableCmdQR=2)
            # itchat.auto_login()
            if online():
                wechatName = self.girlName
                friends = itchat.search_friends(name=wechatName)
                if not friends:
                    print('昵称错误')
                    return
                self.nameUuid = friends[0].get('UserName')  
                print(f'{self.girlName}|{self.nameUuid}:登录成功')
                return True

    def send(self):
        '''发送消息
        '''
        if self.is_online(auto_login=True):
            todayMsg = self.d.start_today_info()
            print(f'sendName:{self.girlName}\n{todayMsg}')
            itchat.send(todayMsg, toUserName=self.nameUuid)
        # 防止信息发送过快。
        time.sleep(5)
        print('发送成功..\n')



if __name__ == "__main__":
    user = UserAPI(BaseConfig)
    user.send()
    # user.start_today_info(is_test=True)
    # user.run()
