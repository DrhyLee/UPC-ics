def login(request):
    if request.method == "GET":
        return render(request, "lab.html")
    if request.method == "POST":
        login_info = request.POST
        user_name = login_info.get("user_name",None)
        user_pwd = login_info.get("user_pwd",None)
        if user_name != "":
            if user_pwd != "":
                try:
                    db_search = user_info.objects.get(user_name=user_name)
                    if db_search.user_pwd != user_pwd:
                        return HttpResponse(json.dumps({"usr_data": "密码错误", "result": 1}))
                    else:
                        return HttpResponse(json.dumps({"usr_data": "登录成功", "result": 0}))
                except:
                    return HttpResponse(json.dumps({"usr_data": "用户不存在", "result": 1}))
            else:
                return HttpResponse(json.dumps({"usr_data":"密码为空","result":1}))
        else:
            return  HttpResponse(json.dumps({"usr_data":"用户名为空","result":1}))

if __name__ == '__main__':
    login()