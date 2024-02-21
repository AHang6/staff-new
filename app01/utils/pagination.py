"""
自定义的分页组件，以后如果想要使用该组件，需要分一下几步

在视图函数中：
    def user_list(request):
        1、根据自己的情况去筛选中自己的数据
        user_data = UserInfo.objects.all()

        2、实例化 Pagination 对象， 传入参数 request, 以及数据库总数据
        page_obj = Pagination(request, user_data)

        context = {
            'user_data': page_obj.page_queryset,   # 分完页的数据
            'page_string': page_obj.html(),        # 分页html代码
    }

    3、 将数据传入到模板中
    return render(request, "user_list.html", context)

在模版中：
    <ul class="pagination center">
      {{ page_string }}
    </ul>
"""

from django.utils.safestring import mark_safe
import copy


class Pagination(object):

    def __init__(self, request, queryset, page_size=10, plus=5, page_parm="page"):

        # 使用深拷贝  对page复制， 直接修改 url  会与其他搜索功能产生冲突
        # 保留url中的 其他参数信息
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        # 获取page数值
        page = request.GET.get(page_parm, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        self.page = page
        self.page_size = page_size
        self.plus = plus
        self.page_parm = page_parm

        start = (page - 1) * page_size
        end = page * page_size

        self.page_queryset = queryset[start: end]

        # 计算总页码数
        total_count = queryset.count()
        page_count, div = divmod(total_count, page_size)
        if div > 0:
            page_count += 1

        self.page_count = page_count

    def html(self):
        page_list = []

        # 限制页码显示范围
        if self.page_count < self.plus * 2 + 1:
            start_page = 1
            end_page = self.page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = self.plus * 2 + 1
            else:
                if self.page + self.plus > self.page_count:
                    start_page = self.page_count - self.plus * 2
                    end_page = self.page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus

        # 首页
        self.query_dict.setlist(self.page_parm, [1])
        page_list.append('<li><a href="?{}" aria-label="Previous">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_parm, [self.page - 1])
            page_list.append(
                '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    self.query_dict.urlencode()))
        else:
            self.query_dict.setlist(self.page_parm, [1])
            page_list.append(
                '<li><a href="?{}" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    self.query_dict.urlencode()))

        # 页码
        for i in range(start_page, end_page + 1):
            if i == self.page:
                self.query_dict.setlist(self.page_parm, [i])
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
                page_list.append(ele)
            else:
                self.query_dict.setlist(self.page_parm, [i])
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
                page_list.append(ele)
        print(start_page, end_page)

        # 下一页
        if self.page < self.page_count:
            self.query_dict.setlist(self.page_parm, [self.page + 1])
            page_list.append(
                '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.query_dict.urlencode()))
        else:
            self.query_dict.setlist(self.page_parm, [self.page_count])
            page_list.append(
                '<li><a href="?{}" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.query_dict.urlencode()))

        # 尾页
        self.query_dict.setlist(self.page_parm, [self.page_count])
        page_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        search_page_string = """
            <li>
				<form action="" method="get" style="width: 150px; float: left; margin-left: 10px">
					<div class="input-group" >
						<input type="text" class="form-control" placeholder="Search for..." name="page">
						<span class="input-group-btn">
						<button class="btn btn-default" type="submit">跳转</button>
      				</span>
					</div><!-- /input-group -->
				</form>
			</li>
        """
        page_list.append(search_page_string)

        return mark_safe("".join(page_list))
