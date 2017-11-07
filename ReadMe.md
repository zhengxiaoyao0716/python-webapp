# Python-webapp开发模板

***
## 快速开始
### 开发
> 在 `src` 目录打开命令行，键入 `script\update` ，开始准备开发环境、安装依赖，然后按照提示输入项目名、项目版本号之类的。


### 运行
> 开发环境中，可以使用 [src\script\test.py](src\script\test.py) 脚本，以调试模式启动开发服务器。

> 生产环境请使用 `Docker` 进行部署，变量配置请参照 [project.py](src\project.py#L41) 。

> 也可以选择使用 `uwsgi` 之类可靠服务器部署启动，配置可参考 [.uwsgi.ini](.uwsgi.ini) 。


### 测试
> 在 `src` 目录打开命令行，键入 `script\ipython` ，然后将进入交互式后台，一些需要的环境、模块与函数已经提前导入了。

***
## 架构说明
### 技术
|功能|技术|--|
|--|--|--|
|部署|Docker+uwsgi||
|Http服务|Flask|Python3|
|Html渲染|Jinjia|Flask内置模板引擎|
|长连接|Flask-SocketIO||
> 关于多进程与分布式环境下部署的注意！
>- 如果你要在多进程或分布式环境中使用 `socket.io` ，你需要参照官网 [using-multiple-workers](http://flask-socketio.readthedocs.io/en/latest/#using-multiple-workers) 配置消息队列等。
>- 用户登录状态通过client-only-session保持，可以正常工作。但如果你要实现服务端session，请记得登录状态的共享。
