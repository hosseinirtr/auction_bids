from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# class Add_auction(models.Model):
#     user = User()


class Categories(models.Model):
    categoryName = models.CharField(max_length=50)
    imageUrl = models.ImageField(upload_to='img', default="", )

    def __str__(self) -> str:
        return self.categoryName


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    # <img src="{{ image.image.url }}" alt="{{ image.alt_text }}">
    imageUrl = models.ImageField(upload_to='img')
    price = models.FloatField(max_length=12)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, blank=True, null=True, related_name='category')

    def __str__(self) -> str:
        return f"{self.title} from {self.owner}"


class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author")
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    message = models.CharField(max_length=200)
