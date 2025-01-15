import logging
import time

# 获取日志记录器
logger = logging.getLogger('django.request')

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()  # 记录请求开始时间
        response = self.get_response(request)
        end_time = time.time()  # 记录请求结束时间
        # 获取客户端 IP
        client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
        # 计算请求的耗时
        duration = end_time - start_time
        # 记录请求日志
        logger.info("| {} | {: <.2f}s | {: <15} | {: <4} | {} |".format(response.status_code, duration, client_ip, request.method, request.path))
        return response
