from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
import json, datetime
from apps.user.models import Role
from django.views.decorators.http import require_http_methods

# 获取角色列表信息
@require_http_methods(["GET"])
def role_get(request):
    # 获取页数等信息
    page = request.GET.get('page')
    size = request.GET.get('size')
    Keyword = request.GET.get('keyword')
    if page == None or page == '':
        page = 1
    if size == None or size == '':
        size = 10
    Page = int(page)
    Size = int(size)
    rolelistall = Role.objects.filter(deleted_at__isnull=True).values('id', 'name', 'level', 'created_at', 'updated_at').order_by('id')
    if Keyword != None and Keyword != '':
        rolelistall = rolelistall.filter(name__contains=Keyword)
    cnt = rolelistall.count()
    return JsonResponse({"code":200,"message":"获取角色列表信息成功","result": {
        "count": cnt,
        "list":  list(rolelistall.values())[(Page-1)*Size:Page*Size],
    }})

# 新增角色信息
@require_http_methods(["POST"])
def role_add(request):
    try:
        # 序列化获取
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    name = data.get('name')
    level = data.get('level')
    remarks = data.get('remarks')
    if name == None or name == '':
        return JsonResponse({'code': -1, 'message': '新增角色信息失败，name 参数不能为空'})
    if level == None or level == '':
        return JsonResponse({'code': -1, 'message': '新增角色信息失败，level 参数不能为空'})
    if remarks == None or remarks == '':
        remarks = ''
    # 判断角色是否存在
    if Role.objects.filter(name=name).exists():
        return JsonResponse({'code': -1, 'message': '新增角色信息失败，角色存在'})
    try:
        # 创建角色
        Role.objects.create(name=name, level=level, remarks=remarks)
    except:
        return JsonResponse({'code': -1, 'message': '新增角色信息失败，创建用户失败'})
    return JsonResponse({"code":200,"message":"新增角色信息成功"})

# 获取角色详细信息
@require_http_methods(["GET"])
def role_detail(request):
    # 获取id
    id = request.GET.get('id')
    if id == "" or id == None:
        return JsonResponse({"code": -1, "message": "获取角色详细信息失败，id 参数不能为空"})
    # 获取角色信息
    role = Role.objects.filter(id=id).values('id', 'name', 'level').first()
    if role == None:
        return JsonResponse({"code": -1, "message": "获取角色详细信息失败，角色不存在"})
    return JsonResponse({"code":200,"message":"获取角色详细信息成功","result": role})

# 修改角色信息
@require_http_methods(["PUT"])
def role_update(request):
    try:
        # 序列化获取
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    id = data.get('id')
    # 判断参数是否为空
    if id == None or id == '':
        return JsonResponse({'code': -1, 'message': '修改角色信息失败，id 参数不能为空'})
    # 判断id是否存在
    if not Role.objects.filter(id=id).exists():
        return JsonResponse({'code': -1, 'message': '修改角色信息失败，修改的角色id不存在'})
    name = data.get('name')
    if name == None or name == '':
        return JsonResponse({'code': -1, 'message': '修改角色信息失败，name 参数不能为空'})
    # 判断角色是否存在
    if Role.objects.filter(name=name).exclude(id=id).exists():
        return JsonResponse({'code': -1, 'message': '修改角色信息失败，角色名存在'})
    level = data.get('level')
    remarks = data.get('remarks')
    if level == None or level == '':
        return JsonResponse({'code': -1, 'message': '修改角色信息失败，level 参数不能为空'})
    if remarks == None or remarks == '':
        remarks = ''
    # 判断admin最高管理角色等级不能被修改
    if id == 1 and level != 1:
        return JsonResponse({'code': -1, 'message': '修改角色信息失败，admin最高管理角色等级不能被修改'})
    try:
        # 修改角色信息
        Role.objects.filter(id=id).update(name=name, level=level, updated_at = datetime.datetime.now(), remarks=remarks)
    except:
        return JsonResponse({'code': -1, 'message': '修改角色信息失败，修改角色失败'})
    return JsonResponse({"code":200,"message":"修改角色信息成功"})

# 删除角色信息
@require_http_methods(["DELETE"])
def role_delete(request, id):
    if id == "" or id == None:
        return JsonResponse({"code": -1, "message": "删除角色信息失败，id 参数不能为空"})
    if id == 1:
        return JsonResponse({"code": -1, "message": "删除角色信息失败，最高管理角色不能被删除"})
    # 删除角色权限
    try:
        Role.objects.filter(id=id).delete()
    except:
        return JsonResponse({"code": -1, "message": "删除角色信息失败，删除角色失败"})
    return JsonResponse({"code":200,"message":"删除角色信息成功"})
