from django.db import models


class User(models.Model):
    email = models.EmailField()
    fam = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    otc = models.CharField(max_length=100)
    phone = models.CharField(max_length=12, blank=True, null=True)


class Coords(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    height = models.IntegerField()


class Level(models.Model):
    winter = models.CharField(max_length=2, blank=True, null=True)
    summer = models.CharField(max_length=2, blank=True, null=True)
    autumn = models.CharField(max_length=2, blank=True, null=True)
    spring = models.CharField(max_length=2, blank=True, null=True)


class Pereval(models.Model):
    STATUSES = [
        ("new", "Новый"),
        ("pending", "Проверяется"),
        ("accepted", "Принят"),
        ("rejected", "Отклонён"),
    ]
    beauty_title = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    other_titles = models.CharField(max_length=100, blank=True, null=True)
    connect = models.CharField(max_length=100, blank=True, null=True)
    add_time = models.DateTimeField()
    status = models.CharField(choices=STATUSES, default='new')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coords = models.ForeignKey(Coords, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)


class Images(models.Model):
    pereval = models.ForeignKey(Pereval, on_delete=models.CASCADE, related_name='images')
    title = models.CharField(max_length=100, blank=True, null=True)
    data = models.CharField(blank=True, null=True)