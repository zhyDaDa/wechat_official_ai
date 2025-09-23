# wechat_official_ai

原先者-技术爬爬虾，转载请注明作者
修改为单纯的微信公众号AI聊天机器人, 不接入其他平台

## 部署方法

在云服务上部署，云服务器必须有公网IP  

### 安装依赖  

``pip3 install -r requirements.txt``

### 修改配置文件  

打开配置文件config.yaml 配置参数

### 运行项目  

``sh start.sh``  

对于docker部署, 可以使用 ``python3 main.py 80`` 直接运行

### 配置微信公众号

打开微信公众平台 设置与开发-基本配置-服务器配置  
将服务器地址(URL)改为 <http://xxx.xxx.xxx.xxx:80/wx> 其中xxx为云服务器的IP地址  
令牌(Token)，消息加密钥随意填，消息加密选明文方式，点击启用服务器配置。

### 使用方法

给公众号发消息，公众号就会给与回答。  
