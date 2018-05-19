from django.db import models
from django.urls import reverse
from categories.models import Category
from django_comments.moderation import CommentModerator, moderator


class Good(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True, verbose_name='Название')
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Краткое описание')
    content = models.TextField(verbose_name='Полное описание')
    price = models.FloatField(db_index=True, verbose_name='Цена, руб.')
    price_acc = models.FloatField(null=True, blank=True, verbose_name='Цена с учетом скидки, руб.')
    in_stock = models.BooleanField(default=True, db_index=True, verbose_name='Есть в наличии')
    featured = models.BooleanField(default=False, db_index=True, verbose_name='Рекомендуемый')
    image = models.ImageField(upload_to='goods/list', verbose_name='Основное изображение')

    def save(self, *args, **kwargs):
        try:
            this_record = Good.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        images = GoodImage.objects.filter(good=self)
        for image in images:
            image.delete()
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('goods_detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class GoodImage(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='goods/detail', verbose_name='Дополнительное изображение')

    def save(self, *args, **kwargs):
        try:
            this_record = GoodImage.objects.get(pk=self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save=False)
        except:
            pass
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete(save=False)
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'изображение к товару'
        verbose_name_plural = 'изображения к товару'


class GoodModerator(CommentModerator):
    email_notification = True


moderator.register(Good, GoodModerator)
