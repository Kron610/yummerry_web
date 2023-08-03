from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    name = models.CharField(max_length=200,
                            validators=[MinLengthValidator(2, "Длина названия продукта должна быть более 2 символов")])

    def __str__(self):
        return self.name


class Filling(models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(2, "Длина названия продукта должна быть более 2 символов")])

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(2, "Длина названия города должна быть более 2 символов")])

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(2, "Длина названия района должна быть более 2 символов")])
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Confectioner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fullName = models.CharField(max_length=300,
                                validators=[MinLengthValidator(5, "ФИО не может быть меньше 5 символов")],
                                blank=True)
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True)
    pickup = models.BooleanField(default=True)
    telegram = models.CharField(max_length=200, blank=True)
    delivery = models.BooleanField(default=True)

    def __str__(self):
        return self.fullName


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_confectioner(sender, instance, created, **kwargs):
    if created:
        Confectioner.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_confectioner(sender, instance, **kwargs):
    instance.confectioner.save()


class Card(models.Model):
    name = models.CharField()
    description = models.CharField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fillings = models.ManyToManyField(Filling)
    owner = models.ForeignKey(Confectioner, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='upload/')
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
