from django.shortcuts import render, HttpResponse
from django.http.response import JsonResponse
from django.conf import settings
import json, os
from common import helper
from apps.food.models import Food
from apps.user.models import User
from django.views.decorators.http import require_http_methods

# 获取食物列表信息
@require_http_methods(["GET"])
def food_get(request):
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
        foodlistall = Food.objects.filter(deleted_at__isnull=True).order_by('id')
        if Keyword != None and Keyword != '':
            foodlistall = foodlistall.filter(foodname=Keyword)
    except:
        return JsonResponse({'code': -1, 'message': '获取食物数据列表失败'})
    cnt = foodlistall.count()
    foodlisttmp = []
    for foodtmp in foodlistall:
        foodlisttmp.append({'id':foodtmp.id, 'user': foodtmp.user.username, 'user_id': foodtmp.user.id, 'foodname': foodtmp.foodname, 'price':foodtmp.price, 'foodicon':foodtmp.foodicon, 'foodprocedure':foodtmp.foodprocedure, 'video':foodtmp.video, 'remarks':foodtmp.remarks, 'created_at':foodtmp.created_at, 'updated_at':foodtmp.updated_at})
    return JsonResponse({"code":200,"message":"获取食物数据列表成功","result": {
        "count": cnt,
        "list":  foodlisttmp[(Page-1)*Size:Page*Size],
    }})

# 新增食物信息
@require_http_methods(["POST"])
def food_add(request):
    try:
        # 序列化获取
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    foodname = data.get('foodname')
    user_id = data.get('user_id')
    foodicon = data.get('foodicon')
    foodprocedure = data.get('foodprocedure')
    video = data.get('video')
    price = data.get('price')
    remarks = data.get('remarks')
    if foodname == None or foodname == '':
        return JsonResponse({"code": -1, "message": "菜品名称不能为空"})
    if user_id == None or user_id == '':
        return JsonResponse({"code": -1, "message": "用户ID不能为空"})
    if foodicon == None or foodicon == '':
        foodicon = ''
    if foodprocedure == None or foodprocedure == '':
        foodprocedure = ''
    if video == None or video == '':
        video = ''
    if price == None or price == '':
        return JsonResponse({"code": -1, "message": "菜品价格不能为空"})
    if remarks == None or remarks == '':
        remarks = ''

    # 检查食物是否存在
    if Food.objects.filter(foodname=foodname).exists():
        return JsonResponse({'code': -1, 'message': '新增菜品信息失败，菜品存在'})
    # 获取用户信息
    UserInfo = helper.GetAuthorizationUserInfo(request.headers.get("Authorization"), settings)
    if UserInfo.get('Uid') == None:
        return JsonResponse({'code': -1, 'message': '新增菜品信息失败，用户信息获取失败'})
    # 获取角色信息
    getuser = User.objects.filter(id=UserInfo.get('Uid')).first()
    if getuser == None:
        return JsonResponse({"code": -1, "message": "新增菜品信息失败，用户不存在"})
    if price < 0:
        return JsonResponse({"code": -1, "message": "新增菜品信息失败，菜品价格不能小于0"})
    
    try:
        # 创建菜品信息
        Food.objects.create(foodname=foodname, user_id=user_id, foodicon=foodicon, foodprocedure=foodprocedure, video=video, price=price, remarks=remarks)
    except:
        return JsonResponse({'code': -1, 'message': '新增菜品信息失败，创建菜品失败'})
    return JsonResponse({"code": 200, "message": "新增菜品信息成功"})

# 获取食物详细信息
@require_http_methods(["GET"])
def food_detail(request):
    # 获取id
    id = request.GET.get('id')
    if id == "" or id == None:
        return JsonResponse({"code": -1, "message": "获取菜品详情信息失败，id 参数不能为空"})
    # 获取菜品信息
    food = Food.objects.filter(id=id).values('id', 'foodname', 'price','user_id', 'foodicon', 'foodprocedure', 'video', 'remarks').first()
    if food == None:
        return JsonResponse({"code": -1, "message": "获取菜品详情信息失败，菜品不存在"})
    return JsonResponse({"code":200,"message":"获取菜品详情信息成功","result": food})

