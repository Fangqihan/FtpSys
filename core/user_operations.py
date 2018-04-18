# -*- coding: utf-8 -*-   @Time    : 18-1-25 下午7:29
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

from conf.settings import *
import subprocess
from os.path import join, getsize
import configparser


def user_select_file(**kwargs):
    """用户选择服务端下载的文件并返回具体路径"""
    global file_path
    file_path = ''
    if kwargs.get('type') == 'get':
        while True:
            print()
            print('服务器文件目录'.center(20, '-'))
            file_lst = os.listdir(SERVER_SHARE_DIR)
            for i in file_lst:
                print(i)

            print(''.center(20, '-'))

            holder_name = input('选择文件夹(q.返回主界面)>>> ').strip()
            if holder_name in get_holders_names(SERVER_SHARE_DIR):  # 文件夹名称输入正确则进入文件夹内部
                print(''.center(20, '-'))
                while True:
                    file_lst = os.listdir(join(SERVER_SHARE_DIR, holder_name))
                    for i in file_lst:
                        print(i)

                    file_name = input('选择文件(b.返回上一层)>>> ').strip()
                    if file_name in file_lst:
                        file_path = join(SERVER_SHARE_DIR, holder_name, file_name).replace('\\','/')
                        print('选择后的file_path: ', file_path)
                        return file_path
                    else:
                        print('文件名输入有误')

                    # elif file_name == 'b':
                    #     break

            if holder_name == 'q':
                return CHOICE_FLAG

    elif kwargs.get('type') == 'push':
        print()
        print('选择上传文件'.center(20, '-'))
        upload_dir = kwargs.get('dir', '')
        file_lst = os.listdir(upload_dir)
        for i in file_lst:
            print(i)

        print()
        while True:
            choice = input('选择文件(q.返回主界面)>>> ').strip()
            if choice == 'q':
                return CHOICE_FLAG
            if not choice: continue

            file_chosen = choice.strip()
            if file_chosen not in file_lst:
                print('文件名输入有误')
            else:
                return join(upload_dir, file_chosen)


def show_user_file_holder(**kwargs):
    """打印用户download和upload文件夹下文件列表以及占用容量百分比"""
    type = kwargs.get('type', '')
    file_path = kwargs.get('dir', '')
    allowed_storage = kwargs.get('allowed_storage', '')
    # 打印出待上传文件
    file_lst = os.listdir(file_path)
    for i in file_lst:
        print(i)

    if type == 'download':
        present_storage = get_file_holder_size(file_path)
        print('-----已占用容量{:.2f}%------'.format(present_storage / allowed_storage * 100))

    elif type == 'upload':
        print(''.center(20, '-'))


def get_file_holder_size(dir_name):
    """获取当前文件夹下所有文件的大小之和,不包含文件夹"""
    size = 0
    for root, dirs, files in os.walk(dir_name):
        size += sum([getsize(join(root, name)) for name in files])
        return size


def get_file_names(dir_path):
    """获取当前文件夹下的文件名称列表,用于判断输入的名称是否在当前文件夹下的文件名称"""
    for root, dirs, files in os.walk(dir_path):
        return files


def get_holders_names(dir_path):
    """获取当前文件夹下的文件夹名称列表,用于判断输入的名称是否在当前文件夹下的文件夹名称"""
    for root, dirs, files in os.walk(dir_path):
        return dirs

if __name__ == '__main__':
    print(os.listdir('E:\python_projects\socket_ftp\database'))


def upgrade_storage(**kwargs):
    """升级当前用户下载目录空间大小"""
    config = configparser.ConfigParser()
    config.read(CONF_DIR)
    username = kwargs.get('username', '')
    old_storage = kwargs.get('old_storage', '')
    while True:
        new_storage = input('新申请的下载存储空间>>> ').strip()
        if new_storage.isdigit():
            if int(new_storage)*1024*1024 > int(old_storage):
                config.set(username, 'storage', new_storage)
                with open(CONF_DIR, 'w') as f:
                    config.write(f)
                    print('------升级成功,下载空间为%sM------' % new_storage)
                    input()
                    break
            else:
                print('\033[1;35m 必须大于初始内存空间 \033[0m')
        else:
            print('\033[1;35m 空间大小必须为数字 \033[0m')



