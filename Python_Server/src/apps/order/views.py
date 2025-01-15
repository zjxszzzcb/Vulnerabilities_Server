from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from django.conf import settings
from common import helper
import json
from apps.order.models import Order
from django.views.decorators.http import require_http_methods

# 获取订单列表
@require_http_methods(["GET"])
def order_get(request):
    page = request.GET.get('page')
    size = request.GET.get('size')
    Keyword = request.GET.get('keyword')
    if page == None or page == '':
        page = 1
    if size == None or size == '':
        size = 10
    Page = int(page)
    Size = int(size)
    try:
        orderlistall = Order.objects.filter(deleted_at__isnull=True).values('id', 'food', 'user', 'num', 'created_at', 'updated_at').order_by('id')[(Page-1)*Size:Page*Size]
    except:
        return JsonResponse({"code": -1, "message": "获取订单列表失败"})
    if Keyword != None and Keyword != '':
        orderlistall = orderlistall.filter(food__contains=Keyword)
    cnt = orderlistall.count()
    return JsonResponse({"code":200,"message":"获取订单列表成功","result": {
        "count": cnt,
        "list":  list(orderlistall.values()),
    }})

# 新增订单信息
@require_http_methods(["POST"])
def order_add(request):
    try:
        # 序列化获取
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    food = data.get('food')
    num = data.get('num')
    remarks = data.get('remarks')
    if food == None or food == '':
        return JsonResponse({'code': -1, 'message': '新增订单信息失败，food 参数不能为空'})
    if remarks == None or remarks == '':
        remarks = ''
    # 判断菜品是否存在
    if Order.objects.filter(food=food).exists():
        return JsonResponse({'code': -1, 'message': '新增订单信息失败，菜品不存在'})
    # 获取用户信息
    UserInfo = helper.GetAuthorizationUserInfo(request.headers.get("Authorization"), settings)
    if UserInfo.get('Name') == None:
        return JsonResponse({'code': -1, 'message': '新增订单信息失败，用户信息获取失败'})
    try:
        # 创建订单
        Order.objects.create(user=UserInfo.get('Name'), food=food, num=num, remarks=remarks)
    except:
        return JsonResponse({'code': -1, 'message': '新增订单信息失败，创建订单失败'})
    return JsonResponse({"code":200,"message":"新增订单信息成功"})

# 根据ID获取订单信息
@require_http_methods(["GET"])
def order_detail(request):
    # 获取id
    id = request.GET.get('id')
    if id == "" or id == None:
        return JsonResponse({"code": -1, "message": "获取订单信息失败，id 参数不能为空"})
    try:
        data = {'user': "", 'food': "", 'num': "", 'remarks': ""}
        # 获取订单信息
        order = Order.objects.raw('SELECT `sys_order`.`id`, `sys_order`.`user`, `sys_order`.`food`, `sys_order`.`num`, `sys_order`.`remarks` FROM `sys_order` WHERE `sys_order`.`id` = '+ id)
        for o in order:
            data = {'user': o.user, 'food': o.food, 'num': o.num, 'remarks': o.remarks}
    except:
        return JsonResponse({"code": -1, "message": "获取订单信息失败，订单不存在"})
    if data["user"] == "":
        return JsonResponse({"code": -1, "message": "获取订单信息失败，订单不存在"})
    return JsonResponse({"code":200,"message":"获取订单信息成功","result": data})

# 删除订单信息
@require_http_methods(["DELETE"])
def order_delete(request, id):
    if id == "" or id == None:
        return JsonResponse({"code": -1, "message": "删除订单信息失败，id 参数不能为空"})
    # 删除订单权限
    try:
        Order.objects.filter(id=id).delete()
    except:
        return JsonResponse({"code": -1, "message": "删除订单信息失败，删除订单失败"})
    return JsonResponse({"code":200,"message":"删除订单信息成功"})
