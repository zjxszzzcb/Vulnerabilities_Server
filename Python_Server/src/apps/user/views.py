from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
import json, datetime
from common import decodes
from apps.user.models import User
from apps.role.models import Role
from django.views.decorators.http import require_http_methods
from django.db import connection

# 获取用户列表信息
@require_http_methods(["GET"])
def user_get(request):
    page = request.GET.get('page')
    size = request.GET.get('size')
    status = request.GET.get('status')
    Keyword = request.GET.get('keyword')
    if page == None or page == '':
        page = 1
    if size == None or size == '':
        size = 10
    Page = int(page)
    Size = int(size)
    try:
        userlistall = User.objects.filter(deleted_at__isnull=True).order_by('id')
        # 关键字查询
        if Keyword != None and Keyword != '':
            userlistall = userlistall.filter(username__contains=Keyword)
        # 状态查询
        if status == '0':
            userlistall = userlistall.filter(status='False')
        elif status == '1':
            userlistall = userlistall.filter(status='True')
    except:
        return JsonResponse({'code': -1, 'message': '获取用户列表失败'})
    # 计算
    cnt = userlistall.count()
    userlisttmp = []
    for usertmp in userlistall:
        userlisttmp.append({'id':usertmp.id, 'role': usertmp.role.name, 'role_id': usertmp.role.id, 'username':usertmp.username, 'password': usertmp.password, 'phone':usertmp.phone, 'sex':usertmp.sex, 'email':usertmp.email, 'avatar':usertmp.avatar, 'status':usertmp.status, 'created_at':usertmp.created_at, 'updated_at':usertmp.updated_at})
    return JsonResponse({"code":200,"message":"获取用户列表成功","result": {
        "count": cnt,
        "list":  userlisttmp[(Page-1)*Size:Page*Size],
    }})

# 新增用户信息
@require_http_methods(["POST"])
def user_add(request):
    try:
        # 序列化获取
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    sex = data.get('sex')
    status = data.get('status')
    role_id = data.get('role_id')
    email = data.get('email')
    remarks = data.get('remarks')
    if username == None or username == '':
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，username 参数不能为空'})
    if password == None or password == '':
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，password 参数不能为空'})
    if phone == None or phone == '':
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，phone 参数不能为空'})
    if sex == None or sex == '':
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，sex 参数不能为空'})
    if status == None or status == '':
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，status 参数不能为空'})
    if role_id == None or role_id == '':
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，role_id 参数不能为空'})
    if email == None or email == '':
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，email 参数不能为空'})
    usertmp, err = decodes.TripleDESDecrypt(username)
    if err != "":
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，解密失败'})
    pwdtmp, err = decodes.TripleDESDecrypt(password)
    if err != "":
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，解密失败'})
    # 判断用户是否存在
    if User.objects.filter(username=usertmp).exists():
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，用户存在'})
    # 判断角色是否存在
    if not Role.objects.filter(id=role_id).exists():
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，角色不存在'})
    try:
        # 创建用户
        User.objects.create(username=usertmp, password=pwdtmp, phone=phone, sex=sex, status=status, role_id=role_id, email=email, remarks=remarks)
    except:
        return JsonResponse({'code': -1, 'message': '新增用户信息失败，创建用户失败'})
    return JsonResponse({"code":200,"message":"新增用户信息成功"})

# 获取用户详细信息
@require_http_methods(["GET"])
def user_detail(request):
    # 获取id
    id = request.GET.get('id')
    if id == "" or id == None:
        return JsonResponse({"code": -1, "message": "获取用户详细信息失败，id 参数不能为空"})
    # 获取角色信息
    user = User.objects.filter(id=id).values('id', 'username', 'password', 'phone', 'sex', 'status', 'role_id', 'email', 'remarks').first()
    if user == None:
        return JsonResponse({"code": -1, "message": "获取用户详细信息失败，用户不存在"})
    # 解密
    try:
        user['username'] = decodes.RSAEncrypt(user['username'])
        user['password'] = decodes.RSAEncrypt(user['password'])
        user['phone'] = decodes.RSAEncrypt(user['phone'])
        user['email'] = decodes.RSAEncrypt(user['email'])
    except:
        return JsonResponse({"code": -1, "message": "获取用户详细信息失败，解密失败"})
    return JsonResponse({"code":200,"message":"获取用户详细信息成功","result": user})

# 修改用户信息
@require_http_methods(["PUT"])
def user_update(request):
    try:
        # 序列化获取
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    id = data.get('id')
    
    # 判断参数是否为空
    if id == None or id == '':
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，id 参数不能为空'})
    # 判断id是否存在
    if not User.objects.filter(id=id).exists():
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，修改的用户id不存在'})
    username = data.get('username')
    if username == None or username == '':
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，username 参数不能为空'})
    # 判断用户是否存在
    if User.objects.filter(username=username).exclude(id=id).exists():
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，用户名存在'})

    role_id = data.get('role_id')
    if role_id == None or role_id == '':
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，role_id 参数不能为空'})
    status = data.get('status')
    if status == None or status == '':
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，status 参数不能为空'})
    # 判断admin最高管理员用户角色或封禁状态不能被修改
    if id == 1 and (role_id != 1 or not status):
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，admin最高管理员用户角色或封禁状态不能被修改'})
    password = data.get('password')
    if password == None or password == '':
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，password 参数不能为空'})
    phone = data.get('phone')
    if phone == None or phone == '':
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，phone 参数不能为空'})
    sex = data.get('sex')
    if sex == None or sex == '':
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，sex 参数不能为空'})
    email = data.get('email')
    if email == None or email == '':
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，email 参数不能为空'})
    remarks = data.get('remarks')
    if remarks == None or remarks == '':
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，remarks 参数不能为空'})
    if remarks == None or remarks == '':
        remarks = ''
    try:
        # 修改用户信息
        User.objects.filter(id=id).update(username=username, password=password, phone=phone, sex=sex, email=email, status=status, role=role_id, updated_at = datetime.datetime.now(), remarks=remarks)
    except:
        return JsonResponse({'code': -1, 'message': '修改用户信息失败，修改用户失败'})
    return JsonResponse({"code":200,"message":"修改用户信息成功"})

# 删除用户信息
@require_http_methods(["DELETE"])
def user_delete(request, id):
    if id == "" or id == None:
        return JsonResponse({"code": -1, "message": "删除用户信息失败，id 参数不能为空"})
    if id == 1:
        return JsonResponse({"code": -1, "message": "删除用户信息失败，最高管理员不能被删除"})
    # 删除用户权限
    try:
        User.objects.filter(id=id).delete()
    except:
        return JsonResponse({"code": -1, "message": "删除用户信息失败，删除用户失败"})
    return JsonResponse({"code":200,"message":"删除用户信息成功"})
