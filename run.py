# __author__: Mai feng
# __file_name__: run.py
# __time__: 2019:05:26:19:11


from WechatService import BaseConfig, UserLogin


if __name__ == "__main__":
    user = UserLogin(BaseConfig)
    user.run()