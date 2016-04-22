#  -*- coding: utf-8 -*-
import datetime
import json
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
        登录考拉FM
        :param login_info:dic
        :return: token
        """
        my_header = self.headers.copy()
        my_header["Host"] = "www.kaolafm.com"
        my_header["Referer"] = "http://www.kaolafm.com/user/user/login/login.do"
        r = self.s.post("http://www.kaolafm.com/user/user/login/loginByEmail.do", data=login_info, headers=my_header)
        return r.text

    def get_albumImg(self, catalogId, albumId):
        album_info = {
            "catalogId": catalogId,
            "albumId": albumId
        }
        my_header = self.headers.copy()
        my_header["Host"] = "www.kaolafm.com"
        my_header["Referer"] = "http://www.kaolafm.com/user/program/0/add.do"
        r = self.s.get("http://www.kaolafm.com/user/program/getRecommondWords.do", params=album_info, headers=my_header)
        json_result = json.loads(r.text)
        return json_result["albumImg"]

    def upload_file(self, file_full_name):
        """
        上传文件到网站
        :param file_full_name: 本地文件物理路径
        :return:
        """
        upload_info = {
            "modelType": "programe_audio_audio",
            "oldUploadFile": ""
        }
        file1 = {'uploadAudioFile': (basename(file_full_name), open(file_full_name, 'rb'), common.get_mime_type(file_full_name), {'Expires': '0'})}
        my_header = self.headers.copy()
        my_header["Host"] = "www.kaolafm.com"
        my_header["Referer"] = "http://www.kaolafm.com/user/program/0/add.do"
        r = self.s.post("http://www.kaolafm.com/user/controller/admin/upload/uploadAudio.do", params=upload_info, files=file1, headers=my_header)
        return json.loads(r.text)

    def publish(self, album_id, catalog_id, file_full_name):
        store_base_path = "http://image.kaolafm.net"
        json_upload_file_info = self.upload_file(file_full_name)
        pub_info = {
            "activityId": "",
            "albumId": album_id,
            "anchorInfos": ""	,
            "audioDesc": "暂无",
            "catalogId": catalog_id,
            "cutSize": "550_550,340_340,250_250,100_100",
            "fileIndex": 1,
            "fileName": "",
            "filePath": store_base_path + json_upload_file_info["uploadFilePath"],
            "height": "",
            "imagePixelH": 550,
            "imagePixelW": 550,
            "img": self.get_albumImg(catalog_id, album_id),
            "imgSrc": "",
            "keyword": "暂无",
            "maxSize": 1024000,
            "minHeight":550,
            "minSize": 5120,
            "minWidth": 550,
            "status": 1,
            "suffix": "jpg",
            "title": json_upload_file_info["fileName"].split(".")[0],
            "url": "",
            "validStartdate": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "width": ""
        }
        my_header = self.headers.copy()
        my_header["Host"] = "www.kaolafm.com"
        my_header["Referer"] = "http://www.kaolafm.com/user/program/0/add.do"
        r = self.s.post("http://www.kaolafm.com/user/program/addInput.do", data=pub_info, headers=my_header)
        return r.text

    """暂时无用
    def setCoords(self, coods_info, jw):
        scalewh = 148
        coods = {
            "x": (jw - scalewh)/2,
            "y": (jw - scalewh)/2,
            "w": scalewh,
            "h": scalewh
        }
        coods_info["w"] = int(coods["w"] * coods_info["cw"])
        coods_info["h"] = int(coods["h"] * coods_info["cw"])
        coods_info["x"] = int(coods["x"] * coods_info["cw"])
        coods_info["y"] = int(coods["y"] * coods_info["cw"])

    def check_user_level(self):
        result = False
        my_header = self.headers.copy()
        my_header["Host"] = "www.kaolafm.com"
        my_header["Referer"] = "http://www.kaolafm.com/user/program/0/add.do"
        r = self.s.get("http://www.kaolafm.com/user/program/checkUserLevel.do", headers=my_header)
        json_result = json.loads(r.text)
        if json_result["level"] is not None:
            if json_result["level"] == 2 or json_result["level"] == 3:
                result = True
        return result

    def upload_image(self, img_full_name):
        # 上传
        upload_info = {
            "minWidth": 550,
            "minHeight": 550,
            "suffix": splitext(img_full_name)[1][1:],
            "maxSize": 1024000,
            "minSize": 5120
        }
        file1 = {'uploadImageFile': (basename(img_full_name), open(img_full_name, 'rb'), common.get_mime_type(img_full_name), {'Expires': '0'})}
        my_header = self.headers.copy()
        my_header["Host"] = "www.kaolafm.com"
        my_header["Referer"] = "http://www.kaolafm.com/user/program/0/add.do"
        r = self.s.post("http://www.kaolafm.com/user/controller/admin/upload/newUploadImageCommon.do", params=upload_info, files=file1, headers=my_header)
        # 切片
        json_upload_result = json.loads(r.text)
        jw = 296
        coods_info = {
            "x": 0,
            "y": 0,
            "w": 100,
            "h": 100,
            "cw": float(json_upload_result["width"])/jw,
            "imgSrc": json_upload_result["uploadFilePath"],
            "suffix": upload_info["suffix"],
            "maxSize": upload_info["maxSize"],
            "minSize": upload_info["minSize"],
            "fileName": json_upload_result["fileName"],
            "imagePixelW": 550,
            "imagePixelH": 550,
            "cutSize": "550_550,340_340,250_250,100_100",
            "iname": json_upload_result["fileName"]
        }
        self.setCoords(coods_info, jw)
        r = self.s.post("http://www.kaolafm.com/user/controller/admin/upload/newUploadImageCutCommon.do", data=coods_info, headers=my_header)
        json_upload_result = json.loads(r.text)
    """

if __name__ == "__main__":
    spider = Spider()
    login_info = {
            "userName": "xxx",
            "password": "xxx",
            "isRemberMe": "yes"
    }
    spider.login(login_info)
    file_full_name = r"E:\MP3Root\RootAdMP3\0\0\8\1363846799833.mp3"
    albumId = "1100000160109"
    catalogId = "120"
    result = spider.publish(albumId, catalogId, file_full_name)
    print result
