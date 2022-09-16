import requests

if __name__ == '__main__':
    for i in range(0,4):
        s = requests.Session()
        pic = s.get('http://jwxt.upc.edu.cn/verifycode.servlet')
        print(s.cookies)
        with open('{}.jpeg'.format(i), 'wb') as pic_file:
            pic_file.write(pic.content)
            pic_file.close()
