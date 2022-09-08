from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
)
from django.db import models


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='email',
        help_text='Введите адрес электронной почты'
        )
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Имя пользователя',
        help_text='Введите имя пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
        help_text='Введите ваше имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
        help_text='Введите вашу фамилию'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    class Meta:
        ordering = ('id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.username


class Following(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
        )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Отслеживаемый пользователь',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_following',
            )
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} now following {self.author}'
