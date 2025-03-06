from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from django.conf import settings
from common import helper, decodes
import apps, json, requests, random, os, base64
from .forms import *
from django.http import QueryDict
from django.views.decorators.http import require_http_methods

# 获取系统数据信息
@require_http_methods(["GET"])
def home_get(request):
    foodlist = apps.food.models.Food.objects.all()
    userlist = apps.user.models.User.objects.all()
    orderlist = apps.order.models.Order.objects.all()
    foodlisttmp = []
    for foodtmp in foodlist:
        foodlisttmp.append({'id':foodtmp.id, 'foodname': foodtmp.foodname, 'userid': foodtmp.user.id, 'user':foodtmp.user.username, 'foodicon':foodtmp.foodicon, 'foodprocedure':foodtmp.foodprocedure, 'video':foodtmp.video, 'remarks':foodtmp.remarks, 'price':foodtmp.price, 'created_at':foodtmp.created_at, 'updated_at':foodtmp.updated_at})
    return JsonResponse({"code":200,"message":"获取系统数据信息成功", "result":{
        "usernum": userlist.count(),
        "foodnum": foodlist.count(),
        "ordernum": orderlist.count(),
        "foodinfos": foodlisttmp,
        }}
    )

# 用户自己更新个人信息
@require_http_methods(["PUT"])
def home_updateInfo(request):
    try:
        # 序列化获取
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    if data.get("id") == None or data.get("username") == None or data.get("sex") == None or data.get("avatar") == None:
        return JsonResponse({"code":-1,"message":"更新用户个人信息失败, 必要信息不能为空"})
    
    # 判断用户是否存在
    if apps.user.models.User.objects.filter(username=data.get("username")).exclude(id=data.get("id")).exists():
        return JsonResponse({'code': -1, 'message': '更新用户个人信息失败，用户名存在'})
    try:
        # 修改用户信息
        apps.user.models.User.objects.filter(id=data.get("id")).update(username=data.get("username"), sex=data.get("sex"), avatar=data.get("avatar"))
    except:
        return JsonResponse({'code': -1, 'message': '更新用户个人信息失败，修改用户失败'})
    return JsonResponse({"code":200,"message":"更新用户个人信息成功"})

# 上传头像
@require_http_methods(["POST"])
def home_upuseravatar(request):
    filedata = request.FILES.get("file", None)
    try:
        filepath = helper.Uploadfile(os.path.join(settings.UPLOAD_FOLDER, "user/"), filedata)
    except:
        return JsonResponse({"code":-1,"message":"上传头像失败"})
    return JsonResponse({"code":200,"message":"上传头像成功", "result": filepath})

# 修改个人密码
@require_http_methods(["PUT"])
def home_updatePwd(request):
    try:
        # 序列化获取
        aesdata = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    # 解密
    plaintext, err = decodes.AesDecrypt(aesdata.get("data"))
    if err != "":
        return JsonResponse({"code":-1, "message":"修改密码失败, 解密错误"})
    try:
        # 序列化获取
        data = json.loads(plaintext.replace("'", "\"", -1))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    uid = data.get("uid")
    newPass = data.get("newpwd")
    if newPass == "" or newPass == None or uid == "" or uid == None:
        return JsonResponse({"code":-1, "message":"修改密码失败, ID或新密码不能为空"})
    # 修改密码
    ok = apps.user.models.User.objects.filter(id=uid).update(password=newPass)
    # 确认操作是否正确
    if ok == 0:
        return JsonResponse({"code":-1, "message":"修改密码失败, ID不存在"})
    return JsonResponse({"code":200,"message":"修改密码成功"})

# 获取每日金句
@require_http_methods(["GET"])
def home_getsentence(request):
    Url = request.GET.get('url')
    requ = requests.get(Url)
    requ.encoding = 'utf-8'
    stlist = requ.text.replace("\r", "").split("\n",-1)
    stsrt = stlist[random.randint(0, len(stlist)-1)]
    if stsrt != "":
        return JsonResponse({"code":200,"message":"获取每日金句成功", "result": stsrt})
    return JsonResponse({"code": 200,"message":"获取每日金句成功", "result": "好好吃饭，天天健康。"})
