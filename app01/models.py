from django.db import models


# Create your models here.

class Depart(models.Model):
    """   部门表   """
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """   用户表   """
    name = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateTimeField(verbose_name="入职时间")
    depart = models.ForeignKey(verbose_name="部门", to="Depart", to_field="id", on_delete=models.CASCADE)

    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class MobileNum(models.Model):
    """   靓号表  """
    mobile = models.CharField(verbose_name="手机号", max_length=32)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2)

    level_choices = (
        (1, '一级'),
        (2, '二级'),
        (3, '三级'),
        (4, '四级'),
        (5, '五级'),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices)

    status_choices = (
        (1, "占用"),
        (2, "未占用"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices)


class Admin(models.Model):
    """   管理员   """
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=32)

    def __str__(self):
        return self.username


class Task(models.Model):
    """   任务表   """
    level_choices = (
        (1, '紧急'),
        (2, '重要'),
        (3, '普通'),
    )

    level = models.SmallIntegerField(verbose_name="任务等级", choices=level_choices)

    title = models.CharField(verbose_name="标题", max_length=32)
    detail = models.CharField(verbose_name="详细信息", max_length=32)
    user = models.ForeignKey(verbose_name="负责人", to="Admin", to_field="id", on_delete=models.CASCADE)


class Older(models.Model):
    """   订单表   """
    older = models.CharField(verbose_name="订单号", max_length=32)
    title = models.CharField(verbose_name="商品名称", max_length=32)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2)

    status_choices = (
        (0, "待支付"),
        (1, "已支付"),
    )

    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices)

    user = models.ForeignKey(verbose_name="用户", to=Admin, to_field="id", on_delete=models.CASCADE)

