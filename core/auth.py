# -*- coding: utf-8 -*-   @Time    : 18-1-25 下午4:46
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

from conf.settings import *
import configparser
from os.path import join
import os

login_status = 0
download_dir = ''
upload_dir = ''
allowed_storage = 0


def register():
    print('注册中'.center(20, '-'))
    config = configparser.ConfigParser()
    config.read(CONF_DIR)
    while True:
        username = input('用户名>>> ').strip()
        if username not in config.sections():
            if len(username) < 3:
                print('用户名长度至少是三位')
            else:
                while True:
                    password = input('密码>>> ').strip()
                    if len(password) >=6:
                        storage = input('您申请的空间大小>>> ')
                        if storage.isdigit():
                            if int(storage) in range(20, 1000):
                                config.add_section(username)
                                config.set(username, 'password', password)
                                config.set(username, 'download_dir', USER_DOWNLOAD_TEMPLATE % username)
                                config.set(username, 'upload_dir', USER_UPLOAD_TEMPLATE % username)
                                config.set(username, 'storage',  storage)
                                with open(CONF_DIR, 'w') as f:
                                    config.write(f)
                                # 创建下载和上传文件夹
                                os.makedirs(join(BASE_DIR, USER_DOWNLOAD_TEMPLATE % username))
                                os.makedirs(join(BASE_DIR, USER_UPLOAD_TEMPLATE % username))
                                print('注册成功'.center(20, '-'))
                                input()
                                return

                            else:
                                print('免费申请空间20-1000(M)')
                        else:
                            print('输入有误')
        else:
            print('对不起,该用户名已经被注册', end='\n\n')


def login(func):
    def inner(**kwargs):
        global login_status, download_dir, upload_dir, allowed_storage, username
        if not login_status:
            while True:
                choice = input('1.登录\n2.注册\n3.退出\n输入操作编号>>> ')
                if choice == '1':
                    config = configparser.ConfigParser()
                    config.read(CONF_DIR)
                    print()
                    print('登录中'.center(20, '-'))
                    while True:
                        username = input('用户名>>> ').strip()
                        if username in config.sections():
                            lock_status = config[username]['lock_status']
                            if lock_status == '0':
                                count = 0
                                while count < 3:
                                    password = input('密码>>> ').strip()
                                    if password == config[username]['password']:
                                        download_dir = join(BASE_DIR, config[username]['download_dir'])
                                        upload_dir = join(BASE_DIR, config[username]['upload_dir'])
                                        allowed_storage = int(config[username]['storage']) * 1024 * 1024
                                        print('登录成功'.center(20, '-'))
                                        return func(username=username,download_dir=download_dir, upload_dir=upload_dir,
                                                    allowed_storage=allowed_storage)

                                    count += 1
                                if count == 3:
                                    config.set(username, 'lock_status', '1')
                                    with open(CONF_DIR, 'w') as f:
                                        config.write(f)
                                        print('\033[1;35m 对不起,您输入的密码次数过多, 已被锁定! \033[0m', end='\n\n')

                            else:
                                print('\033[1;35m 对不起,该用户已被冻结 \033[0m', end='\n\n')

                        else:
                            print('对不起,用户名输入有误', end='\n\n')

                if choice == '2':
                    register()

                if choice == '3':
                    exit('退出')
        else:
            return func(username=username,download_dir=download_dir, upload_dir=upload_dir, allowed_storage=allowed_storage)

    return inner



















