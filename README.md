#### 项目名称
模拟云盘在线下载和上传系统


----------


#### 项目启动:
1. 切换工作路径至`bin`目录下;
2. 启动`start_server.py`文件;
3. 启动`start_client.py`文件;


----------


#### 主要功能介绍
1. 用户认证;
2. 上传本地文件文件之服务器;
3. 从服务器目录中选定文件并下载:


----------


#### 代码结构分布图
![项目目录](http://oyhijg3iv.bkt.clouddn.com/%E6%B7%B1%E5%BA%A6%E6%88%AA%E5%9B%BE_%E9%80%89%E6%8B%A9%E5%8C%BA%E5%9F%9F_20180128143535.png)


----------


#### 项目补充说明
1. `conf.ini`: 包含了用户的信息配置,主要有用户名密码、下载目录、上传目录以及下载目录最大容量；
2. `core/client.py`与`core/server.py`主要函数功能: 
    > `run_client()`启动客户端后进入操作界面;         
    > `upload()`函数是将本地文件上传至服务器;
    > `download()`选择服务器上的文件并下载至本地;
	> 客户端与服务端保持同步:客户端若退出选择的目录,那么会返回一个信号给服务端,服务端也会返回进入主目录的待接收状态,再次接收1, 2, 5这三个信号


----------


## 待扩展功能
1. 目前本系统没有设置用户注册功能,只有三个用户,注意,用户`download`目录和`upload`目录不可随意更改;
2. 进度条, 目前只有进度结果显示,灭有动态进度条功能


----------
