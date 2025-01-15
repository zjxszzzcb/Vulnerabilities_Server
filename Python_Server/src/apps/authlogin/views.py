from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.conf import settings
from apps.user.models import User
from rest_framework_jwt.settings import api_settings
from django.views.decorators.http import require_http_methods
from common import helper
import json, base64, hashlib


# 处理用户登录
@require_http_methods(["POST"])
def auth_login(request):
    try:
        # 序列化获取
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    username = data.get('username')
    password = data.get('password')
    code = data.get('code')
    # 验证码
    if code == "" or code == None:
        return JsonResponse({'code': -1, 'message': '登录失败，验证码不能为空'})
    if username == None or password == None or username == "" or password == "":
        return JsonResponse({'code': -1, 'message': '登录失败，用户名或密码不能为空'})
    try:
        user = User.objects.get(username=username)
    except:
        return JsonResponse({'code': -1, 'message': '登录失败，用户名不存在'})
    md5_obj = hashlib.md5()
    md5_obj.update(user.password.encode('utf-8'))
    if md5_obj.hexdigest() != base64.b64decode(password).decode('utf-8')[:32]:
        return JsonResponse({'code': -1, 'message': '登录失败，密码错误'})
    
    return JsonResponse({'code': 200, 'message': '登录成功', 'result': {
        'uid': user.id,
        'Authorization': 'Bearer '+helper.Generatejwt(user.id, user.role.id, user.username, settings),
        'username': user.username,
        'avatar': user.avatar,
        'phone': user.phone,
        'sex': user.sex,
        'email': user.email,
        'role': user.role.name,
        'rolelevel': user.role.id,
        'introduce': "这是一个集合了多种语言的Web靶场，该系统是以食谱菜单管理系统为场景去编写，一种实战化形式的安全漏洞靶场，其中存在多个安全漏洞，需要我们去探索和发现。\n\n该项目旨在帮助安全研究人员和爱好者了解和掌握关于不同语言系统的渗透测试和代码审计知识。项目地址：https://github.com/A7cc/Vulnerabilities_Server",
        'created_at': user.created_at,
    }})

# 处理用户注销
@require_http_methods(["GET"])
def auth_loginout(request):
    return JsonResponse({'code': 200, 'message': '注销成功'})

