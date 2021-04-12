from django.db import models


class Resource(models.Model):
    """
    Модель товара на складе.
    """
    title = models.CharField(max_length=50, unique=True, verbose_name="Название")
    amount = models.FloatField(default=0, verbose_name="Количество")
    unit = models.CharField(max_length=7, verbose_name="Единица измерения")
    price = models.FloatField(default=0, verbose_name="Цена за у.е.")
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
        ordering = ['title']

    def __str__(self):
        return self.title
