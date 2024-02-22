from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class M1(MiddlewareMixin):
    def process_request(self, request):
        # 1、排除不需要登录就可以访问的网站
        if request.path_info in ["/login/", '/image/code/']:
            return

        # 2、读取当前访问的用的session信息，如果能读到，说明已登陆过，就可以继续访问
        info = request.session.get('info')
        if info:
            return

        return redirect('/login/')
