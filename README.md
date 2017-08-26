# 银杏黄项目：对象服务结点故障快速定位

本工具提供了一个结点管理平台，在平台中，管理员可以批量分发命令与脚本至指定结点执行，并在本地接收对应结果。

通过自定义脚本，本方案可实现高度可定制化的结点日志分析功能。

## 开发

本工具为全新自主开发，前端框架/前端测试浏览器/Python模块 均使用了现有最新版本。js特性/视觉样式测试在Chrome(59.0.3071.115) 1920x1080 上表现正常。

前后端分离。后台源码结构简单，可二次开发。前端页面隔离，可分别再定制。

前端使用了HTML5和CSS3新特性，使用了 bootstrap 4.0.0 + fontawesome 4.7.0 + jquery 3.2.1 + chart.js2.6.0, 实现了响应式布局与交互效果。

后端使用了 python2.7 (web.py 0.38 + paramiko 2.2.1)

本平台实现了跨系统平台运行。目前在Linux/Windows下已测试运行正常。Mac请参考Linux自行安装。

## 安装
* Linux

        本工具推荐使用Linux作为运行平台。另外推荐使用virtualenv隔离python环境。 
        # 编译cryptography包所需环境
        apt-get install -y build-essential libssl-dev libffi-dev python-dev
        # 更新pip至最新，以避免无法找到包的问题
        pip install pip --upgrade
        # 编译安装所有依赖包
        pip install -r requirements.txt

* Windows

        # 安装 [VCForPython27](https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266) 以编译pycrypto包
        pip install pip --upgrade
        pip install -r requirements.txt



## Doc for Devs
后台:
* Web.py作为Web容器
* paramiko提供ssh交互
* /\_\_main\_\_.py 定义了WebAPI的路由信息与对应类名。主要通过控制Nodes对象实例来操纵SSH行为。
* /core/access.py Access类主要用于将连接信息配置文件解析为标准的连接信息配置对象。也提供Access配置文件的管理功能。
* /core/nodes.py Node载入Access对象，实现单独的SSH交互。Nodes为Node对象集的控制器。
* /core/config.py 加载全局配置文件/config/global.ini以初始化后台。
* /core/envsetup.py 初始化调整脚本运行路径、检测/修复目录结构。
* /core/notification.py 后台唯一的消息队列，由前端调用获取状态更新与命令结果。包含结点上下线/基本状态改变的信息、命令/脚本执行的结果。由Node/Nodes推入信息。另外，由于Notification取出即消失，为避免多个页面竞争取出Notification导致各页面都不正常，本前端App限制了只能同时开启一个页面。
* /core/modulefile.py 管理将被交付结点执行的模块文件
* /core/keyfile.py 管理用以连接结点的SSH密钥文件
* /config/global.ini 全局配置
* /config/nodes.list 结点连接配置文件
* /config/keyfile 密钥文件保存目录(可由前端加入或自行加入)
* /modules/\*(.description) 模块文件与模块详情描述文件。(可由前端加入或自行模仿.description文件格式加入)
* /static  前端文件目录
* /static/assets 包含前端中与工具本身无关的文件(如视觉效果用的css/js)
* /static/app 包含与本工具相关的js脚本
* /cache 后台缓存，自动生成。如full_nodes.list用于省略多次解析nodes.list(判断最后修改时间)。

前端：
* 状态更新的Notification在Dashboard/Nodes/Task被定时每3s从后台取出，由界面右上角的Sync按钮控制。
* NSL(Nodes Selecting Language)是一个简单的结点选择语言，解析器在/static/app/common.js中实现。
* 其他具体情况请阅读/static/*.html源码
