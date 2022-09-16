# 获取sid，上面那块代码有小更改
# -*- coding:utf-8 -*-

import urllib
from http import cookiejar
import Image


class Login(object):
    """save sid and cookie"""

    def __init__(self):
        super(Login, self).__init__()
        print
        r"初始化中..."
        self.sid = ''
        self.jid = ''

    # 获取cookie
    def getCookie(self):
        # 创建CookieJar对象，自动管理cookie，可迭代
        ck = cookielib.CookieJar()
        # 创建类内部对象opener，把CookieJar塞进去，每次打开页面都会自动使用cookie
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(ck))
        # try:
            # 打开登陆页面，获取cookie
        self.opener.open('http://XXX.Mosaic.XXX.XXX/elect')
        # except urllib2.URLError, e:
        #     print "Error code:", e.code
        #     print "Return content", e.read()
        #     return None
        for item in ck:
            # 将cookie存到类内部变量jid中。
            self.jid = item.name + '=' + item.value
            return self.jid
        return None

    # 获取验证码
    def getCAPTCHA(self, cookie):
        # 输出cookie检查
        print
        self.jid
        # 按照包内格式，写好头部，是一个字典类型对象。
        header = {
            'Accept': 'image/webp,*/*;q=0.8', \
            'Accept-Encoding': 'gzip, deflate, sdch', \
            'Accept-Language': 'zh-CN,zh;q=0.8', \
            'Connection': 'keep-alive',
            # cookie的值使用self.jid
            'Cookie': self.jid, \
            'Host': 'XXX.Mosaic.XXX.XXX', \
            'Referer': 'http://XXX.Mosaic.XXX.XXX/elect/', \
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36'}
        # 随机数既然是随机的，服务器也应该不知道是什么，所以这里随便给一个。
        # 并且，随机数的值并没有和图片绑定，可以说是然并卵。
        # 编码参数`v`
        params = urllib.urlencode({'v': '0.1932646029163152'})
        # 构造`GET`的地址，格式为：`服务器地址`+`?`+`编码后的参数`
        capurl = ('http://XXX.Mosaic.XXX.XXX/elect/login/code?%s' % params)
        # 用opener打开页面，加上头部
        response = self.opener.open(urllib2.Request(capurl, headers=header))
        # response就是图片内容，将它写入本地图片文件中
        f = file("code.jpg", 'wb')
        f.write(response.read())
        f.close()
        # 关闭图片，之后可以在其他函数中用绝对路径打开图片。
        return

        # 获取sid，因为后面选课的时候要用，获取到了说明登陆成功。

    # 传入账号，密码，验证码。
    def getSid(self, username, password, j_code):
        # build header
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', \
            'Accept-Encoding': 'gzip, deflate', \
            'Accept-Language': 'zh-CN,zh;q=0.8', \
            'Cache-Control': 'max-age=0', \
            'Connection': 'keep-alive', \
            'Content-Length': '80', \
            'Content-Type': 'application/x-www-form-urlencoded', \
            'Cookie': self.jid, \
            'Host': 'XXX.Mosaic.XXX.XXX', \
            'Origin': 'http://XXX.Mosaic.XXX.XXX', \
            'Referer': 'http://XXX.Mosaic.XXX.XXX/elect/index.html', \
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36', \
            }

        # build post data
        # 后三个直接照抄
        postData = {'username': username, \
                    'password': password, \
                    'j_code': j_code, \
                    'lt': '', \
                    '_eventId': 'submit', \
                    'gateway': 'true', \
                    }
        # 编码postdata
        postData = urllib.urlencode(postData)
        # 目标服务器地址
        posturl = 'http://XXX.Mosaic.XXX.XXX/elect/login'
        # 构建request
        request = urllib2.Request(posturl, postData, header)
        # 用带有cookie的opener打开
        response = self.opener.open(request)
        # 分析返回的地址，`geturl()`就是这么用的。从中提取`sid`并储存。
        string = str(response.geturl())
        self.sid = string[string.find(r'sid=') + 4:]
        return self.sid


if __name__ == '__main__':
    # 创建类对象
    lo = Login()
    # 获取验证码
    j_code = lo.getCAPTCHA(lo.getCookie())
    # 打开验证码
    Image.open('code.jpg').show()
    # 输入信息
    j_code = raw_input(r"输入看到的验证码：")
    username = raw_input('username:')
    password = raw_input('password:')
    # 获取sid并输出，证明登陆成功。
    print
    lo.getSid(username, password, j_code)