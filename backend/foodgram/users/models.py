from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Subscription(models.Model):
    who_subscribes = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribes',
        verbose_name='Тот кто подписывается'
    )
    subscribes_to = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribers',
        verbose_name='Тот на кого подписываются'
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        return (f'{self.who_subscribes.username}'
                f' подписан на {self.subscribes_to.username}.')
