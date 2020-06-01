from django.db import models


class Music(models.Model):
    name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    price = models.FloatField(default=0)
    image_url = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return '{}'.format(self.name)


class Cart:
    def __init__(self, item_list=None):
        if item_list is None:
            item_list = []
        self.item_list = item_list
        self.total_price = 0

    def cal_total_price(self):
        for item in self.item_list:
            self.total_price += item.price