# 修改食物信息
@require_http_methods(["PUT"])
def food_update(request):
    try:
        # 序列化获取
        data = json.loads(request.body.decode("utf-8"))
    except:
        return JsonResponse({'code': -1, 'message': '参数绑定失败'})
    id = data.get('id')
    # 判断参数是否为空
    if id == None or id == '':
        return JsonResponse({'code': -1, 'message': '更新菜品信息失败，id 参数不能为空'})
    # 判断id是否存在
    if not Food.objects.filter(id=id).exists():
        return JsonResponse({'code': -1, 'message': '更新菜品信息失败，修改的菜品id不存在'})
    foodname = data.get('foodname')
    if foodname == None or foodname == '':
        return JsonResponse({'code': -1, 'message': '更新菜品信息失败，foodname 参数不能为空'})
    # 判断菜品是否存在
    if Food.objects.filter(foodname=foodname).exclude(id=id).exists():
        return JsonResponse({'code': -1, 'message': '更新菜品信息失败，菜品名存在'})
    # 判断价格
    price = data.get('price')
    if price == None or price == '':
        price = 0
    foodicon = data.get('foodicon')
    if foodicon == None or foodicon == '':
        foodicon = ""
    foodprocedure = data.get('foodprocedure')
    if foodprocedure == None or foodprocedure == '':
        foodprocedure = ""
    video = data.get('video')
    if video == None or video == '':
        video = ""
    remarks = data.get('remarks')
    if remarks == None or remarks == '':
        return JsonResponse({'code': -1, 'message': '更新菜品信息失败，remarks 参数不能为空'})
    if remarks == None or remarks == '':
        remarks = ''
    try:
        # 更新菜品信息
        Food.objects.filter(id=id).update(foodname=foodname, foodicon=foodicon, foodprocedure=foodprocedure, remarks=remarks, video=video, price=price)
    except:
        return JsonResponse({'code': -1, 'message': '更新菜品信息失败，更新菜品失败'})
    return JsonResponse({"code":200,"message":"更新菜品信息成功"})

# 删除食物信息
@require_http_methods(["DELETE"])
def food_delete(request, id):
    if id == "" or id == None:
        return JsonResponse({"code": -1, "message": "删除菜品失败，id 参数不能为空"})
    # 判断id是否存在
    if not Food.objects.filter(id=id).exists():
        return JsonResponse({'code': -1, 'message': '删除菜品失败，菜品id不存在'})
    # 获取菜品信息
    food = Food.objects.filter(id=id).first()
    # 删除菜品图片
    if food.foodicon != "":
        if ".." in food.foodicon:
            return JsonResponse({"code": -1, "message": "删除菜品失败，图片文件删除失败"})
        helper.DeleteFile(food.foodicon)
    # 删除菜品视频
    if food.video != "":
        if ".." in food.foodicon:
            return JsonResponse({"code": -1, "message": "删除菜品失败，视频文件删除失败"})
        helper.DeleteFile(food.video)

    # 删除食物信息
    try:
        Food.objects.filter(id=id).delete()
    except:
        return JsonResponse({"code": -1, "message": "删除菜品失败，删除用户失败"})
    return JsonResponse({"code":200,"message":"删除菜品成功"})

# 上传菜品ICON
@require_http_methods(["POST"])
def food_upfoodicon(request):
    filedata = request.FILES.get("file", None)
    try:
        filepath = helper.Uploadfile(os.path.join(settings.UPLOAD_FOLDER, "food/"), filedata)
    except:
        return JsonResponse({"code":-1,"message":"上传菜品ICON失败"})
    return JsonResponse({"code":200,"message":"上传菜品ICON成功", "result": filepath})

# 上传菜品视频
@require_http_methods(["POST"])
def food_upfoodvideo(request):
    filedata = request.FILES.get("file", None)
    try:
        filepath = helper.Uploadfile(os.path.join(settings.UPLOAD_FOLDER, "food/"), filedata)
    except:
        return JsonResponse({"code":-1,"message":"上传菜品视频失败"})
    return JsonResponse({"code":200,"message":"上传菜品视频成功", "result": filepath})

