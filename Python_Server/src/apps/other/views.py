from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.conf import settings
from common import helper
import os, zipfile

# 测试上传ZIP并解压功能
@require_http_methods(["POST"])
def other_uploadzip(request):
    filedata = request.FILES.get("file", None)
    try:
        zip_file = helper.Uploadfile(os.path.join(settings.UPLOAD_FOLDER, "zip/"), filedata)
        # 使用zipfile解压文件
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(settings.UPLOAD_FOLDER, "zip/"))
    except:
        return JsonResponse({"code":-1,"message":"上传ZIP包失败"})
    return JsonResponse({"code":200,"message":"上传ZIP并解压成功", "result": "解压目录为:"+zip_file})
