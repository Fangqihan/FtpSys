# -*- coding: utf-8 -*-   @Time    : 18-1-25 下午4:47
# @Author  : QiHanFang    @Email   : qihanfang@foxmail.com

from socket import *
from conf.settings import *
from utils.common_func import get_file_md5
import struct
import json


def receive(conn):
    '''接收客户端发过来的文件'''
    while True:
        header_size_obj = conn.recv(4)
        if header_size_obj.decode('utf-8') == CHOICE_FLAG:
            # 检查是否是返回主界面命令
            print('接收到服务端返回主界面')
            break

        if not header_size_obj: continue
        # 获取header长度
        header_obj_size = struct.unpack('i', header_size_obj)[0]
        # 获取header信息
        header_obj_json = conn.recv(header_obj_size).decode('utf8')
        header_obj_dict = json.loads(header_obj_json)
        print('header_obj_dict: ', header_obj_dict)
        filename = header_obj_dict.get('filename', '')
        total_size = header_obj_dict.get('size', '')
        old_md5 = header_obj_dict.get('md5', '')
        # 逐行接收服务端返回的文件
        recv_size = 0
        save_path = '%s%s' % (SERVER_UPLOAD_DIR, filename)
        with open(save_path, 'wb') as f:
            while recv_size < total_size:
                rec1 = conn.recv(8888)
                f.write(rec1)
                recv_size += len(rec1)
            print('文件上传进度进度:{:.2f}%'.format(recv_size / total_size * 100), flush=True, end='\r')

        # 源文件和下载后文件一致性检验
        new_md5 = get_file_md5(save_path)
        file_check = ''
        if new_md5 == old_md5:
            file_check = '一致性匹配合格'
        else:
            file_check = '服务端发送的文件与收到的文件不一致'
        result_dic = {'file_check':file_check, 'upload_status':recv_size / total_size}
        result_str = json.dumps(result_dic)
        result_bytes = json.dumps(result_dic).encode('utf-8')
        result_size = struct.pack('i', len(result_str))
        conn.send(result_size)
        conn.send(result_bytes)
        break


def transfer(conn):
    '''将文件发送给客户端'''
    while True:
        file_path = conn.recv(8000).decode('utf-8').strip()  # 接收客户端选定的文件路径
        if file_path == CHOICE_FLAG:  # 检查是否是返回主界面命令
            print('接收到服务端返回主界面')
            break

        filename = file_path.split('/')[-1]
        try:
            file_size = os.path.getsize(file_path)
        except Exception as e:
            print('文件名称有误')
        # 制作文件的header信息
        header = {
            'filename': filename,
            'md5': get_file_md5(file_path),
            'size': file_size,
        }
        header_obj = json.dumps(header)  # 序列化成str类型
        header_obj_bytes = header_obj.encode('utf-8')
        # 将报头字节大小制作成定长字节串并发送给客户端
        header_obj_size = struct.pack('i', len(header_obj_bytes))
        conn.send(header_obj_size)
        conn.send(header_obj_bytes)
        # 读取客户选定的文件并逐行发送给客户端
        with open(file_path, 'rb') as f:
            for line in f:
                conn.send(line)
        break


def run_server():
    '''运行服务器'''
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET,SO_REUSEADDR, 1)
    server.bind((SERVER_IP, SERVER_PORT))
    server.listen(LISTEN_NUM)
    conn, server_addr = server.accept()
    while True:
        print('待接收....')
        choice = conn.recv(1).decode('utf-8')
        if not choice:break
        if choice in ['1', '2', '5']:
            if choice == '1':
                receive(conn)  # 开始接收客户端上传的文件
            elif choice == '2':
                transfer(conn)  # 开始向客户端发送文件
            elif choice == '5':
                break  # 响应客户端的操作

    conn.close()
    server.close()


if __name__ == '__main__':
    run_server()






