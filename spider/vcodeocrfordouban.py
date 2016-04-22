#  -*- coding: utf-8 -*-
from PIL import Image
import pytesseract

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class VCodeOCR(object):
    def __init__(self, img):
        self.img = img
        self.frame = img.load()

    def pre(self):
        width, height = self.img.size
        threshold = 55
        for i in range(0, width):
            for j in range(0, height):
                p = self.frame[i, j]
                r, g, b = p
                if r > threshold or g > threshold or b > threshold:
                    self.frame[i, j] = WHITE
                else:
                    self.frame[i, j] = BLACK

    def remove_noise(self, window=1):
        """ 中值滤波移除噪点
        """
        if window == 1:
            # 十字窗口
            window_x = [1, 0, 0, -1, 0]
            window_y = [0, 1, 0, 0, -1]
        elif window == 2:
            # 3*3矩形窗口
            window_x = [-1, 0, 1, -1, 0, 1, 1, -1, 0]
            window_y = [-1, -1, -1, 1, 1, 1, 0, 0, 0]
        width, height = self.img.size
        for i in xrange(width):
            for j in xrange(height):
                box = []
                # black_count, white_count = 0, 0
                for k in xrange(len(window_x)):
                    d_x = i + window_x[k]
                    d_y = j + window_y[k]
                    try:
                        d_point = self.frame[d_x, d_y]
                        if d_point == BLACK:
                            box.append(1)
                        else:
                            box.append(0)
                    except IndexError:
                        self.frame[i, j] = WHITE
                        continue
                box.sort()
                if len(box) == len(window_x):
                    mid = box[len(box)/2]
                    if mid == 1:
                        self.frame[i, j] = BLACK
                    else:
                        self.frame[i, j] = WHITE

    def split(self):
        """  用竖线扫描分隔文字
        """
        img_new = self.img.copy()
        frame_new = img_new.load()
        width, heigth = self.img.size
        line_status = None
        pos_x = []
        for x in xrange(width):
            pixs = []
            for y in xrange(heigth):
                pixs.append(self.frame[x, y])
            if len(set(pixs)) == 1:
                _line_status = 0
            else:
                _line_status = 1
            if _line_status != line_status:
                if line_status is not None:
                    if _line_status == 0:
                        _x = x
                    elif _line_status == 1:
                        _x = x-1
                    pos_x.append(_x)
                    # 辅助线
                    for _y in xrange(heigth):
                        frame_new[x, _y] = BLACK
            line_status = _line_status
        # img_new.show()
        # 开始切分
        i = 0
        divs = []
        boxs = []
        while True:
            try:
                xi = pos_x[i]
                xj = pos_x[i+1]
            except Exception, e:
                break
            i += 2
            boxs.append([xi, xj])
        fixed_boxs = []
        i = 0
        while i < len(boxs):
            box = boxs[i]
            if box[1] - box[0] < 10:
                try:
                    box_next = boxs[i+1]
                    fixed_boxs.append([box[0], box_next[1]])
                    i += 2
                except Exception, e:
                    break
            else:
                fixed_boxs.append(box)
                i += 1
        for box in fixed_boxs:
            div = self.img.crop((box[0], 0, box[1], heigth))
            divs.append(div)
        # 过滤掉非字符的切片
        _divs = []
        for div in divs:
            width, heigth = div.size
            if width < 5:
                continue
            frame = div.load()
            points = 0
            for i in xrange(width):
                for j in xrange(heigth):
                    p = frame[i, j]
                    if p == BLACK:
                        points += 1
            # 单张图片中至少有N个黑色点
            if points <= 5:
                continue
            _divs.append(div)
        return _divs

    @staticmethod
    def image_to_string(img, config='-psm 8'):
        """
        使用tesseract 识别图片中的文字
        """
        try:
            result = pytesseract.image_to_string(img, lang='eng', config=config)
            result = result.strip()
            return result.lower()
        except IOError, e:
            return None


def run_test():
    image = Image.open('D:/captcha/captcha9.jpg')
    vcodeocr = VCodeOCR(image)
    print vcodeocr.image_to_string(image)
    vcodeocr.pre()
    vcodeocr.remove_noise(2)
    divs = vcodeocr.split()
    i = 0
    for div in divs:
        div.save("D:/captcha_pre/captcha_" + str(i) + ".jpg")
        print vcodeocr.image_to_string(div)
        i = i +1
    image.save("D:/captcha_pre/captcha_all.jpg", "JPEG")
    print vcodeocr.image_to_string(image)

if __name__ == "__main__":
    run_test()
