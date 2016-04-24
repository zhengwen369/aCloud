#  -*- coding: utf-8 -*-
import hashlib
import json
import time
from os.path import getsize, basename
import requests
import rsa
from spider import common


class Spider(object):
    def __init__(self):
        pass

    headers = {
        "Host": "www.ximalaya.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0'
    }

    req_session = requests.session()

    token = ""

    @staticmethod
    def md5(msg):
        """
        计算MD5值
        :param msg: str
        """
        md5 = hashlib.md5()
        md5.update(msg)
        return md5.hexdigest()

    @staticmethod
    def encryption(msg):
        """
        计算rsa加密值
        :param msg: str,要求ascii编码,unicode编码会报错
        """
        modulus = (
            "009585A4773ABEECB949701D49762F2DFAB9599BA19DFE1E1A2FA200E32E0444F426DA528"
            "912D9EA8669515F6F1014C454E1343B97ABF7C10FE49D520A6999C66B230E0730C3F802D1"
            "36A892501FF2B13D699B5C7ECBBFEF428AC36D3D83A5BD627F18746A7FDC774C12A38DE27"
            "60A3B95C653C10D7EB7F84722976251F649556B"
        )
        public_exponent = "010001"
        n = int(modulus, 16)
        e = int(public_exponent, 16)
        key = rsa.PublicKey(n, e)
        return rsa.encrypt(msg, key).encode('base64')

    def get_login_token(self):
        """
        获取LoginToken
        """
        my_header = self.headers.copy()
        resp = self.req_session.get(
            "http://www.ximalaya.com/passport/token/login",
            headers=my_header
        )
        token_json = json.loads(resp.text)
        return token_json["token"]

    def login(self, login_info):
        """
        登录喜马拉雅FM
        :param login_info:dic
        :return: token
        """
        my_header = self.headers.copy()
        my_header["Referer"] = "http://www.ximalaya.com/explore/"
        password_md5 = str(self.md5(login_info["password"]) + self.get_login_token())
        login_info["password"] = self.encryption(password_md5)
        self.req_session.post(
            "http://www.ximalaya.com/passport/security/popupLogin",
            data=login_info,
            headers=my_header
        )
        self.token = self.req_session.cookies[r"1&_token"]

    def upload_file(self, album_id, file_full_name):
        """
        上传文件到网站
        :param album_id: 专辑Id
        :param file_full_name: 本地文件物理路径
        :return:
        """
        my_header = self.headers.copy()
        my_header["Referer"] = "http://www.ximalaya.com/upload"
        # 验证Token
        check_me_info = {
            "token": self.token,
            "rememberMe": "true"
        }
        self.req_session.get(
            "http://www.ximalaya.com/passport/check_me",
            params=check_me_info,
            headers=my_header
        )
        # 上传音频
        upload_info = {
            "fileSize": getsize(file_full_name),
            "token": self.token,
            "rememberMe": "true"
        }
        file1 = {
            'file': (
                basename(file_full_name),
                open(file_full_name, 'rb'),
                common.get_mime_type(file_full_name),
                {'Expires': '0'}
            )
        }
        resp = self.req_session.post(
            "http://upload.ximalaya.com/dtres/audio/upload",
            params=upload_info,
            files=file1,
            headers=my_header
        )
        json_upload_result = json.loads(resp.text)
        if json_upload_result["status"]:
            # 转码
            fileid = json_upload_result["data"][0]["uploadTrack"]["id"]
            timestamp = str(time.time()).replace('.', '')
            jindu_url = "http://www.ximalaya.com/dtres/zhuanma/%s/jindu/%s" % (fileid, timestamp)
            self.req_session.get(
                jindu_url,
                headers=my_header
            )
            self.req_session.get(
                "http://www.ximalaya.com/dtres/transcode/url",
                params={"uploadTrackId": fileid},
                headers=my_header
            )
            # 发布
            filename = json_upload_result["data"][0]["fileName"].split('.')[0]
            create_data = {
                "activity_id": "",
                "choose_album": album_id,
                "fileids[]": fileid,
                "files[]": filename,
                "intro_images": "",
                "is_album": "false",
                "is_hold_copyright": "on",
                "sound_announcer": "",
                "sound_author": "",
                "sound_image[]": "image_inherit",
                "sound_intro": "",
                "sound_lyric": "",
                "sound_rich_intro": "",
                "sound_tags": "",
                "sound_title": filename,
                "track_destroy": ""
            }
            resp = self.req_session.post(
                "http://www.ximalaya.com/upload2/create",
                data=create_data,
                headers=my_header
            )
            return resp.text


def run_test():
    album_id = "4064168"  # 专辑Id
    file_full_name = u"E:/MP3Root/RootAdMP3/0/0/8/1363846799833.mp3"
    spider = Spider()
    login_info = {
        "account": "xxx",
        "password": "xxx",
        "rememberMe": "true"
    }
    spider.login(login_info)
    result = spider.upload_file(album_id, file_full_name)
    print result

if __name__ == "__main__":
    run_test()
