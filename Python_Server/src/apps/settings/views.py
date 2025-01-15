from django.shortcuts import render, HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, FileResponse
from django.conf import settings
from common import helper
import os

# 测试连通性
@require_http_methods(["POST"])
def settings_ping(request):
    ipaddr = request.POST.get('addre')
    if ipaddr == "":
        return JsonResponse({"code": -1,"message": "测试连通性失败", "result": "addre is none"})
    output = os.popen("ping " + ipaddr).read()
    return JsonResponse({"code":200,"message": "测试连通性成功", "result": output})

# 获取备份数据库列表
@require_http_methods(["POST"])
def settings_getdb(request):
    dir = request.POST.get('dir')
    try:
        dbNames = os.listdir(dir)
    except:
        return JsonResponse({"code": -1,"message": "获取备份数据库列表失败"})
    return JsonResponse({"code":200,"message":"获取备份数据库列表成功", "result": dbNames})

# 备份数据库
@require_http_methods(["GET"])
def settings_backupsdb(request):
    # 数据库连接配置
    db_config = settings.DATABASES['default']
    # 备份
    backupfile = helper.Dackupdb(db_config['HOST'], db_config['USER'], db_config['PASSWORD'], db_config['NAME'], settings.BACKUP_FOLDER)
    if "err：" in backupfile:
        return JsonResponse({"code": -1,"message": "备份数据库失败"})
    return JsonResponse({"code":200,"message":"备份数据库成功"})

# 删除备份数据库
@require_http_methods(["POST"])
def settings_deletedb(request):
    dbfile = request.POST.get('dbfile')
    # 删除数据库
    if helper.DeleteFile(os.path.join(settings.BACKUP_FOLDER, dbfile)):
        return JsonResponse({"code":200,"message": "删除"+dbfile+"备份数据库成功"})
    return JsonResponse({"code": -1,"message": "删除备份数据库失败"})

# 数据库下载
@require_http_methods(["POST"])
def settings_downdb(request):
    dbfile = request.POST.get('dbfile')
    # 检查文件是否存在
    if not os.path.exists(os.path.join(settings.BACKUP_FOLDER, dbfile)):
        return JsonResponse({"code": -1,"message": "下载数据库失败"})
    # 使用 FileResponse 返回文件
    response = FileResponse(open(os.path.join(settings.BACKUP_FOLDER, dbfile), 'rb'), as_attachment=True, filename=dbfile)
    return response