from rest_framework import serializers

from .models import *

        
class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
        



class ContentReadSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField('get_image_url')
    
    
    def get_image_url(self,instance):
        request = self.context.get('request')
        if instance.image and instance.image is not None:
            image_url = instance.image.url
            if request is not None:
                return request.build_absolute_uri(image_url)
            return image_url
        else:
            return "https://placehold.co/600x400?text=File\nBroken"
    
    class Meta:
        model = Content
        fields = '__all__'
        
# class ContentDraftReadSerializer(serializers.ModelSerializer):
#     image=serializers.SerializerMethodField('get_image_url')
    
    
#     def get_image_url(self,instance):
#         request = self.context.get('request')
#         if instance.image and instance.image is not None:
#             image_url = instance.image.url
#             if request is not None:
#                 return request.build_absolute_uri(image_url)
#             return image_url
#         else:
#             return "https://placehold.co/600x400?text=File\nBroken"
    
#     class Meta:
#         model = Content
#         fields = '__all__'
        
class SettingsReadSerializer(serializers.ModelSerializer):
    image=serializers.SerializerMethodField('get_image_url')

    def get_image_url(self,instance):
        request = self.context.get('request')
        image_url = instance.image.url
        if request is not None:
            return request.build_absolute_uri(image_url)
        return image_url

    class Meta:
        model = SettingsEmail
        fields = '__all__'

class SettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SettingsEmail
        fields = '__all__'

class LayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Layout
        fields = '__all__'
        
class LayouttDraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = LayoutDraft
        fields = '__all__'
        
class BlogSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Blogs
        fields = '__all__'
        
    def to_representation(self, instance):
            representation = super().to_representation(instance)
            if not instance.file or not instance.file.name:
                representation['file'] = "https://placehold.co/600x400?text=File\nBroken"
            return representation