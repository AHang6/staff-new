from django.db import models


# Create your models here.

class Depart(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
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
