from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings

tanks = 'TN'
hils = 'HL'
dd = 'DD'
merchants = 'MH'
guild_masters = 'GM'
quest_givers = 'QG'
blacksmiths = 'BM'
tanners = 'TN'
potion_makers = 'PM'
spell_masters = 'SM'

CATEGORY = [
    (tanks, 'Танки'),
    (hils, 'Хилы'),
    (dd, 'ДД'),
    (merchants, 'Торговцы'),
    (guild_masters, 'Гилдмастеры'),
    (quest_givers, 'Квестгиверы'),
    (blacksmiths, 'Кузнецы'),
    (tanners, 'Кожевники'),
    (potion_makers, 'Зельевары'),
    (spell_masters, 'Мастера заклинаний'),
]


class Post(models.Model):
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=2, choices=CATEGORY, default=tanks)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Reply(models.Model):
    reply_text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.reply_text

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def send_accepted_email(self):
        subject = 'Ваш отклик принят'
        message = f'Здравствуйте! Ваш отклик "{self.reply_text}" принят.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.user.email]

        send_mail(subject, message, from_email, recipient_list)
