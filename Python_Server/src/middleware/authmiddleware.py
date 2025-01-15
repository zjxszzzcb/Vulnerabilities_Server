from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.conf import settings
from common import helper

# 需要认证的路由
PROTECTED_PATHS = ["/settings", "/user", "/role", "/food", "/order", "/other"]  # 需要保护的路径

# 登录验证中间件
class AuthMiddleWare(MiddlewareMixin):
    def process_request(self, request):
        # 检查是否为受保护的路径
        if any(request.path.startswith(path) for path in PROTECTED_PATHS):
            # 获取 Authorization 头部
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return JsonResponse({'code': -1, 'msg': '请先登录'})
            # 提取 Token
            token = auth_header.split(" ")[1]
            # 验证 JWT
            jwtpayload = helper.Validatejwt(token, settings)
            if jwtpayload == None:
                return JsonResponse({'code': -1, 'msg': '当前登录已失效请重新登录'})
        # 非受保护路径继续处理
        return None

    # 请求后拦截
    def process_response(self, request, response):
        return response