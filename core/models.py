from django.db import models
from decimal import Decimal


class NetworkNode(models.Model):
    """
    Модель узла торговой сети.

    Атрибуты:
        name (CharField): Название узла (магазина/склада).
        email (EmailField): Контактный email.
        country (CharField): Страна расположения.
        city (CharField): Город расположения.
        street (CharField): Улица.
        house_number (CharField): Номер дома.
        supplier (ForeignKey[NetworkNode] | None): Ссылка на поставщика (родительский узел).
        debt_to_supplier (DecimalField): Задолженность перед поставщиком.
        created_at (DateTimeField): Время создания записи.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=20)
    supplier = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='clients',
        help_text='Поставщик данного узла (или None для корневого).'
    )
    debt_to_supplier = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal('0.00'),
        help_text='Задолженность перед поставщиком.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Узел сети'
        verbose_name_plural = 'Узлы сети'

    def __str__(self):
        """
        Строковое представление узла.
        """
        return f"{self.name} ({self.city})"

    @property
    def level(self) -> int:
        """
        Вычисляет уровень вложенности в иерархии поставщиков.
        Корневой узел (без supplier) — уровень 0, его клиенты — 1 и т.д.
        """
        if not self.supplier:
            return 0
        return self.supplier.level + 1


class Product(models.Model):
    """
    Модель продукта, привязанного к узлу сети.

    Атрибуты:
        node (ForeignKey[NetworkNode]): Узел, к которому привязан товар.
        title (CharField): Название товара.
        model (CharField): Модель или артикул.
        release_date (DateField): Дата релиза.
    """
    node = models.ForeignKey(
        NetworkNode,
        on_delete=models.CASCADE,
        related_name='products',
        help_text='Узел, к которому относится этот продукт.'
    )
    title = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    release_date = models.DateField()

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        """
        Строковое представление продукта.
        """
        return f"{self.title} {self.model}"
