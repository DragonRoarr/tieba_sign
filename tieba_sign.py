#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import hashlib
import json
import os
import requests
import time
from threading import Thread

jsonFile=os.environ.get("jsonFile")
class Tieba(object):
    def __init__(self,):

        self.s = requests.session()

        self.MD5_KEY = 'tiebaclient!!!'
        self.CAPTCHA_API = 'http://222.187.238.211:10086/b'
        self.INDEX_URL = 'https://tieba.baidu.com/index.html'
        self.TBS_URL = 'http://tieba.baidu.com/dc/common/tbs'
        self.LIKES_URL = 'http://c.tieba.baidu.com/c/f/forum/like'
        self.SIGN_URL = 'http://c.tieba.baidu.com/c/c/forum/sign'
        self.GEN_IMG_URL = 'https://tieba.baidu.com/cgi-bin/genimg'
        self.QR_CODE_URL = 'https://passport.baidu.com/v2/api/getqrcode'
        self.UNICAST_URL = 'https://passport.baidu.com/channel/unicast'
        self.USER_INFO_URL = 'https://tieba.baidu.com/f/user/json_userinfo'
        self.QR_LOGIN_URL = 'https://passport.baidu.com/v3/login/main/qrbdusslogin'
        self.HAO123_URL = 'https://user.hao123.com/static/crossdomain.php'
        self.MY_LIKE_URL = 'http://tieba.baidu.com/f/like/mylike'

        self.ALL_TIEBA_LIST = []
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'c.tieba.baidu.com',
            'User-Agent': 'bdtb for Android 10.3.8.10'
        }

    def get_time_stamp(self):
        return str(int(time.time() * 1000))

    def load_cookie(self):
        cookie_dict = json.loads(jsonFile)#secret获取
        for k, v in cookie_dict.items():
            self.s.cookies.set(k, v)       

    def check_login(self):
        r = self.s.get(self.TBS_URL)
        rsp = r.json()
        return True if rsp['is_login'] == 1 else False

    def calc_sign(self, str_dict):
        md5 = hashlib.md5()
        md5.update((
            ''.join(
                '%s=%s' % (k, v)
                for k, v in str_dict.items()
            ) + self.MD5_KEY).encode('utf-8')
        )
        return md5.hexdigest().upper()

    def get_bduss_stoken(self):
        bduss = self.s.cookies.get_dict()['BDUSS']
        stoken = self.s.cookies.get_dict()['STOKEN']
        return bduss, stoken

    def get_like_tiebas(self):
        bduss, stoken = self.get_bduss_stoken()
        data = {
            'BDUSS': bduss,
            'stoken': stoken,
            'timestamp': self.get_time_stamp()
        }
        data['sign'] = self.calc_sign(data)
        for _ in range(5):
            try:
                r = requests.post(
                    url = self.LIKES_URL,
                    data = data,
                    cookies = self.s.cookies,
                    headers = self.headers,
                    timeout=3
                )
            except:
                continue
        return [tieba['name'] for tieba in r.json()['forum_list']]

    def get_tbs(self):
        r = self.s.get(self.TBS_URL).json()
        return r['tbs']


    def sign(self, tieba):
        tbs = self.get_tbs()
        bduss, stoken = self.get_bduss_stoken()
        data = {
            'BDUSS': bduss,
            'kw': tieba,
            'stoken': stoken,
            'tbs': tbs,
            'timestamp': self.get_time_stamp()
        }
        sign = self.calc_sign(data)
        data['sign'] = sign
        for _ in range(5):
            try:
                r = requests.post(
                    url = self.SIGN_URL,
                    data = data,
                    cookies = self.s.cookies,
                    headers = self.headers,
                    timeout=5
                )
                rsp = r.json()
                break
            except:
                continue

    def start(self, tiebas):
        threads = []
        for tieba in tiebas:
            t = Thread(target=self.sign, args=(tieba,))
            threads.append(t)
            
        for tieba in threads:
            tieba.start()

        for tieba in threads:
            tieba.join()

    def main(self):
        start_time = time.time()
        
        self.load_cookie()
        if self.check_login():
            print('CookieLogin: True')
            tiebas = self.get_like_tiebas()
            self.ALL_TIEBA_LIST.extend(tiebas)
            self.start(tiebas)
        else:
            print("failed login")

        
        end_time = time.time()
        print('total{}bars,spend{}seconds'.format(
            len(self.ALL_TIEBA_LIST),
            int(end_time - start_time)
            )
        )
 
if __name__ == "__main__":

    tieba = Tieba()
    tieba.main()
