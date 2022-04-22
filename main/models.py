from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from account.models import MyUser
from django.conf import settings

User = get_user_model()


class Category(models.Model):
    name = models.SlugField(max_length=100, primary_key=True)
    description = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(MyUser, related_name='post', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, related_name='post', on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    text = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)
    created_ad = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item_name


class PostImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='image')


class Rating(models.Model):
    product = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating')
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ])


class Like(models.Model):
    # post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like')
    # like = models.BooleanField('like', default=False)
    user = models.ForeignKey(User,
                             related_name='likes',
                             on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('product', 'object_id')
    like = models.BooleanField('like', default=False)


