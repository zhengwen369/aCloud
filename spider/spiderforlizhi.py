#  -*- coding: utf-8 -*-
import json
import time
import common
import requests
from os.path import basename


class Spider:
    def __init__(self):
        pass

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
    }

    s = requests.session()

    def login(self, login_info):
        """
        登录荔枝FM
        :param login_info:dic
        :return: token
        """
        my_header = self.headers.copy()
        my_header["Host"] = "nj.lizhi.fm"
        my_header["Referer"] = "http://nj.lizhi.fm/account/login"
        r = self.s.post("http://nj.lizhi.fm/account/dologin", data=login_info, headers=my_header)
        return r.text

    def get_upload_token(self):
        """
        获取UploadToken
        """
        timestamp = str(time.time()).replace('.', '')
        my_header = self.headers.copy()
        my_header["Host"] = "nj.lizhi.fm"
        my_header["Referer"] = "http://nj.lizhi.fm/radio/upload"
        r = self.s.get("http://nj.lizhi.fm/radio/upload_token", params={"t": timestamp}, headers=my_header)
        return json.loads(r.text)

    def upload_file(self, file_full_name):
        """
        上传文件到网站
        :param file_full_name: 本地文件物理路径
        :return:
        """
        # 上传音频
        token_json = self.get_upload_token()
        upload_info = {
            "name": basename(file_full_name),
            "chunk": "0",
            "chunks": "1",
            "key": token_json["ret"]["key"],
            "token": token_json["ret"]["token"]
        }
        file1 = {'file': (basename(file_full_name), open(file_full_name, 'rb'), common.get_mime_type(file_full_name), {'Expires': '0'})}
        my_header = self.headers.copy()
        my_header["Host"] = "uplz.qiniu.com"
        my_header["Origin"] = "http://nj.lizhi.fm"
        my_header["Referer"] = "http://nj.lizhi.fm/radio/upload"
        r = self.s.post("http://uplz.qiniu.com/", data=upload_info, files=file1, headers=my_header)
        json_upload_result = json.loads(r.text)
        # 发布
        filename = upload_info["name"].split('.')[0]
        post_info = {
                "name": filename,
                "info": "",
                "audio_img": "",
                "audio_file": "",
                "x": "0",
                "y": "0",
                "w": "0",
                "h": "0",
                "imgRatio": "1",
                "avatar": "1",
                "ptime": "",
                "fileKey": json_upload_result["key"],
                "domain": token_json["ret"]["domain"],
                "bucket": token_json["ret"]["bunket"]
        }
        my_header = self.headers.copy()
        my_header["Host"] = "nj.lizhi.fm"
        my_header["Referer"] = "http://nj.lizhi.fm/radio/upload"
        r = self.s.post("http://nj.lizhi.fm/radio/json_uploadfinish_cloud", data=post_info, headers=my_header)
        return r.text

if __name__ == "__main__":
    file_full_name = u"E:/MP3Root/RootAdMP3/0/0/8/1363846799833.mp3"
    spider = Spider()
    login_info = {
            "phoneAreaNum": "86",
            "phoneNum": "xxx",
            "pwd": "xxx"
    }
    spider.login(login_info)
    result = spider.upload_file(file_full_name)
    print result
