# -*- coding: utf-8 -*-   @Time    : 18-1-25 下午4:46
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

import json
from conf.settings import *
import configparser
from core.user_operations import show_user_file_holder

login_status = 0
download_dir = ''
upload_dir = ''
allowed_storage = 0


def login(func):
    def inner():
        global login_status
        if not login_status:
            print('登录中'.center(20, '-'))
            config = configparser.ConfigParser()
            config.read(CONF_DIR)
            flag = True
            while flag:
                username = input('用户名>>> ').strip()
                if username in config.sections():
                    while True:
                        global download_dir
                        global upload_dir
                        global allowed_storage
                        password = input('密码>>> ').strip()
                        if password == config[username]['password']:
                            download_dir = config[username]['download_dir']
                            upload_dir = config[username]['upload_dir']
                            allowed_storage = int(config[username]['storage']) * 1024 * 1024
                            print('登录成功'.center(20, '-'))
                            return func(download_dir=download_dir, upload_dir=upload_dir, allowed_storage=allowed_storage)

        else:
            return func(download_dir=download_dir, upload_dir=upload_dir, allowed_storage=allowed_storage)

    return inner()


def logout():
    global login_status
    global download_dir
    global upload_dir
    login_status = 0
    download_dir = ''
    upload_dir = ''














