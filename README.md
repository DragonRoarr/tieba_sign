# Tieba_Sign
[![](https://img.shields.io/github/license/Aruelius/tieba_sign.svg?color=ff69b4)](https://github.com/Aruelius/tieba_sign/blob/master/LICENSE)  [![](https://img.shields.io/badge/Python-3.7-ff69b4.svg)](hhttps://github.com/Aruelius/tieba_sign)  

百度贴吧多线程自动登陆 / 自动签到 / 自动打码

经测试：在三个帐号，一共207个贴吧的情况下，全部签到完成速度为12s左右。(Cookies登录情况下)

**Use：Python3**

## 效果

![alt 效果图](./View.png)

## 使用教程

###### 1.安装依赖

```python
pip install -r requirements.txt
```

###### 2.修改配置文件(config.py)

```python
users = ['用户名']
# 用户名,例如['用户1', '用户2', '用户3'] 一共3个用户

accounts = {
    '用户名': {
        'username': '帐号',
        'password': '密码'
    }
}

#用户名以及对应的帐号密码
#例如：
#accounts = {
#    '用户1': {
#        'username': '用户1的帐号',
#        'password': '用户1的密码.'
#    },
#    '用户2': {
#        'username': '用户2的帐号',
#        'password': '用户2的密码'
#    },
#    '用户3': {
#        'username': '用户3的帐号',
#        'password': '用户3的密码'
#    }
#}
# 一定要按照users里面的用户名顺序来填写accounts！！！
# 一定要按照users里面的用户名顺序来填写accounts！！！
# 一定要按照users里面的用户名顺序来填写accounts！！！
```

### 运行

```shell
python tieba_sign.py # 开始登录并签到
```

### TODO

- 手机号码登陆（Working）

- 扫码登陆，动态口令登陆（Working）

- 自动获取QQ邮箱验证码，达到全自动登陆（Woking）

- 添加打码平台（已完成）
- 二次使用Cookie登陆（已完成）
- 多线程签到（已完成）
- 多账号签到（已完成）

### 优势

1. Python3
2. 支持Windows / Mac / Linux 全平台
3. 使用自建免费打码平台
4. 签到200个贴吧仅需10s左右
5. 支持邮箱和手机验证

### 注意事项

- 如果使用Crontab自动签到，请先将已经得到的Cookie文件放入/root/目录下

  > 如果不是root用户，把Cookie放入当前用户目录下即可
  >
  > Cookie文件格式为‘.User’，User为用户名，整体为隐藏文件
  >
  > 复制命令为cp，例子：```cp .User /root/```
  >
  > 查看隐藏文件命令为```ll -a```
  >
  > 建议设置自动签到时间为早四点和下午四点：04:00 16:00防止漏签
  >
  > 漏签只有一个原因，网络问题导致连接打码服务器出问题。

- 遇到任何问题，请提交Issues！

### ChangeLog

2019年06月12日

1. 重写登陆块，放弃selenium模拟登陆
2. 二次验证支持邮箱，手机验证码
3. 代码逻辑有改善

------

2019年04月07日

1. 添加多线程签到，签到速度约为1秒20个贴吧
2. 去除若快打码，使用自己训练的验证码识别接口，识别速度更快，准确率可以打到99.99%
3. 增加多用户签到，自行按照config.py文件填写相应帐号密码即可

------

2019年03月25日

1. 修复不能正确判断验证类型的BUG

   > 由于Centos安装的Chrome版本为71，Ubuntu为73，71版本的Chrome登录一定是验证码+二代验证，而73版本正常登录只有二代验证，所以这里判断策略出了点问题。

------

2019年03月20日

1. 由于签到一百个贴吧之后需要验证码，所以添加了打码功能，打码平台为若快打码
2. 登录一次之后会自动保存Cookie在本地，后续签到直接调用Cookie

------

### LICENSE

[MIT](https://github.com/Aruelius/tieba_sign/blob/master/LICENSE)

