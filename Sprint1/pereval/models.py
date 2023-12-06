from django.db import models


class MyUser(models.Model):
    email = models.EmailField(max_length=255)
    fam = models.CharField(max_length=255, verbose_name='Фамилия')
    name = models.CharField(max_length=255, verbose_name='Имя')
    otc = models.CharField(max_length=255, verbose_name='Отчество')
    phone = models.CharField(max_length=12, verbose_name='Телефон')

    def __str__(self):
        return f'{self.fam} {self.name}'


class Coord(models.Model):
    latitude = models.FloatField(max_length=30, verbose_name='Широта')
    longitude = models.FloatField(max_length=30, verbose_name='Долгота')
    height = models.IntegerField(verbose_name='Высота')

    def __str__(self):
        return f'широта: {self.latitude}, долгота: {self.longitude}, высота: {self.height}'


LEVEL = [
    ('1a', '1A'),
    ('1b', '1Б'),
    ('2a', '2А'),
    ('2b', '2Б'),
    ('3a', '3А'),
    ('3b', '3Б'),
    ('4a', '4А'),
    ('4b', '4Б'),
    ('5a', '5А'),
    ('5b', '5Б'),
]


class Level(models.Model):
    winter = models.CharField(max_length=2, choices=LEVEL, verbose_name='Зима', null=True, blank=True)
    summer = models.CharField(max_length=2, choices=LEVEL, verbose_name='Лето', null=True, blank=True)
    autumn = models.CharField(max_length=2, choices=LEVEL, verbose_name='Осень', null=True, blank=True)
    spring = models.CharField(max_length=2, choices=LEVEL, verbose_name='Весна', null=True, blank=True)

    def __str__(self):
        return f'{self.winter} {self.summer} {self.autumn} {self.spring}'


class Pereval(models.Model):
    NEW = 'NW'
    PENDING = 'PN'
    ACCEPTED = 'AC'
    REJECTED = 'RJ'
    STATUS_CHOICES = (
        ('NW', 'New'),
        ('AC', 'Accepted'),
        ('PN', 'Pending'),
        ('RJ', 'Rejected'),
    )
    beauty_title = models.CharField(max_length=255, verbose_name='Индекс')
    title = models.CharField(max_length=255, verbose_name='Название')
    other_titles = models.CharField(max_length=255, verbose_name='Другое название', null=True, blank=True)
    connect = models.TextField(null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=NEW)
    coord_id = models.OneToOneField(Coord, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    level_id = models.ForeignKey(Level, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.beauty_title}'


class Images(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название', null=True, blank=True)
    data = models.ImageField(verbose_name='Изображение', null=True, blank=True)
    pereval_id = models.ForeignKey(Pereval, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'
