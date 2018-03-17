import django.dispatch

# from ContentApp.models import Remark

comment_done = django.dispatch.Signal(providing_args=['obj'])

from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.core.signals import request_finished


# @receiver(pre_save, sender=Remark)
# def my_handler(sender, **kwargs):
#     print('hhh')


def zhutao(sender, kwargs):
    if "obj" in kwargs:
        obj = kwargs.get("obj")

        print(obj, 'oojuju')

# comment_done.connect(zhutao, sender=Remark)