import urllib,json,requests
url = 'http://www.hylee.xyz/课程表/jwxtsource.html'
headers = {}
data = {'username':'asd','pwd':'123456$'}
request = requests.post(url=url, data=data,json=True,headers=headers)
response = request.content.decode()
#需要携带请求头信息的可以全部写在headers里面，data就是请求体，需要携带其他信息的也可以另外再加
print(response)
#一般情况下就可以请求成功得到返回值