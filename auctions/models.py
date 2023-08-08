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
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)
    imageUrl = models.ImageField(upload_to='img')
    price = models.FloatField(max_length=12)
    isActive = models.BooleanField(default=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="owned_listings"
    )
    category = models.ForeignKey(
        Categories, on_delete=models.CASCADE, blank=True, null=True, related_name='listed_in_categories'
    )

    def __str__(self) -> str:
        return f"{self.title} from {self.owner}"


class WatchlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    id = models.BigAutoField(primary_key=True)
    
    def __str__(self) -> str:
        return f"{self.listing}"

class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments_author"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="comments"
    )
    message = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)


class Bids(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bids_user"
    )
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="bids"
    )
    offered_price = models.IntegerField(blank=False)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return f"@{self.user.username} offered {self.offered_price} on {self.date}"