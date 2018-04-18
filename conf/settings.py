# -*- coding: utf-8 -*-   @Time    : 18-1-25 下午6:58
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

import os
import sys
from os.path import join


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)


SERVER_IP = '127.0.0.1'
SERVER_PORT = 9002
LISTEN_NUM = 5

SERVER_SHARE_DIR = '%s/database/server/' % BASE_DIR
SERVER_UPLOAD_DIR = '%s/database/server/upload/' % BASE_DIR

CONF_DIR = os.path.join(BASE_DIR, 'database/conf.ini')

DEBUG = True

CHOICE_FLAG = 'q'

# 设定用户上传文件和下载文件的模板路径, 用户文件夹以用户名命名,先用%s,以后待替换成username
USER_DOWNLOAD_TEMPLATE = join(BASE_DIR, 'database/client/%s/download/')
USER_UPLOAD_TEMPLATE = join(BASE_DIR, 'database/client/%s/upload/')
