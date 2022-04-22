from rest_framework import serializers
from .models import *


class RatingSerializers(serializers.ModelSerializer):
    owner = serializers.EmailField(required=False)

    class Meta:
        model = Rating
        fields = ('rating',)


class LikeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ('like',)


class CategorySerializers(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ImageSerializers(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = '__all__'


class PostSerializers(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'author', 'item_name', 'text', 'price', 'created_ad', 'category', 'image')

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     images_data = request.FILES
    #     product = Post.objects.create(**validated_data)
    #     for image in images_data.getlist('images'):
    #         PostImage.objects.create(product=product, image=image)
    #     return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
    #     # representation['author'] = instance.author.email
    #     # representation['category'] = CategorySerializers(instance.category).data
        representation['image'] = ImageSerializers(instance.images.all(), many=True, context=self.context).data
        return representation

    # def create(self, validated_data):
    #     request = self.context.get('request')
    #     user_id = request.user.id
    #     print(validated_data)
    #     validated_data['author_id '] = user_id
    #     post = Post.objects.create(**validated_data)
    #     return post
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating_result = 0
        for i in instance.rating.all():
            rating_result += int(i.rating)
        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result
        else:
            representation['rating'] = rating_result / instance.rating.all().count()

        return representation











